from django.shortcuts import render
from django.db.models import Q

from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .serializers import (
    RecruitSimpleSerializer,
    RecruitDetailSerializer,
    RecruitCreateSerializer,
)

from .models import Recruit


class RecruitViewSet(ModelViewSet):

    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = RecruitSimpleSerializer
    pagination_class = PageNumberPagination
    queryset = Recruit.objects.all()

    def get_serializer_class(self):

        if self.action in ["retrieve", "update", "partial_update"]:
            return RecruitDetailSerializer
        elif self.action == "create":
            return RecruitCreateSerializer

        return super().get_serializer_class()

    def get_queryset(self):

        skill = self.request.query_params.get("skill", "")
        position = self.request.query_params.get("position", "")
        return Recruit.objects.filter(
            Q(skill__contains=skill) & Q(position__contains=position)
        )
