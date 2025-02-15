from django.db import models


# Create your models here.
class Quota(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=350)
    objects = models.Manager()

    def __str__(self):
        return self.name


class LanguageOfStudy(models.Model):
    name = models.CharField(max_length=20, unique=True)
    objects = models.Manager()

    def __str__(self):
        return self.name


class Specialty(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=50)
    objects = models.Manager()

    def __str__(self):
        return self.name


class PreviousPlaceOfStudyType(models.Model):
    name = models.CharField(max_length=30, unique=True)
    objects = models.Manager()

    def __str__(self):
        return self.name


class CitizenshipList(models.Model):
    name = models.CharField(max_length=100, unique=True)
    objects = models.Manager()

    def __str__(self):
        return self.name


class Nationality(models.Model):
    name = models.CharField(max_length=100, unique=True)
    objects = models.Manager()

    def __str__(self):
        return self.name


class Entrant(models.Model):
    GENDER_CHOICES = {'М': "Мужчина", "Ж": "Женщина"}
    STUDY_FORMAT_CHOICES = {"Очное обучение": "Очное обучение", "Заочное обучение": "Заочное обучение"}

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    patronymic = models.CharField(max_length=150, default="")
    birth_date = models.DateTimeField("birth date")
    individual_identical_number = models.CharField(max_length=50, default="")
    quota = models.ManyToManyField(Quota)
    language_of_study = models.ForeignKey(LanguageOfStudy, on_delete=models.SET_NULL, null=True)
    on_the_budget = models.BooleanField(default=1)
    previous_place_of_study_type = models.ForeignKey(PreviousPlaceOfStudyType, on_delete=models.SET_NULL, null=True)
    specialty = models.ForeignKey(Specialty, on_delete=models.SET_NULL, null=True)
    citizenship = models.ForeignKey(CitizenshipList, on_delete=models.SET_NULL, null=True)
    nationality = models.ForeignKey(Nationality, on_delete=models.SET_NULL, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="")
    study_format = models.CharField(max_length=20, choices=STUDY_FORMAT_CHOICES, default="")

    objects = models.Manager()

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.patronymic}"
