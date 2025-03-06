from django.urls import path

from admissions_api.views import (
    QuotaListCreate,
    QuotaReadUpdateDelete,
    SpecialtyListCreate,
    SpecialtyReadUpdateDelete,
    LangOfStudyListCreate,
    LangOfStudyReadUpdateDelete,
    PreviousPlaceOfStudyTypeReadUpdateDelete,
    PreviousPlaceOfStudyTypeListCreate,
    EntrantListCreate,
    EntrantReadUpdateDelete,
    NationalityListCreate,
    NationalityReadUpdateDelete,
    CitizenshipListCreate,
    CitizenshipReadUpdateDelete,
    get_csv_report
)

app_name = 'admissions_api'

urlpatterns = [
    path('quotas', QuotaListCreate.as_view(), name='quota_getlist_create'),
    path('quotas/<int:pk>', QuotaReadUpdateDelete.as_view(), name='quota_detail_delete_update'),

    path('specialties', SpecialtyListCreate.as_view(), name="specialty_list_create"),
    path('specialties/<int:pk>', SpecialtyReadUpdateDelete.as_view(), name="specialty_detail_delete_update"),

    path('langs_of_study', LangOfStudyListCreate.as_view(), name="langs_of_study_list_create"),
    path('langs_of_study/<int:pk>', LangOfStudyReadUpdateDelete.as_view(), name="lang_of_study_detail_delete_update"),

    path('previous_place_of_study_types', PreviousPlaceOfStudyTypeListCreate.as_view(),
         name="previous_place_of_study_types_list_create"),
    path('previous_place_of_study_types/<int:pk>', PreviousPlaceOfStudyTypeReadUpdateDelete.as_view(),
         name="previous_place_of_study_type_detail_delete_update"),

    path('entrants', EntrantListCreate.as_view(), name="entrant_list_create"),
    path('entrants/<int:pk>', EntrantReadUpdateDelete.as_view(), name="entrant_detail_delete_update"),

    path('nationalities', NationalityListCreate.as_view(), name="nationality_list_create"),
    path('nationalities/<int:pk>', NationalityReadUpdateDelete.as_view(), name="nationality_detail_delete_update"),

    path('citizenships', CitizenshipListCreate.as_view(), name="citizenship_list_create"),
    path('citizenships/<int:pk>', CitizenshipReadUpdateDelete.as_view(), name="citizenship_detail_delete_update"),

    path('get_report_csv', get_csv_report, name="get_report_csv"),
]
