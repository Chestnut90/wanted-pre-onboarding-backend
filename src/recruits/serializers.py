from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from .models import Company, Recruit, Application


class CompanySerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"


class RecruitSimpleSerializer(ModelSerializer):

    company = CompanySerializer(read_only=True)

    class Meta:
        model = Recruit
        fields = (
            "pk",
            "title",
            "company",
            "skill",
            "position",
        )


class RecruitDetailSerializer(ModelSerializer):
    company = CompanySerializer(read_only=True)

    # TODO : method field for other recruits

    class Meta:
        model = Recruit
        fields = "__all__"


class RecruitCreateSerializer(ModelSerializer):
    company = PrimaryKeyRelatedField(
        label="primary key of company", queryset=Company.objects.all()
    )

    class Meta:
        model = Recruit
        fields = (
            "title",
            "company",
            "skill",
            "position",
            "description",
        )


class ApplicationSerializer(ModelSerializer):
    class Meta:
        model = Application
        fields = "__all__"
