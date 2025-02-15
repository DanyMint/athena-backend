from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework.decorators import api_view
from admissions.tools.report import get_report
from django.http import HttpResponse
from django.db.utils import OperationalError
import psycopg
from rest_framework.response import Response
from rest_framework import  status
from core.logger import logger

from admissions.models import (
    Quota,
    Specialty,
    LanguageOfStudy,
    PreviousPlaceOfStudyType,
    Entrant,
    Nationality,
    CitizenshipList
)
from .paginations import EntrantsSetPagination, DirectoryManagmentSetPagination
from .serializers import (
    QuotaSerializer,
    SpecialtySerializer,
    LanguageOfStudySerializer,
    PreviousPlaceOfStudyTypeSerializer,
    EntrantSerializer,
    CitizenshipListSerializer,
    NationalityListSerializer
)


class QuotaListCreate(generics.ListCreateAPIView):
    queryset = Quota.objects.all()
    serializer_class = QuotaSerializer
    pagination_class = DirectoryManagmentSetPagination

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['name', 'description']
    search_fields = ['name', 'description']


class QuotaReadUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quota.objects.all()
    serializer_class = QuotaSerializer


class SpecialtyListCreate(generics.ListCreateAPIView):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer
    pagination_class = DirectoryManagmentSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['name', 'code']
    search_fields = ['name', 'code']


class SpecialtyReadUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer


class LangOfStudyListCreate(generics.ListCreateAPIView):
    queryset = LanguageOfStudy.objects.all()
    serializer_class = LanguageOfStudySerializer
    pagination_class = DirectoryManagmentSetPagination

    filter_backends = [SearchFilter]
    search_fields = ['name']


class LangOfStudyReadUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = LanguageOfStudy.objects.all()
    serializer_class = LanguageOfStudySerializer


class PreviousPlaceOfStudyTypeListCreate(generics.ListCreateAPIView):
    queryset = PreviousPlaceOfStudyType.objects.all()
    serializer_class = PreviousPlaceOfStudyTypeSerializer
    pagination_class = DirectoryManagmentSetPagination

    filter_backends = [SearchFilter]
    search_fields = ['name']


class PreviousPlaceOfStudyTypeReadUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = PreviousPlaceOfStudyType.objects.all()
    serializer_class = PreviousPlaceOfStudyTypeSerializer


class BaseListCreateView(generics.ListCreateAPIView):
    def handle_exception(self, exc):
        logger.info(f"Бляя {exc}")
        if isinstance(exc, (OperationalError, psycopg.OperationalError)):
            logger.error(exc)
            return Response(
                {'error': "У нас возникли технические шоколадки"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        return super().handle_exception(exc)


class EntrantListCreate(generics.ListCreateAPIView):
    queryset = Entrant.objects.all()
    serializer_class = EntrantSerializer
    pagination_class = EntrantsSetPagination

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['quota', 'specialty']
    search_fields = ['individual_identical_number', 'first_name', 'last_name']


class EntrantReadUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Entrant.objects.all()
    serializer_class = EntrantSerializer


class CitizenshipListCreate(generics.ListCreateAPIView):
    queryset = CitizenshipList.objects.all()
    serializer_class = CitizenshipListSerializer
    pagination_class = DirectoryManagmentSetPagination

    filter_backends = [SearchFilter]
    search_fields = ['name']


class CitizenshipReadUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = CitizenshipList.objects.all()
    serializer_class = CitizenshipListSerializer


class NationalityReadUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Nationality.objects.all()
    serializer_class = NationalityListSerializer


class NationalityListCreate(generics.ListCreateAPIView):
    queryset = Nationality.objects.all()
    serializer_class = NationalityListSerializer
    pagination_class = DirectoryManagmentSetPagination
   
    filter_backends = [SearchFilter]
    search_fields = ['name']


@api_view(["GET"])
def get_csv_report(reuqest):
    csv_file_value = get_report().getvalue()

    response = HttpResponse(csv_file_value, content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="report.csv"'

    return response
