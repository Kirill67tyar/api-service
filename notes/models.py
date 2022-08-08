from django.contrib.auth import get_user_model
from django.db.models import (
    Model, CharField, TextField,
    DateTimeField, ForeignKey, SET_NULL,

)

User = get_user_model()


class Note(Model):
    author = ForeignKey(
        to=User,
        on_delete=SET_NULL,
        related_name='notes',
        blank=False,
        null=True,
    )
    title = CharField(
        max_length=255,
        verbose_name='Заголовок'
    )
    text = TextField(
        blank=True,
        verbose_name='Содержание записи'
    )
    created = DateTimeField(
        auto_now_add=True,
        verbose_name='Запись создана'
    )
    updated = DateTimeField(
        auto_now=True,
        verbose_name='Запись изменена'
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-updated', '-created',)
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
