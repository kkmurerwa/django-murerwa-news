from django.db.models import Exists, OuterRef, Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.models import Article
from articles.serializers import ArticleSerializer


@api_view(['GET', 'POST'])
def articles(request):
    if request.method == 'GET':
        # Get all articles
        articles_list = Article.objects.all()

        # Serialize them
        serializer = ArticleSerializer(articles_list, many=True)

        return Response(
            {
                "success": True,
                "message": "Articles returned successfully",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )
    elif request.method == 'POST':
        # Create a serializer
        serializer = ArticleSerializer(data=request.data)

        # Add the data to db
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Article added successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        else:
            missing_keys = list(serializer.errors.keys())

            return Response(
                {
                    "success": False,
                    "message": f"Could not create article because required field(s) {missing_keys} are missing",
                    "data": None
                },
                status=status.HTTP_400_BAD_REQUEST
            )
    else:
        return Response(
            {
                "success": False,
                "message": "Method not allowed",
                "data": None
            },
            status.HTTP_405_METHOD_NOT_ALLOWED
        )


@api_view(['GET'])
def search_article(request):
    if request.method == 'GET':
        # Get the search query
        search_query = request.GET.get('query', '')

        # Get all articles that match the search query
        queryset = Article.objects.filter(
            Q(title__icontains=search_query) | Q(body__icontains=search_query)
        )

        # Serialize the results of the query
        serializer = ArticleSerializer(queryset, many=True)

        return Response(
            {
                "success": True,
                "message": "Articles returned successfully",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )
    else:
        return Response(
            {
                "success": False,
                "message": "Method not allowed",
                "data": None
            },
            status.HTTP_405_METHOD_NOT_ALLOWED
        )


@api_view(['GET', 'PATCH', 'DELETE'])
def article(request, id):

    # Get the article
    try:
        # Try to get the current article
        current_article = Article.objects.get(id=id)
    except Article.DoesNotExist:
        return Response(
            {
                "success": False,
                "message": "Article does not exist",
                "data": None
            },
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        # Serialize the article
        serializer = ArticleSerializer(current_article)

        return Response(
            {
                "success": True,
                "message": "Article returned successfully",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

    elif request.method == 'PATCH':
        # Serialize the article
        serializer = ArticleSerializer(current_article, data=request.data)

        # Check if data is valid
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Article updated successfully",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )
        else:
            missing_keys = list(serializer.errors.keys())

            return Response(
                {
                    "success": False,
                    "message": f"Could not update article because required field(s) {missing_keys} are missing",
                    "data": None
                },
                status=status.HTTP_400_BAD_REQUEST
            )
    elif request.method == 'DELETE':
        current_article.delete()

        return Response(
            {
                "success": True,
                "message": "Article deleted successfully",
                "data": None
            },
            status=status.HTTP_200_OK
        )
    else:
        return Response(
            {
                "success": False,
                "message": "Method not allowed",
                "data": None
            },
            status.HTTP_405_METHOD_NOT_ALLOWED
        )