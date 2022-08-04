from rest_framework import serializers

from notes.models import Note


class NoteSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    title = serializers.CharField(
        required=True,
        max_length=255
    )
    text = serializers.CharField(
        required=False,  # аналог required=False у форм
        allow_blank=True  # аналог blank=True у моделей
    )

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)  # self.title
        instance.text = validated_data.get('text', instance.text)
        instance.save()
        return instance

    def create(self, validated_data):
        return Note.objects.create(**validated_data)


class ListNoteModelSerializer(serializers.ModelSerializer):
    # формирует абсолютный url.
    # нужно добавить в сериалайзер в обработчике context={'request': request,}
    url = serializers.HyperlinkedIdentityField(view_name='api:detail')

    class Meta:
        model = Note
        fields = ('id', 'title', 'url',)


class NoteModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('id', 'title', 'text', 'created', 'updated',)  # '__all__'
        extra_kwargs = {
            'created': {'read_only': True, },
            'updated': {'read_only': True, },
        }
