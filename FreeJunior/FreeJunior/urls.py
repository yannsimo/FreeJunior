"""
URL configuration for FreeJunior project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from FreeJuniorapp1 import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('page_company/', views.page_company, name='page_company'),
    path('page_etudiant/', views.page_etudiant, name='page_etudiant'),
    path('login/', views.login_view, name='login'),
    path('FreeJunior/FormulaireEtudiant/', views.register_student, name='student_form'),
    path('FreeJunior/FormulaireEntreprise/', views.register_company, name='company_form'),
    path('FreeJunior/Etudiants/', views.student_list, name='student_list'),
    path('FreeJunior/detail/<int:student_id>/', views.student_detail,name='student_detail'),
    path('FreeJunior/Etudiants/<str:speciality_name>/', views.student_list, name='student_list_filter'),
    path('student/<int:student_id>/contact/', views.student_detail, name='contact_student'),
    path('FreeJunior/etudiant/<int:pk>/modifier/', views.edit_student_profile, name='edit_student_profile'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)