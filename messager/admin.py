from django.contrib import admin
from registration.models import User
from .models import Profile, Message


class ProfileInline(admin.StackedInline):
    model = Profile


class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username "]
    inlines = [ProfileInline]


admin.site.register(User, UserAdmin)
admin.site.register(Message)
