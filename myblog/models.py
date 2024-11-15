from django.contrib.auth import get_user_model
from django.db import models

from myblog.services.utils import unique_slugify


class Post(models.Model):
    h1 = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    url = models.SlugField(max_length=255, blank=True)
    description = models.TextField()
    content = models.TextField()
    tag = models.CharField(max_length=200)
    image = models.ImageField(upload_to="myblog/%Y/%m/%d", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ['-id']

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.url:
            self.url = unique_slugify(self, self.title)
        super().save(*args, **kwargs)
