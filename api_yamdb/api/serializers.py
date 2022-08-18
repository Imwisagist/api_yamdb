from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueValidator

from reviews.models import (Category, Comment, Genre, Review,
                            Title, User)


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        min_length=3,
        max_length=30,
        validators=[UniqueValidator(queryset=User.objects.all())],
        required=True,
    )
    email = serializers.EmailField(
        max_length=30,
        validators=[UniqueValidator(queryset=User.objects.all())],
        required=True,
    )

    class Meta:
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")
        model = User


class UserEditSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        min_length=3, max_length=30, required=True
    )
    email = serializers.EmailField(
        max_length=30, required=True
    )
    first_name = serializers.CharField(min_length=2, max_length=50, )
    last_name = serializers.CharField(min_length=2, max_length=50, )
    bio = serializers.CharField(max_length=1000, )

    class Meta:
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")
        model = User
        read_only_fields = ('role',)


class RegisterDataSerializer(serializers.HyperlinkedModelSerializer):
    username = serializers.CharField(
        max_length=30, required=True
    )
    email = serializers.EmailField(
        max_length=30,
        required=True,
    )

    class Meta:
        fields = ("username", "email")
        model = User

    def validate_username(self, value):
        if value.lower() == "me":
            raise serializers.ValidationError("Username 'me' is not valid")
        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=30, required=True
    )
    confirmation_code = serializers.CharField(
        max_length=50, required=True
    )


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    title = SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        fields = '__all__'
        model = Review

    def validate(self, data):
        title_id = self.context.get('view').kwargs.get('title_id')
        request = self.context['request']
        if (request.method == 'POST'
           and Review.objects.filter(
            title=get_object_or_404(Title, pk=title_id),
                author=request.user).exists()):
            raise ValidationError('Вы уже писали ревью')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('review',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)


class TitleSerializerPost(serializers.ModelSerializer):
    category = SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    year = serializers.IntegerField(min_value=1, max_value=3000)

    class Meta:
        model = Title
        fields = '__all__'


class TitleSerializerGet(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = '__all__'
        read_only_fields = ('__all__',)
