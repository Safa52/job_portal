from django.contrib import admin
from accounts.models import User
# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "email",
        "first_name",
        "last_name",
        "mobileno",
        "city",
        "qualification",
        "resume",
       
    ]
    list_filter = ["city"]
    