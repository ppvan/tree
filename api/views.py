import os

import requests
from django.contrib.postgres.search import SearchQuery, SearchVector
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View

from blog.models import Post
from core.models import District, Product, Province, Ward

# Create your views here.


class ProductSearchView(View):
    def search_product(self, query):
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
        return products

    def search_post(self, query):
        search_vector = SearchVector("title__unaccent")
        search_query = SearchQuery(query)
        posts = (
            Post.objects.annotate(
                search=search_vector, rank=SearchVector(search_vector, search_query)
            )
            .filter(search=search_query)
            .order_by("-rank")[:5]
        )
        return posts

    def get(self, request):
        query = request.GET.get("q", "")
        products = self.search_product(query)
        posts = self.search_post(query)
        return render(
            request,
            "components/search_result_item.html",
            {
                "products": products,
                "posts": posts,
            },
        )


class ProvinceView(View):
    def get(self, request):
        return JsonResponse(
            [
                {"id": province.id, "name": province.name}
                for province in Province.objects.all().order_by("name")
            ],
            safe=False,
        )


class DistrictView(View):
    def get(self, request):
        province_id = request.GET.get("province_id")
        return JsonResponse(
            [
                {"id": district.id, "name": district.name}
                for district in District.objects.filter(
                    province_id=province_id
                ).order_by("name")
            ],
            safe=False,
        )


class WardView(View):
    def get(self, request):
        district_id = request.GET.get("district_id")
        return JsonResponse(
            [
                {"id": ward.id, "name": ward.name}
                for ward in Ward.objects.filter(district_id=district_id).order_by(
                    "name"
                )
            ],
            safe=False,
        )


class TransportFeeView(View):
    API = "https://online-gateway.ghn.vn/shiip/public-api/v2/shipping-order/fee"
    API_TOKEN = os.getenv("API_TOKEN")
    SHOP_DISTRICT_ID = os.getenv("SHOP_DISTRICT_ID")

    def get(self, request):
        payload = {
            "service_id": request.GET.get("service_id"),
            "insurance_value": 0,  # 500k bảo hiểm?
            "from_district_id": self.SHOP_DISTRICT_ID,
            "to_district_id": request.GET.get("district_id"),
            "to_ward_code": request.GET.get("ward_code"),
            # Một cái cây cảnh chắc là 2kg, 50x50x20 cm
            "height": 50,
            "length": 50,
            "weight": 1000,
            "width": 20,
        }

        r = requests.get(self.API, headers={"Token": self.API_TOKEN}, params=payload)
        response = r.json()
        if response["code"] != 200:
            return JsonResponse({"total": "-1"}, status=400)

        return JsonResponse(response["data"], safe=False)


class TransportServiceView(View):
    API = "https://online-gateway.ghn.vn/shiip/public-api/v2/shipping-order/available-services"
    API_TOKEN = os.getenv("API_TOKEN")
    SHOP_ID = os.getenv("SHOP_ID")
    SHOP_DISTRICT_ID = os.getenv("SHOP_DISTRICT_ID")

    def get(self, request):
        payload = {
            "shop_id": self.SHOP_ID,
            "from_district": self.SHOP_DISTRICT_ID,
            "to_district": request.GET.get("district_id"),
        }
        r = requests.get(self.API, headers={"Token": self.API_TOKEN}, params=payload)
        response = r.json()
        if response["code"] != 200:
            return JsonResponse([], safe=False)

        return JsonResponse(r.json()["data"], safe=False)


class GenerateAvatarView(View):
    API = "https://ui-avatars.com/api/"

    def get(self, request, name):
        r = requests.get(self.API, params={"name": name}, stream=True)
        return HttpResponse(r.content, content_type="image/png")
