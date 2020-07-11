from django.contrib import admin
from .models import Thread, Reply

class ThreadAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created', 'modified']
    search_fields = ['title', 'author', 'email', 'body']
    prepopulated_fields = {'slug': ('title', )}

class ReplyAdmin(admin.ModelAdmin):
    list_display = ['author', 'correct','reply']
    search_fields = ['author', 'email', 'reply']

 
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Reply, ReplyAdmin)
