from django.db.models import Manager

from django.db.models.query import QuerySet
from django.db.models.manager import BaseManager
from django.db.models.fields.related_descriptors import ReverseManyToOneDescriptor, ManyToManyDescriptor


def get_object_or_null(model, **kwargs):
    if isinstance(model, (QuerySet,
                          BaseManager,
                          ManyToManyDescriptor,
                          ReverseManyToOneDescriptor)):
        return model.filter(**kwargs).first()
    return model.objects.filter(**kwargs).first()


class PostManager(Manager):
    def main(self, since=None, limit=10):
        qs = self.order_by('-pk')
        if since:
            qs = qs.fitler(pk__lt=since)
        response = []
        for p in qs[:1000]:
            if not len(response):
                response.append(p)
            elif response[-1].category != p.category:
                response.append(p)
            if len(response) >= limit:
                break
        return response
