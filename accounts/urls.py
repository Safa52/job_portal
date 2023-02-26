from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from jobsapp.views import EditProfileView, EmployerProfileEditView

from .views import *

app_name = "accounts"

urlpatterns = [
     path("searchcompany/", SearchcompanyView.as_view(), name="searchcompany"),
    path("employee/register/", RegisterEmployeeView.as_view(), name="employee-register"),
    path("employer/register/", RegisterEmployerView.as_view(), name="employer-register"),
    path("employer/<int:id>/",  JobCompanyView.as_view(), name="employer-company"),
    path("employee/profile/update/", EditProfileView.as_view(), name="employee-profile-update"),
    path("employer/profile/update/", EmployerProfileEditView.as_view(), name="employer-profile-update"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("login/", LoginView.as_view(), name="login"),
    path("companysearch/", CompanyListView.as_view(), name="companylist"),
    path("companysearch/<int:id>", Viewalljobs.as_view(), name="viewcompanyjobs"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
