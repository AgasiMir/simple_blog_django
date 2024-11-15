from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    search_fields = ["title", "author__username", "tag"]
    list_display = ["get_image", "title", "tag", "author", "created_at"]
    list_display_links = ["get_image", "title"]
    ordering = ["-id", "title", "author"]
    date_hierarchy = "created_at"
    list_filter = ["created_at", "author__username"]
    list_per_page = 10

    fields = [
        "get_fields_image",
        "h1",
        "title",
        "description",
        "content",
        "tag",
        "image",
        "author",
    ]
    save_on_top = True
    readonly_fields = ["get_fields_image"]

    @admin.display(description="image")
    def get_image(self, obj: Post):
        if obj.image:
            return mark_safe(f"<img src={obj.image.url} width=160>")
        return "No image"

    @admin.display(description="image")
    def get_fields_image(self, obj: Post):
        if obj.image:
            return mark_safe(f"<img src={obj.image.url} width=80%>")
        return "No image"


admin.site.site_title = "myblog"
admin.site.site_header = "myblog"
admin.site.index_title = "Администрирование myblog"
