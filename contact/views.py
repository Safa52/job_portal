from django.shortcuts import render,redirect
from .forms import ContactForm
from django.views.generic import CreateView
from contact.models import Contact



class contact_view(CreateView):
    model = Contact
    form_class = ContactForm
    template_name = "contact.html"
    success_url = "/"

    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)

        if form.is_valid():
           form.save()
           return render(request, "home.html")
        else:
            return render(request, "contact.html", {"form": form})

