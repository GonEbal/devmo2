from django.contrib import admin

from .models import User, Publication, User_followers, Categories
# Register your models here.

admin.site.register(User)
admin.site.register(Publication)
admin.site.register(User_followers)
admin.site.register(Categories)