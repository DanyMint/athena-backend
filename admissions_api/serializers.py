from rest_framework import serializers

from admissions.models import (
    Quota,
    Specialty,
    LanguageOfStudy,
    PreviousPlaceOfStudyType,
    Entrant,
    Nationality,
    CitizenshipList
)


class QuotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quota
        fields = ("id", "name", "description")


class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ("id", "name", "code")


class LanguageOfStudySerializer(serializers.ModelSerializer):
    class Meta:
        model = LanguageOfStudy
        fields = ("id", "name")


class PreviousPlaceOfStudyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreviousPlaceOfStudyType
        fields = ("id", "name")


class EntrantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entrant
        fields = "__all__"

    citizenship = serializers.SlugRelatedField(
        slug_field="name",
        queryset=CitizenshipList.objects.all()
    )

    nationality = serializers.SlugRelatedField(
        slug_field="name",
        queryset=Nationality.objects.all()
    )

    quota = serializers.SlugRelatedField(
        many=True,
        slug_field="name",  # Поле в модели Quota, которое будет использоваться для сериализации
        queryset=Quota.objects.all()
    )

    specialty = serializers.SlugRelatedField(
        slug_field='name',  # Для ForeignKey связей используем `name` из Specialty
        queryset=Specialty.objects.all()
    )

    previous_place_of_study_type = serializers.SlugRelatedField(
        slug_field='name',
        queryset=PreviousPlaceOfStudyType.objects.all()
    )

    language_of_study = serializers.SlugRelatedField(
        slug_field='name',
        queryset=LanguageOfStudy.objects.all()
    )


class CitizenshipListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CitizenshipList
        fields = "__all__"


class NationalityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nationality
        fields = "__all__"
