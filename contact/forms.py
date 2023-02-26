from django import forms
from .models import Contact
from django.contrib.auth.forms import UserCreationForm


class ContactForm(forms.ModelForm):
    email = forms.EmailField()
    subject = forms.CharField(max_length=255)
    message = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields["email"].required = "Email"
        self.fields["subject"].label = "Subject"
        self.fields["message"].label = "Message"
       

        self.fields["email"].widget.attrs.update({"placeholder": "Enter Your EmailId"})
        self.fields["subject"].widget.attrs.update({"placeholder": "Enter Subject"})
        self.fields["message"].widget.attrs.update({"placeholder": "Enter Your Message"})

    class Meta:
        model = Contact
        fields = ["email", "subject", "message"]
        error_messages = {
            "email": {"required": "Email is required"},
            "subject": {"required": "Subject is required", "max_length": "Subject is too long"},
            "message": {"required": "Message is required"},
        }  