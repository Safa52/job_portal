from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from contact.views import contact_view

from .views import *

app_name = "contact"

urlpatterns = [
    path("contact/", contact_view.as_view(), name="contact"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)