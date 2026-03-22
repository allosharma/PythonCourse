from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from .models import Products


@registry.register_document
class PostDocument(Document):
    class Index:
        name = 'products'    # use default index name
        settings = {'number_of_shards': 1, 'number_of_replicas': 0}

    class Django:
        model = Products
        fields = [
            'name',
            'price',
            'stock',
            'image',
            'description']