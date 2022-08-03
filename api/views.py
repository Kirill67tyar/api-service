from rest_framework.response import Response
from rest_framework.decorators import api_view
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
    NoteSerializer, NoteModelSerializer,
)
from common.utils import get_object_or_null
from common.analize.analizetools import (
    delimiter, console, p_dir, p_type, p_mro
)


@api_view(['GET', 'POST', ])  # по умолчанию идёт только GET запрос. Если запрос каоторый не указан в списке то 405
def note_list_create_api_view(request):  # , format=None
    if request.method == 'GET':
        notes = Note.objects.all()
        serializer = NoteSerializer(notes, many=True)
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
