from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from catalog.models import Post

User = get_user_model()


def start(request):
    return render(request, 'catalog/start.html')


class AuthorDetailView(generic.DetailView):
    model = User
    template_name = 'catalog/author.html'


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    fields = ['title', 'short_text', 'full_text', 'status']
    success_url = reverse_lazy("catalog:user_posts")
    login_url = '/accounts/login/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        text = f"{form.instance.author} create new post right now!"
        # send_mail_to_admin.delay(text)
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Post
    fields = ['title', 'short_text', 'full_text', 'status']
    success_url = reverse_lazy('catalog:user_posts')
    login_url = '/accounts/login/'


class PostDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Post
    success_url = reverse_lazy('catalog:user_posts')
    login_url = '/accounts/login/'


class AllPostsListView(generic.ListView):
    model = Post
    paginate_by = 20
    template_name_suffix = '_all_list'



class OwnPostsListView(LoginRequiredMixin, generic.ListView):
    model = Post
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(
            author=self.request.user
        )


class PostDetailView(generic.DetailView):
    model = Post
