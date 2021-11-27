
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from movies.permissions import OnlyAdmin, OnlyCritico

from .models import Movie, Review
from .serializers import (CreateReviewSerializer, MovieDetailSerializer,
                          MovieSerializer, ReviewSerializer)


class MovieViews(ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, OnlyAdmin]
    authentication_classes = [TokenAuthentication]

    def filter_queryset(self, queryset):
        if 'title' in self.request.GET:
            return queryset.filter(title__contains=self.request.GET['title'])
        return queryset

    def retrieve(self, request, *args, **kwargs):
        user = self.request.user
        movie = get_object_or_404(Movie, id=kwargs.get('pk'))

        if user.is_anonymous:
            serialized = MovieSerializer(movie)
            return Response(serialized.data)
        serialized_detail = MovieDetailSerializer(movie)
        return Response(serialized_detail.data)

    @action(detail=True, methods=['post', 'put'], permission_classes=[OnlyCritico],
            serializer_class=CreateReviewSerializer, url_path='review')
    def create_review(self, request,  *args, **kwargs):
        user = request.user

        if user.is_superuser:
            return Response({'error': 'Only the critic can create a review'},
                            status=status.HTTP_403_FORBIDDEN)

        movie = get_object_or_404(Movie, id=kwargs.get('pk'))

        if request.method == 'POST':
            serializer = CreateReviewSerializer(data=request.data)
            validated_data = serializer.is_valid(raise_exception=True)

            if movie.reviews.filter(critic_id=user.id).exists():
                return Response({"detail": "You already made this review."},
                                status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            validated_data = serializer.validated_data

            review = Review.objects.create(
                **validated_data, critic=user, movie=movie)

            serialized = CreateReviewSerializer(review)

            return Response(serialized.data, status=status.HTTP_201_CREATED)

        if request.method == 'PUT':
            try:
                movie = get_object_or_404(Movie, id=kwargs.get('pk'))

                review = movie.reviews.get(critic_id=user.id)

                partial = kwargs.pop('partial', False)
                instance = review

                serializer = CreateReviewSerializer(
                    instance, data=request.data, partial=partial)
                serializer.is_valid(raise_exception=True)
                serializer.save()

                return Response(serializer.data)

            except Review.DoesNotExist:
                return Response({'error': 'Review does not exist'},
                                status=status.HTTP_404_NOT_FOUND)


class ListReview(ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [OnlyCritico]

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def list(self, request, *args, **kwargs):
        user = request.user

        if not user.is_staff and not user.is_superuser:
            return Response({'detail': 'You do not have permission to perform this action.'},
                            status=status.HTTP_403_FORBIDDEN)

        if user.is_superuser:
            queryset = Review.objects.all()
        else:
            queryset = Review.objects.filter(critic_id=user.id)
        paginator = PageNumberPagination()
        page = paginator.paginate_queryset(queryset, request=request.data)
        if page is not None:
            serializer = ReviewSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = ReviewSerializer(queryset, many=True)
        return Response(serializer.data)
