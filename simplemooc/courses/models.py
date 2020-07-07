from django.db import models
from django.conf import settings

from core.mail import send_mail_template

class CourseManager(models.Manager):

    # Quando chamar essa função fará uma pesquisa pelo nome e descrição
    def search(self, query):
        # Vai pegar os dados do banco e filtra-los
        return self.get_queryset().filter(
            # Faz o filtro com or(se colocar a virgula é and)
            models.Q(name__icontains = query) | \
            models.Q( description__icontains=query)
            
        )


class Course(models.Model):
    
    name = models.CharField('Nome', max_length=100)
    slug = models.SlugField('Atalho')
    description = models.TextField('Descrição', blank=True)
    about = models.TextField('Sobre o curso', blank = True)
    start_date = models.DateField(
        'Data de inicio', null=True, blank=True
    )

    image = models.ImageField(
        upload_to='courses/images', verbose_name='Imagem',
        null=True, blank=True
    )

    created_at = models.DateField(
        'Criado em', auto_now_add=True
    )

    updated_at = models.DateField(
        'Atualizado em', auto_now = True
    )

    # Atrai ao objects o Manager customizado ao invés do padrão
    objects = CourseManager()

    def __str__(self):
        return self.name
        
    # Metodo para pegar url 
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("courses:details", kwargs={"slug": self.slug})
    
    # Edições no admin
    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos' 
        ordering = ['name']

class Lesson(models.Model):
    name =models.CharField('Nome', max_length=100)
    description = models.TextField('Descrição', blank=True)
    number = models.IntegerField('Número(ordem)', blank=True, default=0)
    release_date = models.DateField('Data de Liberação', blank=True, null=True)

    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    course = models.ForeignKey(Course, verbose_name='Curso', related_name='lessons', on_delete = models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Aula'
        verbose_name_plural = 'Aulas'
        ordering = ['number']

class Material(models.Model):

    name = models.CharField('Nome', max_length=100)
    embedded = models.TextField('Video Embedded', blank=True)
    file = models.FileField(upload_to='lessons/materials', blank=True, null=True)

    lesson = models.ForeignKey(Lesson, verbose_name='Aula', related_name='materials', on_delete=models.CASCADE)
    
    def is_embedded(self):
        return bool(self.embedded)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Material'
        verbose_name_plural = 'Materiais'




class Enrollment(models.Model):

    # Atribui um numero para cada opção de status
    STATUS_CHOICES = (
        (0, 'Pendente'),
        (1, 'Aprovado'),
        (2, 'Cancelado')
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Usuário', 
        # related_name faz a relação com o usuario
        related_name='enrollments', on_delete=models.CASCADE,
    )
    course = models.ForeignKey(
        Course, verbose_name='Curso',
        # related_name faz a relação com o curso
        related_name='enrollments', on_delete=models.CASCADE
    )
    status = models.IntegerField('Situação', choices=STATUS_CHOICES,
        default = 0,
        blank = True,
    )

    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    def active(self):
        self.status = 1
        self.save()
    
    def is_approved(self):
        self.status = 1
        self.save()


    class Meta:
        verbose_name = 'Inscrição'
        verbose_name_plural = 'Incrições'
        # Faz com que o usuário possa se cadastrar em apenas um curso
        unique_together = (('user', 'course'),)

class Announcement(models.Model):
    course = models.ForeignKey(Course, verbose_name = 'Curso', related_name='announcements', on_delete = models.CASCADE)
    title = models.CharField('Título', max_length=100)
    content = models.TextField('Conteudo')
    
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Anúncio'
        verbose_name_plural = 'Anúncios'
        ordering = ['-created_at']

# Função dos comentários
class Comment(models.Model):
    announcement = models.ForeignKey(
        # related_name uma instancia do anuncio terá uma relação chamada comments que trás o s comentários
        Announcement, verbose_name='Anúncio', related_name='comments', on_delete = models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Usuário', on_delete = models.CASCADE)
    comment = models.TextField('Comentário')
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'
        ordering = ['created_at']

# Função para disparar email
def post_save_announcement(instance, created, **kwargs):
    if created:
        subject = instance.title
        context = {
            'announcement': instance
        }
        template_name = 'courses/announcement_mail.html'
        # Pega todos os usuarios que estão aprovados no curso
        enrollments = Enrollment.objects.filter(
            course=instance.course, status=1)
        
        # Pega os usuários e então realiza o envio dos email
        for enrollment in enrollments:
            recipient_list = [enrollment.user.email]
            send_mail_template(subject, template_name, context, recipient_list)

    # Função que vai ser enviada, só será enviada pelo
models.signals.post_save.connect(
    post_save_announcement, sender=Announcement,
    dispatch_uid='post_save_announcement'
)

