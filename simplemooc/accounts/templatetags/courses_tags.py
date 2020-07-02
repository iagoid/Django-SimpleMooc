from django.template import Library

register = Library()

from courses.models import Enrollment

# Pega os cursos que o usuário está inscrito
# inclusion_tag converte para uma função que pode ser usada
@register.inclusion_tag('courses/templatetags/my_courses.html')
def my_courses(user):
    enrollments = Enrollment.objects.filter(user=user)
    context = {
        'enrollments': enrollments
    }
    return context


@register.simple_tag
def load_my_courses(user):
    return Enrollment.objects.filter(user=user)

