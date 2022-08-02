"""
from rest_framework import serializers

-------------------------------- serializers.Serializer -----------------------------------------------

Что интересно, базовый класс BaseSerializer унаследован
от класса Field, который также определён в rest_framework

Это нужно для того, чтобы наши сериалайзеры могли быть как классами,
которые сериализуют и десиреализуют, так и могли быть полями, вложенными сериалайзерами
в других сериалайзерах

В сериалайзер мы можем передавать:

 -- QuerySet
    тогда обязательно передавать аргумент many=True

 -- Экземпляр модели
    тогда можно передать many=False, (many=False по умолчанию)

Аргументы BaseSerializer(Field)
def __init__(self, instance=None, data=empty, **kwargs)

Аргументы класса Field
def __init__(self, *, read_only=False, write_only=False,
                 required=None, default=empty, initial=empty, source=None,
                 label=None, help_text=None, style=None,
                 error_messages=None, validators=None, allow_null=False)

Сам сериалайзер не преобразовывает объекты Python в json данные
Он преобразовывает объекты Python в другие объекты Python - OrderedDict


Если хотим обратиться к содержимому сериалайзера, то нужно:

1 - вызвать метод is_valid()
2 - обратиться по атрибуту data  -  serializer.data

"""