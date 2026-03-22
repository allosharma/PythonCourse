from django.shortcuts import render
from home.models import Product
from django.contrib.postgres.search import (
    SearchVector, SearchQuery, SearchRank,
    SearchHeadline, TrigramSimilarity
)
from django.db.models import Q
from django.views.decorators.cache import cache_page
from django.core.cache import cache


@cache_page(60 * 1) # It wil be cached for 1 minutes
def homePage(request):

    search_query = request.GET.get("search")
    selected_brand = request.GET.get("brand")
    selected_category = request.GET.get("category")
    selected_max_price = request.GET.get("max_price")

    products = Product.objects.all()

    # SEARCH
    if search_query:

        vector = (
            SearchVector("title", weight="A") +
            SearchVector("description", weight="B") +
            SearchVector("category", weight="C") +
            SearchVector("brand", weight="D")
        )

        query = SearchQuery(search_query)

        products = products.annotate(
            search=vector,
            rank=SearchRank(vector, query),
            similarity=(
                TrigramSimilarity("title", search_query) +
                TrigramSimilarity("brand", search_query) +
                TrigramSimilarity("category", search_query)
            ),
            headline=SearchHeadline(
                "description",
                query,
                start_sel="<mark>",
                stop_sel="</mark>",
            )
        ).filter(
            Q(rank__gte=0.1) | Q(similarity__gt=0.3)
        ).order_by("-rank", "-similarity").distinct()

    # PRODUCT FILTERS
    if selected_brand:
        products = products.filter(brand=selected_brand)

    if selected_category:
        products = products.filter(category=selected_category)

    if selected_max_price:
        products = products.filter(price__lte=selected_max_price)

    # BRAND DROPDOWN
    brand_queryset = Product.objects.all()

    if selected_category:
        brand_queryset = brand_queryset.filter(category=selected_category)

    brands = (
        brand_queryset
        .exclude(brand__isnull=True)
        .exclude(brand="")
        .values_list("brand", flat=True)
        .distinct()
        .order_by("brand")
    )

    # CATEGORY DROPDOWN (depends on brand)
    category_queryset = Product.objects.all()

    if selected_brand:
        category_queryset = category_queryset.filter(brand=selected_brand)

    categories = (
        category_queryset
        .exclude(category__isnull=True)
        .exclude(category="")
        .values_list("category", flat=True)
        .distinct()
        .order_by("category")
    )

    context = {
        "products": products,
        "search": search_query,
        "brands": brands,
        "categories": categories,
        "selected_brand": selected_brand,
        "selected_category": selected_category,
        "max_price": selected_max_price,
    }

    return render(request, "index.html", context)