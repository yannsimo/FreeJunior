from typing import List

from FreeJuniorapp1.models import Student, Specialty

student_speciality_all = Specialty(name='All')

def get_speciality_Student(speciality_name):
    student = Student.objects.all()
    if speciality_name == student_speciality_all.slug():
        specialty_std = student_speciality_all
    else:
        try:
            specialty_std = Specialty.objects.get(name__iexact=speciality_name)
            student = student.filter(specialty=specialty_std)
        except Specialty.DoesNotExist:
            specialty_std = Specialty(name=speciality_name)
            student = Student.objects.none()

    student = student.order_by('hourly_rate')
    return specialty_std, student

def get_speciality():
    specialities = list(Specialty.objects.all().order_by('name'))
    return specialities