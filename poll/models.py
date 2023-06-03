from django.db import models
from django.utils import timezone
from django.urls import reverse

from file.models import Category
from user.models import Profile


class Testing(models.Model):
    title = models.CharField(max_length=200, verbose_name='Тест')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    is_published = models.BooleanField(default=True, verbose_name="Публикация")
    polls = models.ManyToManyField("Poll", related_name="Ответы")
    description = models.CharField("Описание теста", max_length=500, blank=True, null=True)
    points = models.IntegerField("Очки", default=0, help_text="Количество правильных ответов для прохождения теста")
    photo = models.ImageField(upload_to='image/')

    cat = models.ForeignKey(Category, on_delete=models.PROTECT)

    def get_absolute_url(self):
        return reverse('poll_list', kwargs={'testing_slug': self.slug})

    class Meta:
        verbose_name = 'Тесты'
        verbose_name_plural = 'Тесты'

    def __str__(self):
        return self.title


class Poll(models.Model):
    #testing_id = models.ForeignKey(Testing, on_delete=models.CASCADE, verbose_name='Вопрос')
    text = models.TextField()
    choices = models.ManyToManyField("Choice", related_name="Ответы")

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Choice(models.Model):
    name = models.CharField(max_length=20)
    # poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="Ответ")
    IsRight = models.BooleanField()

    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответа'

    def __str__(self):
        return self.name


class Vote(models.Model):
    testing_id = models.OneToOneField(Testing, on_delete=models.CASCADE, verbose_name='Тест')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='User')
    test_passed = models.BooleanField(verbose_name="Тест пройден", default=False)

    poll = models.ForeignKey(
        Poll, on_delete=models.SET_NULL, related_name="votes", null=True, blank=True)
    choice = models.ForeignKey(
        Choice, on_delete=models.SET_NULL, related_name="votes", null=True, blank=True)

    # timestamp = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return f"{self.poll.text} - {self.choice.name}"

    class Meta:
        verbose_name = 'Итог тестирования'
        verbose_name_plural = 'Итоги тестирований'
