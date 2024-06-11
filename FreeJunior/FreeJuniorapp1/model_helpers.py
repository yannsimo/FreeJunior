from django.shortcuts import render
from FreeJuniorapp1.models import Student, Specialty
from FreeJuniorapp1 import navigation


from django.db.models import Q

def get_speciality_Student(speciality_slug):
    if speciality_slug.lower() == 'all':
        students = Student.objects.all()
        specialty_std = None
    else:
        try:
            specialty_std = Specialty.objects.get(slug=speciality_slug)
            students = Student.objects.filter(specialty=specialty_std)
        except Specialty.DoesNotExist:
            students = Student.objects.none()
            specialty_std = None  # Aucune spécialité trouvée, on utilise None pour signaler l'absence de spécialité

    students = students.order_by('hourly_rate')
    return specialty_std, students

def get_speciality():
    specialities = list(Specialty.objects.all().order_by('name'))
    return specialities
