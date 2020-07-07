from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Course, Enrollment, Announcement
from .forms import ContactCourse, CommentForm
from .decorators import enrollment_required



def index(request):
    courses = Course.objects.all()
    template_name = 'courses/index.html'

    context = {
        'courses': courses
    }
    return render(request, template_name, context)

# def details(request, pk):
#     course = get_object_or_404(Course, pk=pk)
#     course = Course.objects.get(pk=pk)
#     context = {
#         'course': course
#     }
#     template_name = 'courses/details.html'
#     return render(request, template_name, context)

def details(request, slug):
    context = {}
    course = get_object_or_404(Course, slug=slug)
    course = Course.objects.get(slug=slug)
    if request.method == 'POST':
        form = ContactCourse(request.POST)
        if form.is_valid():
            context['is_valid'] = True
            print(form.cleaned_data)
            form.send_mail(course)
            form = ContactCourse()
    else:
        form = ContactCourse()
    context['course'] = course
    context['form'] = form

    template_name = 'courses/details.html'
    return render(request, template_name, context)

@login_required
def enrollment(request, slug):
    course = get_object_or_404(Course, slug=slug)
    # Retorna a inscrição
    # Se a incrição existia ele faz o GET, senão ele cria
    enrollment, created = Enrollment.objects.get_or_create(
        user=request.user, course=course
    )

    if created:
        # enrollment.active()
        messages.success(request, 'Inscrição realizada com sucesso')
    else:
        messages.info(request, 'Você já está incrito no curso')
    return redirect('accounts:dashboard')

# Cancelar inscrição no curo
@login_required
def undo_enrollment(request, slug):
    course = get_object_or_404(Course, slug=slug)
     #Retorna 404 caso o usuario não estiver inscrito no curso
    enrollment = get_object_or_404(
        Enrollment, user=request.user, course=course
    )
    if request.method == 'POST':
        enrollment.delete()
        messages.success(request, 'Sua inscrição foi cancelada com sucesso')
        return redirect('accounts:dashboard')
    template = 'courses/undo_enrollment.html'
    context = {
        'enrollment': enrollment,
        'course': course,
    }
    return render(request, template, context)


# Realizar inscrição no curso
@login_required
@enrollment_required
def announcements(request, slug):
    course = request.course
    template = 'courses/announcements.html'
    context = {
        'course': course,
        # Atribui todos os cursos ao pegar o course mo model
        'announcements': course.announcements.all()
    }
    return render(request, template, context)

@login_required
@enrollment_required
def show_announcement(request, slug, pk):
    course = request.course

    announcement = get_object_or_404(course.announcements.all(), pk=pk)

    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit = False)
        comment.user = request.user
        comment.announcement = announcement
        comment.save()
        form = CommentForm()
        messages.success(request, 'Seu comentário foi enviado.')

    template = 'courses/show_announcement.html'
    context = {
        'course': course,
        'announcement': announcement,
        'form': form
    }
    return render(request, template, context)
    
