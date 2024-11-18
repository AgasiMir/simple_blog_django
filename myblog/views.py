from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    TemplateView,
    ListView,
)
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from myblog.forms import CommentForm, ContactForm, SignUpForm

from myblog.models import Post, Comment


class MixinView:
    template_name = "myblog/index.html"
    context_object_name = "posts"
    paginate_by = 6

    def get_mixin_context(self, context):
        page = context["page_obj"]
        context["paginator_range"] = page.paginator.get_elided_page_range(
            page.number, on_each_side=1, on_ends=1
        )
        return context


class HomeView(MixinView, ListView):
    model = Post
    extra_context = {"title": "Главная страница"}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)


class PostDetailView(DetailView):
    template_name = "myblog/post_detail.html"
    # Если бы из urls возвращался бы slug:slug, то такой подход бы сработал.
    # Мы указалы бы, что в модели Post атрибут url соответствует слагу
    # А так нужно написать метод get_object
    # slug_field = 'url'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.title
        context["comment_form"] = CommentForm
        context["comments"] = Comment.objects.filter(post=self.object)
        # context['title'] = context['post'].title
        # context['title'] = Post.objects.get(url=self.kwargs['post_url']).title
        return context

    def get_object(self, queryset=None):
        post = Post.objects.get(url=self.kwargs["post_url"])
        return post


class TagView(MixinView, ListView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = Post.objects.filter(tag=self.kwargs["tag"])[0].tag
        return self.get_mixin_context(context)

    def get_queryset(self):
        return Post.objects.filter(tag=self.kwargs["tag"])


class UserLoginView(LoginView):
    model = get_user_model()
    template_name = "myblog/signin.html"
    form_class = AuthenticationForm
    extra_context = {"title": "Авторизация"}
    next_page = "home"


class UserLogoutView(LogoutView):
    next_page = "home"


class UserRegistrationView(CreateView):
    template_name = "myblog/signup.html"
    form_class = SignUpForm
    extra_context = {"title": "Регистрация"}
    success_url = reverse_lazy("signin")


class ContactView(CreateView):
    template_name = "myblog/contact.html"
    form_class = ContactForm
    extra_context = {"title": "Обратная связь"}
    success_url = reverse_lazy("home")


class Search(MixinView, ListView):

    search_obj = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = str(self.__class__.search_obj).capitalize()
        return self.get_mixin_context(context)

    def get_queryset(self):
        if "q" in self.request.GET:
            self.__class__.search_obj = self.request.GET.get("q")
        return Post.objects.filter(
            Q(title__iregex=self.__class__.search_obj)
            | Q(tag__iregex=self.__class__.search_obj)
        )


class CommentCreateView(LoginRequiredMixin, CreateView):
    form_class = CommentForm

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post_id = self.kwargs.get("pk")
        comment.username = self.request.user
        comment.save()
        # return redirect(self.request.META.get("HTTP_REFERER"))
        return redirect(comment.post.get_absolute_url())


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment

    def get_object(self, queryset=None):
        Comment.objects.get(pk=self.kwargs["pk"]).delete()


class CommentCreateView_2(View):
    def post(self, request, pk):
        form = CommentForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.post_id = pk
            form.username = self.request.user
            form.save()
        return redirect(self.request.META.get("HTTP_REFERER"))
        # return redirect(form.post.get_absolute_url())


class AboutView(TemplateView):
    template_name = "about.html"
    extra_context = {"title": "О нас"}
