from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class News(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, blank=True, db_index=True, default='', verbose_name="Слаг")
    content = models.TextField(blank=True, verbose_name="Контент")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", default=None, blank=True, null=True, verbose_name="Фото")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время Обновления")
    is_published = models.BooleanField(default=True, verbose_name="Флаг публикации")
    cat = models.ForeignKey("Category", on_delete=models.PROTECT, null=True, verbose_name="Категория")
    profiles = models.ForeignKey("Profiles", on_delete=models.PROTECT, null=True, verbose_name="Профиль")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новости'
        verbose_name_plural = 'Новости'
        ordering = ['-time_create', 'title']
        indexes = [
            models.Index(fields=['-time_create'])
        ]

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True, db_index=True, default='')

    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категории'


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('cat', kwargs={'cat_slug': self.slug})

class Profiles(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, verbose_name="Профиль")
    land = models.CharField(max_length=255, verbose_name="Страна")
    age = models.IntegerField(max_length=10, verbose_name="Возраст")
    photo = models.ImageField(upload_to="profiles/%Y/%m/%d/", default=None, blank=True, null=True, verbose_name="Фото")

    def __str__(self):
        return f"{self.user}"
    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Comment(models.Model):
    user = models.ForeignKey("Profiles", on_delete=models.PROTECT, null=True, verbose_name="Профиль")
    news = models.ForeignKey("News", on_delete=models.PROTECT, null=True, verbose_name="Новость")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    content = models.TextField(blank=True, verbose_name="Контент")

    def __str__(self):
        return f" Комментарий {self.user} к новости {self.news} || {self.pk}"
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
