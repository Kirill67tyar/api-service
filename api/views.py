from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    CreateAPIView,
    DestroyAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    get_object_or_404
)
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
)
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_405_METHOD_NOT_ALLOWED,

)

from notes.models import Note
from api.serializers import (
    NoteSerializer,
    NoteModelSerializer,
    ListNoteModelSerializer,
    UserModelSerializer,
)
from api.permissions import IsAuthorOrAuthenticatedReadOnly
from common.utils import get_object_or_null
from common.analize.analizetools import (
    delimiter, console, p_dir, p_type, p_mro, console_compose2,
)

User = get_user_model()


@api_view(['GET', 'POST', ])  # по умолчанию идёт только GET запрос. Если запрос который не указан в списке то 405
def note_list_create_api_view(request):  # , format=None
    if request.method == 'GET':
        notes = Note.objects.all()
        serializer = NoteSerializer(
            instance=notes,
            many=True
        )
        return Response(
            data=serializer.data,
            status=HTTP_200_OK
        )
    else:
        serializer = NoteSerializer(data=request.data)  # request.data - как request.GET и request.POST

        # --- console ---
        delimiter()
        console(request.GET, request.POST, request.data)
        delimiter()
        # --- console ---

        if serializer.is_valid():
            serializer.save()
            return Response(
                data=serializer.data,
                status=HTTP_200_OK
            )
        else:
            return Response(
                data=serializer.errors,
                status=HTTP_400_BAD_REQUEST
            )


@api_view(['GET', 'PUT', 'DELETE', ])
def note_detail_update_delete_api_view(request, pk):  # , format=None
    note = get_object_or_null(
        model=Note,
        pk=pk
    )
    if note:
        if request.method == 'GET':
            serializer = NoteSerializer(instance=note)
            return Response(
                data=serializer.data,
                status=HTTP_200_OK
            )
        elif request.method == 'PUT':
            serializer = NoteSerializer(
                instance=note,
                data=request.data
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    data=serializer.data,
                    status=HTTP_201_CREATED
                )
            else:
                return Response(
                    data=serializer.data,
                    status=HTTP_400_BAD_REQUEST
                )
        elif request.method == 'DELETE':
            serializer = NoteSerializer(instance=note)
            note.delete()
            # return Response(
            #     data=serializer.data,
            #     status=HTTP_200_OK
            # )
            return Response(status=HTTP_204_NO_CONTENT)
        else:
            return Response(
                data={'status': '405 Method Not Allowed', },
                status=HTTP_405_METHOD_NOT_ALLOWED
            )
    else:
        return Response(
            data={'status': '404 Not Found', },
            status=HTTP_404_NOT_FOUND
        )


http_method_names = [
    "get",
    "post",
    "put",
    "patch",
    "delete",
    "head",
    "options",
    "trace",
]


class NoteListAPIView(APIView):
    model = Note
    http_method_names = [
        "get",
        "post",
        "head",
        "options",
    ]

    def get(self, request, *args, **kwargs):
        notes = self.model.objects.all()
        serializer = ListNoteModelSerializer(
            instance=notes,
            many=True,
            context={'request': request, }
        )
        return Response(
            data=serializer.data,
            status=HTTP_200_OK
        )

    def post(self, request, *args, **kwargs):
        serializer = NoteModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data=serializer.data,
                status=HTTP_201_CREATED
            )
        else:
            return Response(
                data=serializer.data,
                status=HTTP_400_BAD_REQUEST
            )


class NoteDetailAPIView(APIView):  # APIView.mro --> View
    queryset = Note.objects.all()
    http_method_names = [
        "get",
        "put",
        "head",
        "options",
        "delete",
    ]

    def get(self, request, pk, *args, **kwargs):
        note = get_object_or_404(self.queryset, pk=pk)
        serializer = NoteModelSerializer(instance=note)
        return Response(data=serializer.data, status=HTTP_200_OK)

    def put(self, request, pk, *args, **kwargs):
        note = get_object_or_404(self.queryset, pk=pk)
        serializer = NoteModelSerializer(
            instance=note,
            data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                data=serializer.data, status=HTTP_201_CREATED
            )
        return Response(
            data=serializer.data, status=HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk, *args, **kwargs):
        note = get_object_or_404(
            queryset=self.queryset,
            pk=pk
        )
        note_id = note.pk
        note.delete()
        return Response(
            data={'status': f'object id={note_id} was successfully deleted', },
            status=HTTP_204_NO_CONTENT
        )


class NoteListCreateAPIView(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteModelSerializer
    http_method_names = [
        "get",
        "post",
        "options",
        "head",
    ]

    def get_queryset(self):
        return super().get_queryset()  # .filter()  # - ну и тут можно отсортировать как-то, related_name сделать

    def get(self, request, *args, **kwargs):
        self.serializer_class = ListNoteModelSerializer
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class NoteDetailUpdateDeleteAPIView(RetrieveModelMixin,
                                    UpdateModelMixin,
                                    DestroyModelMixin,
                                    GenericAPIView):
    serializer_class = NoteModelSerializer
    queryset = Note.objects.all()
    http_method_names = [
        "get",
        "put",
        "delete",
        "head",
        "options",
        "trace",
    ]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class EasyNoteListCreateAPIView(ListCreateAPIView):
    serializer_class = NoteModelSerializer
    queryset = Note.objects.all()
    http_method_names = [
        "get",
        "post",
        "head",
        "options",
        "trace",
    ]

    # def list(self, request, *args, **kwargs):
    #     serializer = ListNoteModelSerializer(
    #         instance=request.data,
    #         many=True,
    #         context={'request': request, }
    #     )
    #     return Response(serializer.data, status=HTTP_200_OK)

    def get_serializer_class(self):  # get_serializer_class от GenericAPIView
        if self.request.method == 'GET':
            self.serializer_class = ListNoteModelSerializer
        return super().get_serializer_class()


class EasyNoteDetailUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = NoteSerializer
    queryset = Note.objects.all()
    http_method_names = [
        "get",
        "put",
        "delete",
        "head",
        "options",
        "trace",
    ]


class NoteModelViewSet(ModelViewSet):
    serializer_class = NoteModelSerializer
    queryset = Note.objects.all()
    http_method_names = [
        "get",
        "post",
        "put",
        "patch",
        "delete",
        "head",
        "options",
        "trace",
    ]
    permission_classes = (IsAuthorOrAuthenticatedReadOnly,)

    def get_serializer_class(self):
        # --- console ---
        delimiter()
        console(
            self.request.GET,  # если POST http://127.0.0.1:8000/api/notes/?ask=1 то будет {'ask': ['1']}
            self.request.data,
            self.request.POST
            # если POST http://127.0.0.1:8000/api/notes/?ask=1 то будет {'title': 'some title with querystring'}
            # p_dir(self.request),
            # console_compose2(self.request, stype=1)

        )
        delimiter()
        # --- console ---

        if self.action == 'list':
            self.serializer_class = ListNoteModelSerializer
        return super(NoteModelViewSet, self).get_serializer_class()

    # def get_queryset(self):
    #     """
    #         если пользователь админ, то он увидит все записи,
    #         если пользователь не админ, но аутентифицировн, то увидит
    #         только те, которые закреплены за конкретным пользльзователем
    #     """
    #     user = self.request.user
    #     if user.is_admin:
    #         return self.queryset
    #     return self.queryset.filter(author=user)

    def perform_create(self, serializer):  # благодаря этому методу мы можем добавлять свою логику
        serializer.save(author=self.request.user)


class UserModelViewSet(ModelViewSet):
    model = User
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    permission_classes = (IsAdminUser,)
    http_method_names = [
        "get",
        "post",
        "put",
        "patch",
        "delete",
        "head",
        "options",
        "trace",
    ]
