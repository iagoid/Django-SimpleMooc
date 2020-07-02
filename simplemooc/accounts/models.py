import re
from django.db import models
from django.core import validators
from django.contrib.auth.models import AbstractUser, PermissionsMixin, UserManager

from django.conf import settings


class User(AbstractUser, PermissionsMixin):
    username = models.CharField('Nome do usuário', max_length=30, unique = True,
    # Faz a validação de que caracteres o campo aceita
    validators=[validators.RegexValidator(re.compile('^[\w.@+-]+$'),
            'O nome de usuário só pode conter letras, digitos ou os '
            'seguintes caracteres: @/./+/-/_', 'invalid')]
    )
    email = models.EmailField('E-mail', unique=True)
    name = models.CharField('Nome', max_length=100, blank=True)
    # Campos já compativeis do Django
    is_active = models.BooleanField('Está Ativo?', blank=True, default=True)
    is_staff = models.BooleanField('É da equipe', blank=True, default=False)
    is_superuser = models.BooleanField('É da equipe', blank=True, default=False)
    date_joined = models.DateTimeField('Data de Entrada', auto_now_add=True)

    objects = UserManager()

    # Usado no campo de login 
    USERNAME_FIELD = 'username'
    # Usado no cadastro do usuário
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.name or self.username

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return str(self)

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
      

# Nova senha temporária
class PasswordReset(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Usuário', on_delete=models.CASCADE,
        #related_name='resets'
    )

    key = models.CharField('Chave', max_length=100, unique=True)
    created_at = models.DateField('Criado em: ', auto_now_add=True)
    confirmed = models.BooleanField('Confirmado', default=False, blank=True)

    def __str__(self):
        return '{0} - {1}'.format(self.user, self.created_at)

    class Meta:
        verbose_name = 'Nova Senha'
        verbose_name_plural = 'Novas Senhas'
        ordering = ['-created_at']
