from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse

from user.models import Profile

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url1(self):
        return reverse('video_category', kwargs={'cat_slug': self.slug})
    def get_absolute_url_wiki(self):
        return reverse('wiki_category', kwargs={'cat_slug': self.slug})
    def get_absolute_url_task(self):
        return reverse('task_category', kwargs={'cat_slug': self.slug})
    def get_absolute_url_testing(self):
        return reverse('testing_category', kwargs={'cat_slug': self.slug})
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']

# class Data(models.Model):
#     title = models.CharField(max_length=100)
#     slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
#     content = models.TextField()
#     photo = models.ImageField(upload_to='image/')
#
#     file = models.FileField(upload_to="video/", validators=[FileExtensionValidator(allowed_extensions=['mp4'])])
#
#     time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
#     time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
#
#     is_published = models.BooleanField(default=True, verbose_name="Публикация")
#     cat = models.ForeignKey('Category', on_delete=models.PROTECT)
#
#     def __str__(self):
#         return self.title
#
#     def get_absolute_url(self):
#         return reverse('video', kwargs={'video_slug': self.slug})
#
#     class Meta:
#         verbose_name = 'Видео-курс'
#         verbose_name_plural = 'Видео-курсы'
#         ordering = ['id']

class VideoCourse(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField()
    photo = models.ImageField(upload_to='image/')

    file = models.FileField(upload_to="video/", validators=[FileExtensionValidator(allowed_extensions=['mp4'])])

    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")

    is_published = models.BooleanField(default=True, verbose_name="Публикация")
    cat = models.ForeignKey('Category', on_delete=models.PROTECT)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('video', kwargs={'video_slug': self.slug})

    class Meta:
        verbose_name = 'Видео-курс'
        verbose_name_plural = 'Видео-курсы'
        ordering = ['id']

class Wiki(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(null=True)
    photo = models.ImageField(upload_to='image/')
    file = models.FileField(upload_to="wiki/", validators=[FileExtensionValidator(allowed_extensions=['pdf'])])

    is_published = models.BooleanField(default=True, verbose_name="Публикация")

    cat = models.ForeignKey('Category', on_delete=models.PROTECT)

    def __str__(self):
        return self.title



    class Meta:
        verbose_name = 'Вики'
        verbose_name_plural = 'Вики'
        ordering = ['id']

class Tasks(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(null=True)
    photo = models.ImageField(upload_to='image/')
    file = models.FileField(upload_to="task/", validators=[FileExtensionValidator(allowed_extensions=['docx'])])

    is_published = models.BooleanField(default=True, verbose_name="Публикация")

    cat = models.ForeignKey('Category', on_delete=models.PROTECT)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('task', kwargs={'task_slug': self.slug})

    class Meta:
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'
        ordering = ['id']

class TaskAnswer(models.Model):
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE, verbose_name='Задание')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='User')
    task_passed = models.BooleanField(verbose_name="Задание пройдено", default=False)
    file = models.FileField(upload_to="answer/", validators=[FileExtensionValidator(allowed_extensions=['docx'])])

    def get_absolute_url(self):
        return reverse('taskanswer', kwargs={'taskanswer_pk': self.pk})

    def __str__(self):
        return self.user.name+self.task.name

    class Meta:
        verbose_name = 'Итог практической работы'
        verbose_name_plural = 'Итоги практических'