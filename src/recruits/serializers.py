from rest_framework.serializers import (
    ModelSerializer,
    PrimaryKeyRelatedField,
    SerializerMethodField,
    ValidationError,
)

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
    other_recruits = SerializerMethodField()

    class Meta:
        model = Recruit
        fields = "__all__"

    def get_other_recruits(self, obj):
        return [
            r.pk for r in Recruit.objects.filter(company=obj.company) if r.pk != obj.pk
        ]


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

    def validate(self, attrs):

        user = attrs["user"]
        recruit = attrs["recruit"]
        try:
            Application.objects.get(user=user, recruit=recruit)
            raise ValidationError("already submitted recruit.")
        except Application.DoesNotExist:
            # no error
            pass
        return super().validate(attrs)
