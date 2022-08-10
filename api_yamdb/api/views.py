from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from Reviews.models import Comment, Review

from .permissions import OwnerCheck
from .serializers import (CommentSerializer, ReviewSerializer)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (OwnerCheck,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        return Review.objects.filter(title_id=title_id)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (OwnerCheck,)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        title_id = self.kwargs.get('title_id')
        return Comment.objects.filter(
            title_id=title_id, review_id=review_id
        )

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        serializer.save(
            author=self.request.user,
            review_id=get_object_or_404(Review, review_id=review_id)
        )
