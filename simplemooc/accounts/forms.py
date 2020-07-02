from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from core.utils import generate_hash_key
from core.mail import send_mail_template

from .models import PasswordReset

User = get_user_model()

class PasswordResetForm(forms.Form):
    email = forms.EmailField(label='Email')
    
    def clean_email(self):
        email = self.cleaned_data['email']
        # Faz a verificação se o email existe
        if User.objects.filter(email=email).exists():
            return email
        raise forms.ValidationError(
            'Nenhum usuário encontrado com este email'
        )

    def save(self):
        user = User.objects.get(email = self.cleaned_data['email'])
        key = generate_hash_key(user.username)
        reset = PasswordReset(key=key, user=user)
        reset.save()
        template_name = 'accounts/password_reset_mail.html'
        context = {
            'reset': reset,
        }
        subject = 'Criar Nova senha no SIMPLE MOOC'
        send_mail_template(subject, template_name, context, [user.email])

# Utiliza o form padrão UserCreationForm e adiciona à ele o campo email
class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Senha', widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Confirmação de Senha', widget=forms.PasswordInput
    )
    # Faz a verificação das senhas, se elas foram enviadas e se são iguais
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('A confirmação não está correta')
        return password2

    # substitui o save padrão de UserCreationForm
    def save(self, commit=True):
        # Chama o super para validar os campos user e password, mas não salva
        user = super(RegisterForm, self).save(commit = False)
        # Criptografa a senha
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

    # Pega o Model definido no models.py e seus campos para o registro
    class Meta:
        model = User
        fields = ['username', 'email']


class EditAccountForm(forms.ModelForm):

    # Qual model ele vai pegar e seus campos
    class Meta:
        model = User
        fields = ['username', 'email', 'name']

