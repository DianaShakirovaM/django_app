from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse


class Menu(models.Model):
    name = models.CharField('Название меню', max_length=100, unique=True)

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    menu = models.ForeignKey(
        Menu, on_delete=models.CASCADE, related_name='items',
        verbose_name='Меню')
    title = models.CharField('Заголовок', max_length=100)
    url = models.CharField('URL', max_length=255, blank=True)
    named_url = models.CharField('Named URL', max_length=255, blank=True)
    parent = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE,
        related_name='children', verbose_name='Родитель')
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'
        ordering = ('order', 'id')
        unique_together = ('menu', 'parent', 'order')

    def __str__(self):
        return self.title

    def clean(self):
        if self.url and self.named_url:
            raise ValidationError(
                'Укажите либо URL, либо named URL, но не оба.')
        if not self.url and not self.named_url:
            raise ValidationError(
                'Укажите хотя бы один из: URL или named URL.')

    def get_absolute_url(self):
        if self.named_url:
            return reverse(self.named_url)
        return self.url
