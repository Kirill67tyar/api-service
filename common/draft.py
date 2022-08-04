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


Как передавать:

 -- для read
    SomeSerializer(instance=<model_instance>) # один экземпляр
    SomeSerializer(instance=<some QuerySet>, many=True) # много

 -- для create
    SomeSerializer(data=request.data) # один экземпляр

 -- для update
    SomeSerializer(instance=<model_instance>, data=request.data) # один экземпляр



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
3 - если данные не валидны, то надо вернуть serializer.errors

В модельных формах первым аргументом идёт data, а instance где-то в конце и по умолчанию
В сериалайзерах не так. Первым аргументом идёт instance, а data идёт вторым аргументом
когда ты меняешь существующую запись через модельный сериалайзер, то нужно передавать
в instance=старую запись, а в data=request.data (новую дату)


------------- Response

class Response(SimpleTemplateResponse):
    ' (тройные ковычки)
    An HttpResponse that allows its data to be rendered into
    arbitrary media types.
    ' (тройные ковычки)

    def __init__(self, data=None, status=None,
                 template_name=None, headers=None,
                 exception=False, content_type=None):
        ' (тройные ковычки)
        Alters the init arguments slightly.
        For example, drop 'template_name', and instead use 'data'.

        Setting 'renderer' and 'media_type' will typically be deferred,
        For example being set automatically by the `APIView`.
        ' (тройные ковычки)

Принимает аргументы:
 - data - то что передаётся serializer.data, по сути обычный словарь
 - status - статус код, берётся из rest_framework.status (status=status.HTTP_405_METHOD_NOT_ALLOWED)



И так:

    HTTP GET
     -- serializer = Serializer(instance=<[QuerySet ...]>, many=True)  # read (list)
        return Response(data=serializer.data, status=status.HTTP_200_OK)  # [OrderedDict(...

     -- serializer = Serializer(instance=<instance Model>)  # read (detail)  # <class 'rest_framework.utils.serializer_helpers.ReturnDict'>
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    HTTP POST
     -- serializer = Serializer(data=request.data)  # create
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.data, status=status.HTTP_400_BAD_REQUEST)

    HTTP PUT, PATH
     -- serializer = Serializer(instance=<instance Model>, data=request.data)  # update
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.data, status=status.HTTP_400_BAD_REQUEST)

    HTTP DELETE
     -- data = get_object_or_404(Model, **kwargs)
        serializer = Serializer(instance=data)
        data.delete()
        return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(
                data={'status': 'object has successfully deleted',},
                status=status.HTTP_204_NO_CONTENT
                )


------------- Миксины DRF

Классы которые используют миксины:

    from rest_framework.generics (
        ListAPIView,
        RetrieveAPIView,
        UpdateAPIView,
        CreateAPIView,
        DestroyAPIView,
    )

Сами миксины
    from rest_framework.mixins import (
        ListModelMixin,
        RetrieveModelMixin,
        CreateModelMixin,
        UpdateModelMixin,
        DestroyModelMixin,
    )
C:\Users\kiril\Desktop\Job\tree-of-knowledge\Django\DRF\media\схема_GenericAPIView_3


 -- GenericAPIView(APIView)
    предоставляет некие методы, для связки миксинов, и дженериков типа ListAPIView, RetrieveAPIView и т.д.

    Два обязательных аргумента при определении обработчика от миксинов и GenericAPIView:
    serializer_class =
    queryset =
    т.к. GenericAPIView заимствуется от APIView, а тот в свояю очередь от View от Django,
    то мы можем настраивать queryset, get_model и т.д.
    !!! def get_queryset(self) находится в GenericAPIView
    Это может нам понадобиться чтобы оптимизировать queryset, сделать фильтрацию по нему,
    или select_related (JOIN), т.е. оптимизировать запрос в db

"""





