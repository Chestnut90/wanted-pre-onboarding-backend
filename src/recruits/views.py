from django.shortcuts import render
from django.db.models import Q

from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import (
    RecruitSimpleSerializer,
    RecruitDetailSerializer,
    RecruitCreateSerializer,
    ApplicationSerializer,
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

    @action(
        methods=["post"],
        detail=True,
        url_path=r"application",
        url_name="application",
        serializer_class=ApplicationSerializer,
    )
    def application(self, request, pk):
        request.data["user"] = self.request.user.pk
        request.data["recruit"] = pk
        return self.create(request)

        # serializer = self.get_serializer(
        #     data={
        #         "user": self.request.user.pk,
        #         "recruit": Recruit.objects.get(id=pk).pk,
        #     }
        # )
        # serializer.is_valid(raise_exception=True)

        # self.perform_create(serializer)

        return Response(data=serializer.data)
