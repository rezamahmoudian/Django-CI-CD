from rest_framework import status
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from typing import Dict
from drf_spectacular.utils import extend_schema

from myproject.api.pagination import LimitOffsetPagination
# from myproject.blog.models import Product

from myproject.blog.selectors.product import get_product
from myproject.blog.services.product import create_product


def response_func(status: bool, msg: str, data: Dict) -> Dict:
    res = {
        'status': status,
        'message': msg,
        'data': data
    }
    return res


class ProductAPI(APIView):

    class Pagination(LimitOffsetPagination):
        default_limit = 15

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=255)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            # model = Product
            fields = ['name', 'created_at', 'updated_at']

    @extend_schema(responses=OutputSerializer)
    def get(self, request):
        query = get_product()
        data = self.OutputSerializer(query, context={"request": request}, many=True).data
        return response_func(status=True, msg="products", data=data)

    @extend_schema(request=InputSerializer, responses=OutputSerializer)
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(self, raise_exception=True)

        try:
            query = create_product(name= serializer.validated_data('name'))
            data = self.OutputSerializer(query, context={"request": request}, many=True).data
            return response_func(status=True, msg="product created", data=data)

        except Exception as ex:
            return Response(
                f"Database Error {ex}",
                status=status.HTTP_400_BAD_REQUEST
            )

