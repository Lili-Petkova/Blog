from catalog.forms import CommentForm, ContactForm, PostModelForm
from catalog.models import Post
from catalog.tasks import contact_mail, send_mail

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage, Paginator
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.views import generic
from django.views.decorators.cache import cache_page

User = get_user_model()


@cache_page(60 * 60)
def start(request):
    return render(request, 'catalog/start.html')


class AuthorDetailView(generic.DetailView):
    model = User
    template_name = 'catalog/author.html'


def create_post(request):
    author = request.user
    if request.method == 'POST':
        post_form = PostModelForm(request.POST, request.FILES, instance=author)
        if post_form.is_valid():
            post_form.save()
            messages.add_message(request, messages.SUCCESS, 'Post was created successfuly')
            status = post_form.cleaned_data['status']
            if status == 'deferred':
                text = f"{author} create new post right now!"
                send_mail.delay('New post.', text, 'main.blog@mail.com', ['admin@mail.com'])
            return redirect('catalog:all_posts')
    else:
        post_form = PostModelForm(instance=author)
    return render(
        request,
        'catalog/post_form.html',
        {
            'form': post_form,
        }
    )


def update_post(request, pk):
    post = Post.objects.get(pk=pk)
    user = request.user
    if post.author == user:
        if request.method == 'POST':
            post_form = PostModelForm(data=request.POST, instance=post)
            if post_form.is_valid():
                post_form.save()
                messages.add_message(request, messages.SUCCESS, 'Post has been successfully updated!')
                status = post.status
                if status == 'deferred':
                    text = f"{user} has just updated a previously published post!"
                    send_mail.delay('New post.', text, 'main.blog@mail.com', ['admin@mail.com'])
                return redirect('catalog:start')
        else:
            post_form = PostModelForm(instance=post)

        return render(
            request,
            'catalog/post_update.html',
            {
                'form': post_form,
                'user': user,
            }
        )
    else:
        return redirect('catalog:one_post', pk=pk)


def delete_post(request, pk):
    post = Post.objects.get(pk=pk)
    user = request.user
    if post.author == user:
        if request.method == 'POST':
            post_form = PostModelForm(data=request.POST, instance=post)
            post.delete()
            messages.add_message(request,  messages.SUCCESS, 'Post has been successfully deleted!')
            return redirect('catalog:own_posts')
        else:
            post_form = PostModelForm(instance=post)

        return render(
            request,
            'catalog/post_confirm_delete.html',
            {
                'form': post_form,
                'post': post
            }
        )
    else:
        return redirect('catalog:own_posts')


class AllPostsListView(generic.ListView):
    model = Post
    paginate_by = 40
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
    paginator = Paginator(post, 2)
    page = request.GET.get('page', 1)
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
    comments = post.comment_set.all().filter(status=True)
    paginator = Paginator(comments, 2)
    page = request.GET.get('page', 1)
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
            messages.add_message(request, messages.SUCCESS, 'Your comment has been accepted and will be published after'
                                                            ' verification by the administrator.')
            text_to_admin = 'The user left a new comment. Need to check it out.'
            send_mail.delay('New comment', text_to_admin, 'main.blog@mail.com', ['admin@mail.com'])
            url = request.build_absolute_uri()
            text_to_user = f'A new comment has been added to your post {post.title} {url} from {new_comment.author}.'
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


def contact(request):
    data = dict()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            text = form.cleaned_data['text']
            data['form_is_valid'] = True
            contact_mail.delay(text, email)
            mes = messages.add_message(request,  messages.SUCCESS, 'Message sent')
            context = {'mes': mes}
            data['answer'] = render_to_string('catalog/includes/success.html', context, request=request)
        else:
            data['form_is_valid'] = False
    else:
        form = ContactForm()
    context = {'form': form}
    data['html_form'] = render_to_string('catalog/includes/contact_form.html', context, request=request)
    return JsonResponse(data)
