from catalog.forms import CommentForm
from catalog.models import Post
from catalog.tasks import send_mail

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage, Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import generic

User = get_user_model()


def start(request):
    return render(request, 'catalog/start.html')


class AuthorDetailView(generic.DetailView):
    model = User
    template_name = 'catalog/author.html'


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    fields = ['title', 'short_text', 'full_text', 'status']
    success_url = reverse_lazy("catalog:own_posts")
    login_url = '/accounts/login/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        text = f"{form.instance.author} create new post right now!"
        send_mail.delay('New post.', text, 'main.blog@mail.com', ['admin@mail.com'])
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Post
    fields = ['title', 'short_text', 'full_text', 'status']
    success_url = reverse_lazy('catalog:own_posts')
    login_url = '/accounts/login/'


class PostDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Post
    success_url = reverse_lazy('catalog:own_posts')
    login_url = '/accounts/login/'


class AllPostsListView(generic.ListView):
    model = Post
    paginate_by = 20
    template_name_suffix = '_all_list'

    def get_queryset(self):
        return Post.objects.filter(
            status='published'
        )


class OwnPostsListView(LoginRequiredMixin, generic.ListView):
    model = Post
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(
            author=self.request.user
        )


def user_posts(request, pk):
    post = Post.objects.filter(author_id=pk, status='published')
    author = User.objects.get(pk=pk)
    page = request.GET.get('page', 1)
    paginator = Paginator(post, 2)
    try:
        page_posts = paginator.page(page)
    except EmptyPage:
        raise Http404
    return render(
        request,
        'catalog/user_posts.html',
        {
            'post': post,
            'author': author,
            'paginator': paginator,
            'page_posts': page_posts
        }
    )


def post_with_comment(request, pk):
    Post.objects.prefetch_related('comment_set')
    post = get_object_or_404(Post, pk=pk)
    comments = post.comment_set.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 2)
    try:
        page_comments = paginator.page(page)
    except EmptyPage:
        raise Http404
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            text_to_admin = 'The user left a new comment. Need to check it out.'
            send_mail.delay('New comment', text_to_admin, 'main.blog@mail.com', ['admin@mail.com'])

            text_to_user = 'A new comment has been added to your post.'
            author = post.author
            send_mail.delay('New comment', text_to_user, 'main.blog@mail.com', [author.email])

        return redirect('catalog:one_post', pk=pk)
    else:
        comment_form = CommentForm()
    return render(
        request,
        'catalog/one_post.html',
        {
            'post': post,
            'form': comment_form,
            'comments': comments,
            'paginator': paginator,
            'page_comments': page_comments,
        }
    )
