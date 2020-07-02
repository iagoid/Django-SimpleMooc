from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Course, Enrollment
from .forms import ContactCourse


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

