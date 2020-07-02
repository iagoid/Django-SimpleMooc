from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, SetPasswordForm
from django.conf import settings
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from core.utils import generate_hash_key
from django.contrib import messages
from courses.models import Enrollment

from .forms import RegisterForm, EditAccountForm, PasswordResetForm
from .models import PasswordReset

User = get_user_model()

@login_required
def dashboard(request):
    template_name = 'accounts/dashboard.html'
    context = {}
    return render(request, template_name)



def register(request):
    template_name = 'registration/register.html'

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            # Atribui ao user o username e senha(antes da criptografia)
            user = authenticate(username=user.username, password=form.cleaned_data['password1'])
            # Faz o login automatico
            login(request, user)
            return redirect('core:home')

    else:
        form = RegisterForm()

    context = {
        'form': form
    }

    return render(request, template_name, context)

def password_reset(request):
    template_name='accounts/password_reset.html'
    context = {}
    # Ao ser requisitado o valor pega o valor do formulário 
    # Quando não é requisitado pega o valor None
    form = PasswordResetForm(request.POST or None)
    if form.is_valid():
        form.save()
        context['success'] = True
    context['form'] = form
    
    return render(request, template_name, context)
 
def password_reset_confirm(request, key):
    template_name = 'accounts/password_reset_confirm.html'
    context = {}
    reset = get_object_or_404(PasswordReset, key=key)
    form = SetPasswordForm(user=reset.user, data = request.POST or None)
    if form.is_valid():
        form.save()
        context['success'] = True
    context['form'] = form
    return render(request, template_name, context)

@login_required
def edit(request):
    template_name= 'accounts/edit.html'
    context = {}
    if request.method == 'POST':
        # Atribui ao post os dados do usuário logado
        form = EditAccountForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Os dados da sua conta foram alterados com sucesso')
            return redirect('accounts:dashboard')
    else:
        form = EditAccountForm(instance=request.user)
    context['form'] = form
    return render(request, template_name, context)

@login_required
def edit_password(request):
    template_name = 'accounts/edit_password.html'
    context = {}
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            context['success'] = True

    else:
        form = PasswordChangeForm(user=request.user)
    context['form'] = form
    return render(request, template_name, context)


