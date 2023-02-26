from readline import clear_history
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

from accounts.models import User

GENDER_CHOICES = (("male", "Male"), ("female", "Female"))


class EmployeeRegistrationForm(UserCreationForm):
    # gender = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=GENDER_CHOICES)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    mobileno = forms.CharField(required=True,max_length=10,min_length=10)
    city = forms.CharField(required=True)
    qualification = forms.CharField(required=True)
    resume = forms.FileField()


    def __init__(self, *args, **kwargs):
        super(EmployeeRegistrationForm, self).__init__(*args, **kwargs)
        self.fields["gender"].required = True
        self.fields["first_name"].label = "First Name"
        self.fields["last_name"].label = "Last Name"
        self.fields["password1"].label = "Password"
        self.fields["password2"].label = "Confirm Password"
        self.fields["mobileno"].label = "Mobile Number"
        self.fields["city"].label = "City"
        self.fields["qualification"].label = "Qualification"

        # self.fields['gender'].widget = forms.CheckboxInput()

        self.fields["first_name"].widget.attrs.update({"placeholder": "Enter First Name"})
        self.fields["last_name"].widget.attrs.update({"placeholder": "Enter Last Name"})
        self.fields["email"].widget.attrs.update({"placeholder": "Enter Email"})
        self.fields["password1"].widget.attrs.update({"placeholder": "Enter Password"})
        self.fields["password2"].widget.attrs.update({"placeholder": "Confirm Password"})
        self.fields["mobileno"].widget.attrs.update({"placeholder": "Enter Mobile Number"})
        self.fields["city"].widget.attrs.update({"placeholder": "Enter City"})
        self.fields["qualification"].widget.attrs.update({"placeholder": "Your Qualification"})
        self.fields["resume"].widget.attrs.update({"placeholder": "Your Resume"})


    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password1", "password2", "gender","mobileno","city","qualification","resume"]
        error_messages = {
            "first_name": {"required": "First name is required", "max_length": "Name is too long"},
            "last_name": {"required": "Last name is required", "max_length": "Last Name is too long"},
            "gender": {"required": "Gender is required"},
            "mobileno": {"required": "Mobile Number is required", "max_length": "Enter Valid mobile number","min_length":"Enter Valid mobile number"},
        }

    def clean_gender(self):
        gender = self.cleaned_data.get("gender")
        if not gender:
            raise forms.ValidationError("Gender is required")
        return gender

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.role = "employee"
        if commit:
            user.save()
        return user


class EmployerRegistrationForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    city = forms.CharField(required=True)
    company_description = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(EmployerRegistrationForm, self).__init__(*args, **kwargs)
        self.fields["first_name"].label = "Company Name"
        self.fields["city"].label = "Company Address"
        self.fields["company_description"].label = "Company Description"
        self.fields["password1"].label = "Password"
        self.fields["password2"].label = "Confirm Password"

        self.fields["first_name"].widget.attrs.update({"placeholder": "Enter Company Name"})
        self.fields["city"].widget.attrs.update({"placeholder": "Enter Company Address"})
        self.fields["company_description"].widget.attrs.update({"placeholder": "Enter Company Description"})
        self.fields["email"].widget.attrs.update({"placeholder": "Enter Email"})
        self.fields["password1"].widget.attrs.update({"placeholder": "Enter Password"})
        self.fields["password2"].widget.attrs.update({"placeholder": "Confirm Password"})

    class Meta:
        model = User
        fields = ["first_name", "city", "email","company_description", "password1", "password2"]
        error_messages = {
            "first_name": {"required": "Company name is required", "max_length": "Name is too long"},
            "city": {"required": "Company address is required", "max_length": "Address is too long"},
            "company_description": {"required": "Company Description is required", "max_length": "Description is too long"},
            "email": {"required": "Email is required"},

        }

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.role = "employer"
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(label="Password", strip=False, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.fields["email"].widget.attrs.update({"placeholder": "Enter Email"})
        self.fields["password"].widget.attrs.update({"placeholder": "Enter Password"})

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            self.user = authenticate(email=email, password=password)

            if self.user is None:
                raise forms.ValidationError("Email or Password Incorrect.")
            if not self.user.check_password(password):
                raise forms.ValidationError("Password Does not Match.")
            if not self.user.is_active:
                raise forms.ValidationError("User is not Active.")

        return super(UserLoginForm, self).clean(*args, **kwargs)

    def get_user(self):
        return self.user


class EmployeeProfileUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EmployeeProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs.update({"placeholder": "Enter First Name"})
        self.fields["last_name"].widget.attrs.update({"placeholder": "Enter Last Name"})
        self.fields["mobileno"].widget.attrs.update({"placeholder": "Enter Mobile Number"})
        self.fields["city"].widget.attrs.update({"placeholder": "Enter City"})
        self.fields["qualification"].widget.attrs.update({"placeholder": "Your Qualification"})
        self.fields["resume"].widget.attrs.update({"placeholder": "Your Resume"})


    class Meta:
        model = User
        fields = ["first_name", "last_name", "gender","mobileno","city","qualification","resume"]


class EmployerProfileUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EmployerProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs["placeholder"] = "Company name"
        self.fields["city"].widget.attrs["placeholder"] = "Company address"
        self.fields["company_description"].widget.attrs["placeholder"] = "Company Description"

        self.fields["first_name"].label = "Company name"
        self.fields["city"].label = "Company address"
        self.fields["company_description"].label = "Company Description"

    class Meta:
        model = User
        fields = ["first_name", "city","company_description"]
