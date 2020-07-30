from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from django.core.exceptions import *


class AllArticleList(APIView):
    def get(self, request):
        model = Article.objects.all()
        serializer = ArticleSerializer(model, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AllArticleDetails(APIView):
    def get(self, request, ids):
        if not self.exceptionFun(ids):
            return Response(f"User with {ids} is Not Found  in database", status=status.HTTP_404_NOT_FOUND)
        serializer = ArticleSerializer(self.exceptionFun(ids))
        return Response(serializer.data)

    def put(self, request, ids):
        if not self.exceptionFun(ids):
            return Response(f"User with {ids} is Not Found  in database", status=status.HTTP_404_NOT_FOUND)
        serializer = ArticleSerializer(self.exceptionFun(ids), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, ids):
        if not self.exceptionFun(ids):
            return Response(f"User with {ids} is Not Found  in database", status=status.HTTP_404_NOT_FOUND)
        model = self.exceptionFun(ids)
        model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def exceptionFun(self, ids):
        try:
            model = Article.objects.get(id=ids)
            return model
        except ObjectDoesNotExist:
            return
