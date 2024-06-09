from audioop import reverse

from .FormsEtudiant import StudentRegistrationForm, EmailAuthenticationForm
from .FormsEntreprise import EntrepriseRegistrationForm
from .ContactForm import ContactForm
from FreeJuniorapp1 import navigation, model_helpers
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from FreeJuniorapp1.models import Student, Specialty, Comment
from django.core.mail import send_mail
from .CommentForm import CreateComment

def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print(form.instance)
    else:
        form = StudentRegistrationForm()

    context = {
        'navigation_items': navigation.navigation_items(navigation.NAV_FormStudent),
        'form': form
    }

    return render(request, 'FreeJuniorapp1/student_form.html', context)

def register_company(request):
    if request.method == 'POST':
        form = EntrepriseRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_url')
    else:
        form = EntrepriseRegistrationForm()

    context = {
        'navigation_items': navigation.navigation_items(navigation.NAV_FormCompany),
        'form': form
    }
    return render(request, 'FreeJuniorapp1/Entreprise_form.html', context)

def login_view(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Vous êtes maintenant connecté en tant que {email}.")
                return redirect(reverse('edit_student_profile', kwargs={'pk': user.pk}))
            else:
                messages.error(request, "Email ou mot de passe incorrect.")
        else:
            messages.error(request, "Email ou mot de passe incorrect.")
    else:
        form = EmailAuthenticationForm()
    return render(request, 'login/login.html', {'form': form})

def student_list(request, speciality_name=model_helpers.student_speciality_all.slug()):
    speciality, students = model_helpers.get_speciality_Student(speciality_name)
    specialities = model_helpers.get_speciality()
    context = {
        'specialities': specialities,
        'students': students,
        'speciality': speciality,
        'navigation_items': navigation.navigation_items(navigation.NAV_FormListStudent),
    }
    return render(request, 'FreeJuniorapp1/student_list.html', context)

def student_detail(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    comments = student.comments.exclude(status=Comment.STATUS_HIDDEN).order_by('created_at')


    if request.method == 'POST':
        comment_form = CreateComment(request.POST)
        form = ContactForm(request.POST)
        if form.is_valid():
            your_name = form.cleaned_data['your_name']
            your_email = form.cleaned_data['your_email']
            message = form.cleaned_data['message']
            subject = f"Message de {your_name} via FreeJunior"
            email_message = f"De: {your_name}\nEmail: {your_email}\n\nMessage:\n{message}"
            try:
                send_mail(subject, email_message, your_email, [student.email])
                messages.success(request, "Votre message à été envoyé")
            except Exception as e:
                messages.error(request,f"une erreur s'est produite")

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.student=student
            comment.save()
            messages.success(request, "Votre commentaire a été ajouté avec succès.")
    else:
        comment_form = CreateComment()
        form = ContactForm()


    context = {
        'student': student,
        'form': form,
        'comments': comments,
        'comment_form': comment_form
    }
    return render(request, 'FreeJuniorapp1/student_detail.html', context)


def edit_student_profile(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_detail', pk=student.pk)
    else:
        form = StudentRegistrationForm(instance=student)

    context = {
        'form': form,
        'student': student
    }
    return render(request, 'FreeJuniorapp1/edit_student_profile.html', context)