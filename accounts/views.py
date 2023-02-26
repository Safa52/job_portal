from pyexpat import model
from django.contrib import auth, messages
from django.http import HttpResponseRedirect,Http404
from django.shortcuts import redirect, render
from django.views.generic import CreateView, FormView, RedirectView,DetailView,ListView
from accounts.forms import *
from accounts.models import User
from jobsapp.models import *



class RegisterEmployeeView(CreateView):
    model = User
    form_class = EmployeeRegistrationForm
    template_name = "accounts/employee/register.html"
    success_url = "/"

    extra_context = {"title": "Register"}

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.success_url)
        return super().dispatch(self.request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password1")
            user.set_password(password)
            user.save()
            return redirect("accounts:login")
        else:
            return render(request, "accounts/employee/register.html", {"form": form})


class RegisterEmployerView(CreateView):
    model = User
    form_class = EmployerRegistrationForm
    template_name = "accounts/employer/register.html"
    success_url = "/"

    extra_context = {"title": "Register"}

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.success_url)
        return super().dispatch(self.request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password1")
            user.set_password(password)
            user.save()
            return redirect("accounts:login")
        else:
            return render(request, "accounts/employer/register.html", {"form": form})


class LoginView(FormView):
    """
    Provides the ability to login as a user with an email and password
    """

    success_url = "/"
    form_class = UserLoginForm
    template_name = "accounts/login.html"

    extra_context = {"title": "Login"}

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def get_success_url(self):
        if "next" in self.request.GET and self.request.GET["next"] != "":
            return self.request.GET["next"]
        else:
            return self.success_url

    def get_form_class(self):
        return self.form_class

    def form_valid(self, form):
        auth.login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form))


class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """

    url = "/login"

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        messages.success(request, "You are now logged out")
        return super(LogoutView, self).get(request, *args, **kwargs)


class JobCompanyView(DetailView):
    model = User
    template_name = "accounts/employer/company.html"
    context_object_name = "user"
    pk_url_kwarg = "id"

    def get_object(self, queryset=None):
        obj = super(JobCompanyView, self).get_object(queryset=queryset)
        if obj is None:
            raise Http404("Company doesn't exists")
        return obj

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            # raise error
            raise Http404("Company doesn't exists")
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class SearchcompanyView(ListView):
    model = User
    template_name = "searchcompany.html"
    context_object_name = "searchcompany"
    

    def get_queryset(self):
        # q = JobDocument.search().query("match", title=self.request.GET['position']).to_queryset()
        # print(q)
        # return q
        return self.model.objects.filter(
            city__contains=self.request.GET.get("city", ""),
            first_name__contains=self.request.GET.get("Name", ""),
        )

class CompanyListView(ListView):
    model = User
    template_name = "companysearch.html"
    context_object_name = "companylist"
    paginate_by = 5

    def get_queryset(self):

     return self.model.objects.filter(
            role='employer'
        )


class Viewalljobs(ListView):
    model =Job
    template_name = "companyjobs.html"
    context_object_name = "viewcompanyjobs"

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return Job.objects.filter(user_id=self.kwargs["id"]).order_by("id")

   

    # def dispatch(self, request,id, *args, **kwargs):
    #     return super().dispatch(self.request,id, *args, **kwargs)
   
    # def get(self,request, primary_key):
    #  try:
    #     JOB = self.model.objects.get(user_id=primary_key)
    #  except JOB.DoesNotExist:
    #     raise Http404('job does not exist')
    #  return JOB

    # def get_queryset(self):
    #    return self.model.objects.filter(user_id= id)
         
         