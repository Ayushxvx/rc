from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Usertype)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Dislike)
admin.site.register(Comment)
admin.site.register(Ticket)
admin.site.register(Subscription)