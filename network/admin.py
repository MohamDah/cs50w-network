from django.contrib import admin

from .models import User, post, follow, likes

# Register your models here.
admin.site.register(User)
admin.site.register(post)
admin.site.register(follow)
admin.site.register(likes)