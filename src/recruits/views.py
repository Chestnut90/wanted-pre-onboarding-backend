from django.db.models import Q

from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action

from .serializers import (
    RecruitSimpleSerializer,
    RecruitDetailSerializer,
    RecruitCreateSerializer,
    ApplicationSerializer,
)

from .models import Recruit
from .permissions import IsManagerOrReadOnly, IsNotManagerOnlyOrReadOnly


class RecruitViewSet(ModelViewSet):

    permission_classes = [IsManagerOrReadOnly]
    serializer_class = RecruitSimpleSerializer
    pagination_class = PageNumberPagination
    queryset = Recruit.objects.all()

    def get_serializer_class(self):

        if self.action in ["retrieve"]:
            return RecruitDetailSerializer
        elif self.action in ["create", "update", "partial_update"]:
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
        permission_classes=[IsNotManagerOnlyOrReadOnly],
    )
    def application(self, request, pk):
        request.data["user"] = self.request.user.pk
        request.data["recruit"] = pk
        return self.create(request)
