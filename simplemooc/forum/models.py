from django.db import models
from django.conf import settings

from taggit.managers import TaggableManager

class Thread(models.Model):
    title = models.CharField('Título', max_length=100)
    slug = models.SlugField('Identificador', max_length=100, unique=True)
    body = models.TextField('Mensagem')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Autor', related_name='threads', on_delete=models.PROTECT,
    )
    views = models.IntegerField('Visualizações', blank=True, default=0)
    answers = models.IntegerField('Respostas', blank=True, default=0)

    tags = TaggableManager()

    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)


    def __str__(self):
        return self.title

    # Metodo para pegar url 
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("forum:thread", kwargs={"slug": self.slug})
    class Meta:
        verbose_name = 'Tópicos'
        verbose_name_plural = 'Tópicos'
        ordering = ['-modified']

    
class Reply(models.Model):
    thread = models.ForeignKey(
        Thread, verbose_name='Tópico', related_name='replies', on_delete = models.CASCADE
    )
    reply = models.TextField('Resposta')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Autor', related_name='replies', on_delete=models.PROTECT,
    )
    correct = models.BooleanField('Correta?', blank=True, default=False)


    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)

    def __str__(self):
        return self.reply

    class Meta:
        verbose_name = 'Resposta'
        verbose_name_plural = 'Respostas'
        ordering = ['-correct', 'created']


# Ao colocar uma resposta como correta todas as outras respostas recebem False
def post_save_reply(created, instance, **kwargs):
    instance.thread.answers = instance.thread.replies.count()
    instance.thread.save()
    if instance.correct:
        instance.thread.replies.exclude(pk=instance.pk).update(
            correct=False
        )

def post_delete_reply(instance, **kwargs):
    instance.thread.answers = instance.thread.replies.count()
    instance.thread.save()

models.signals.post_save.connect(
    post_save_reply, sender=Reply, dispatch_uid='post_save_reply'
)
models.signals.post_delete.connect(
    post_delete_reply, sender=Reply, dispatch_uid='post_delete_reply'
)