from accounts.serializers import CriticSerializer
from rest_framework import serializers

from .models import Genre, Movie, Review


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)
    
    class Meta:
        model = Movie
        fields = '__all__'
        depth = 1

    def create(self, validated_data):
        genres = validated_data.pop('genres')

        movie = Movie.objects.create(
            **validated_data)

        for genre in genres:
            item = Genre.objects.get_or_create(
                name=genre['name'])[0]
            movie.genres.add(item)

        return movie

    def update(self, instance, validated_data):
        genres = validated_data.pop('genres')

        for genre in genres:
            item, create = Genre.objects.get_or_create(
                name=genre['name'])
            instance.genres.add(item)

        return super().update(instance, validated_data)


class ReviewSerializer(serializers.ModelSerializer):

    critic = CriticSerializer(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'

        extra_kwargs = {
            'stars': {'min_value': 1, 'max_value': 10},
        }


class CreateReviewSerializer(serializers.ModelSerializer):

    critic = CriticSerializer(read_only=True)

    class Meta:
        model = Review
        exclude = ['movie']

        extra_kwargs = {
            'stars': {'min_value': 1, 'max_value': 10}
        }

        depth = 1


class MovieDetailSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)
    reviews = CreateReviewSerializer(many=True, required=False)

    class Meta:
        model = Movie
        fields = '__all__'
        depth = 1

    def update(self, instance, validated_data):
        genres = validated_data.pop('genres')

        for genre in genres:
            item, create = Genre.objects.get_or_create(
                name=genre['name'])
            instance.genres.add(item)

        return super().update(instance, validated_data)
