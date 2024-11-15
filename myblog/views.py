from django.views.generic import TemplateView, ListView

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


class AboutView(TemplateView):
    template_name = "about.html"
    extra_context = {"title": "О нас"}


class ContactView(TemplateView):
    template_name = "contact.html"
    extra_context = {"title": "Контакты"}
