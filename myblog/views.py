from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, TemplateView, ListView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from myblog.forms import ContactForm, SignUpForm

from myblog.models import Post


class HomeView(ListView):
    model = Post
    template_name = "myblog/index.html"
    context_object_name = "posts"
    extra_context = {"title": "Главная страница"}
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = context["page_obj"]
        context["paginator_range"] = page.paginator.get_elided_page_range(
            page.number, on_each_side=1, on_ends=1
        )
        return context


class PostDetailView(DetailView):
    template_name = "myblog/post_detail.html"
    # Если бы из urls возвращался бы slug:slug, то такой подход бы сработал.
    # Мы указалы бы, что в модели Post атрибут url соответствует слагу
    # А так нужно написать метод get_object
    # slug_field = 'url'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.title
        # context['title'] = context['post'].title
        # context['title'] = Post.objects.get(url=self.kwargs['post_url']).title
        return context

    def get_object(self, queryset=None):
        post = Post.objects.get(url=self.kwargs["post_url"])
        return post


class TagView(ListView):
    template_name = "myblog/index.html"
    context_object_name = "posts"
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = Post.objects.filter(tag=self.kwargs["tag"])[0].tag
        page = context["page_obj"]
        context["paginator_range"] = page.paginator.get_elided_page_range(
            page.number, on_each_side=1, on_ends=1
        )
        return context

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


class AboutView(TemplateView):
    template_name = "about.html"
    extra_context = {"title": "О нас"}



