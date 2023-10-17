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

    company = SerializerMethodField()  # replace object to string

    class Meta:
        model = Recruit
        fields = (
            "pk",
            "title",
            "company",
            "skill",
            "position",
        )

    def get_company(self, obj):
        return str(obj.company)


class RecruitDetailSerializer(ModelSerializer):
    company = SerializerMethodField()

    # TODO : method field for other recruits
    other_recruits = SerializerMethodField()

    class Meta:
        model = Recruit
        fields = "__all__"

    def get_company(self, obj):
        return str(obj.company)

    def get_other_recruits(self, obj):
        return [
            r.pk for r in Recruit.objects.filter(company=obj.company) if r.pk != obj.pk
        ]


class RecruitCreateSerializer(ModelSerializer):
    class Meta:
        model = Recruit
        fields = (
            "title",
            "skill",
            "position",
            "description",
        )
        read_only_fields = ("company",)

    def create(self, validated_data):
        validated_data["company"] = self.context["request"].user.company
        return super().create(validated_data)


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
