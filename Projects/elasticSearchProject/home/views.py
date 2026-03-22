from django.shortcuts import render
from django.http import JsonResponse
from home.documents import PostDocument
from elasticsearch_dsl.query import MultiMatch


def search_product(request):
    data = {
        'status': '200',
        'message': 'Products Fetched Successfully',
        'products': []
    }

    if request.GET.get('search'):
        search = request.GET.get('search')

        result = PostDocument.search().query(
            MultiMatch(
                query=search,
                fields=['name', 'description'],
                fuzziness='auto'
            )
        )

        result = result.execute()

        products = []
        for hit in result:
            products.append({
                'Product Name': hit.name,
                'brand': '',
                'price': hit.price,
                'stock': hit.stock,
                'image': hit.image,
                'description': hit.description,
                'score': hit.meta.score
            })

        data['products'] = products

    return JsonResponse(data)