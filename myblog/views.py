from django.views.generic import TemplateView, ListView

from myblog.models import Post


class HomeView(ListView):
    model = Post
    template_name = "myblog/index.html"
    context_object_name = 'posts'
    extra_context = {"title": "Главная страница"}


class AboutView(TemplateView):
    template_name = "about.html"
    extra_context = {"title": "О нас"}


class ContactView(TemplateView):
    template_name = "contact.html"
    extra_context = {"title": "Контакты"}
