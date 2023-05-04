from django.contrib.postgres.search import SearchQuery, SearchVector
from django.http import JsonResponse
from django.views import View

from core.models import Product
from core.serializers import ModelSerializer

# Create your views here.


class ProductSearchView(View):
    def get(self, request):
        query = request.GET.get("q", "")
        search_vector = SearchVector(
            "name__unaccent", "summary__unaccent", "description__unaccent"
        )
        search_query = SearchQuery(query)
        products = (
            Product.objects.annotate(
                search=search_vector, rank=SearchVector(search_vector, search_query)
            )
            .filter(search=search_query)
            .order_by("-rank")[:20]
        )
        result = ModelSerializer(products).to_dict()
        return JsonResponse(result, safe=False)
