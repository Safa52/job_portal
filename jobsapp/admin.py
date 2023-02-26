from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage

# Register your models here.
from jobsapp.models import Job, Applicant


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "salary",
        "location",
        "type",
        "category",
        "last_date",
        "created_at",
        "filled",
        "user",
    ]
    list_filter = ["salary", "last_date", "created_at", "user"]
    date_hierarchy = "created_at"


@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "job",
        "created_at",
        "comment",
        "status",
       
    ]
    list_filter = [ "created_at"]
    date_hierarchy = "created_at"
