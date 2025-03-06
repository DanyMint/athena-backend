from admissions.models import Entrant, PreviousPlaceOfStudyType, Quota
import csv
import io


def _get_count_entrants_by_filter(filters=None):
    if not filters:
        return Entrant.objects.count()  # count() быстрее, чем len(Entrant.objects.all())

    return Entrant.objects.filter(**filters).distinct().count()


def _get_rows_for_model(model, filters, filter_key_for_item, first_descriptions_part):
    items = model.objects.all()
    rows = []

    for item in items:
        filters[filter_key_for_item] = item

        rows.append([
            f"{first_descriptions_part} {item}",
            _get_count_entrants_by_filter(filters)
        ])

    return rows


def _get_report_data_list():
    all_entrants = _get_count_entrants_by_filter()

    all_study_base = _get_rows_for_model(PreviousPlaceOfStudyType, {}, "previous_place_of_study_type__name","На базе")
    on_the_budget = _get_count_entrants_by_filter({"on_the_budget": True})
    on_the_budget_with_base_rows = _get_rows_for_model(PreviousPlaceOfStudyType, {"on_the_budget": True}, "previous_place_of_study_type__name","На бюджет на базе")

    not_on_the_budget = _get_count_entrants_by_filter({"on_the_budget": False})
    not_on_the_budget_with_base_rows = _get_rows_for_model(PreviousPlaceOfStudyType, {"on_the_budget": False}, "previous_place_of_study_type__name","На бюджет на базе")

    study_on_kazak = _get_count_entrants_by_filter({"language_of_study__name": "Казахский"})
    study_on_kazak_with_base_rows = _get_rows_for_model(PreviousPlaceOfStudyType, {"language_of_study__name": "Казахский"}, "previous_place_of_study_type__name","На государственном языке на базе")

    study_on_kazak_day_format = _get_count_entrants_by_filter({"language_of_study__name": "Казахский", "study_format":"Очное обучение"})
    study_on_kazak_parttime_format = _get_count_entrants_by_filter({"language_of_study__name": "Казахский", "study_format":"Заочное обучение"})

    study_on_kazak_with_base_day_rows = _get_rows_for_model(PreviousPlaceOfStudyType, {"language_of_study__name": "Казахский", "study_format":"Очное обучение"}, "previous_place_of_study_type__name","На государственном языке на дневное обучение на базе")
    study_on_kazak_with_base_parttime_rows = _get_rows_for_model(PreviousPlaceOfStudyType, {"language_of_study__name": "Казахский", "study_format": "Заочное обучение"}, "previous_place_of_study_type__name","На государственном языке на заочное обучение на базе")

    entrants_with_quotas_rows = _get_rows_for_model(Quota, {}, "quota__name","С квотой: ")

    data_list = [
        ["Всего принято заявлений", all_entrants],
        ["Всего на бюджет", on_the_budget],
        ["Всего на платной основе", not_on_the_budget],
        ["Всего на государственном языке", study_on_kazak],
        ["Всего на государственном языке на дневное обучение", study_on_kazak_day_format],
        ["Всего на государственном языке на заочное обучение", study_on_kazak_parttime_format],
    ]

    data_list.extend( all_study_base )
    data_list.extend(on_the_budget_with_base_rows)
    data_list.extend(not_on_the_budget_with_base_rows)
    data_list.extend(study_on_kazak_with_base_rows)
    data_list.extend(study_on_kazak_with_base_day_rows)
    data_list.extend(study_on_kazak_with_base_parttime_rows)
    data_list.extend(entrants_with_quotas_rows)

    return data_list


def get_report():
    output = io.StringIO()
    writer = csv.writer(output)

    data = _get_report_data_list()

    writer.writerow(["Название", "Количество"])

    for row in data:
        writer.writerow(row)

    output.seek(0)
    return output


