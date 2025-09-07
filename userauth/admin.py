from django.contrib import admin
from userauth.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'bio')
    search_fields = ('username', 'email')
    ordering = ('username',)

admin.site.register(User, UserAdmin)
# Register your models here.
