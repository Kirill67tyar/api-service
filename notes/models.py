from django.db.models import (
    Model, CharField, TextField, DateTimeField,
)


class Note(Model):
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
