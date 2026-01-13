from django import forms
from django.contrib.auth.models import User
from .models import VerificationCode
from django.contrib.auth.forms import AuthenticationForm
# from utils.send_email import send_email_custom
# from utils.code_generator import random_with_N_digits
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserAdminCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name','password')

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'is_active')

    # def clean_password(self):
    #     # Regardless of what the user provides, return the initial value.
    #     # This is done here, rather than on the field, because the
    #     # field does not have access to the initial value
    #     return self.initial["password"]


class CreateAccountForm(forms.ModelForm):
    re_password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        if self.data['password'] != self.data['re_password']:
            raise forms.ValidationError("Passwords don't match")
        elif User.objects.filter(email=self.data['email']).exists():
            raise forms.ValidationError("Email is already exists")
        return super().clean()

    class Meta:
        model = User
        fields = ( "first_name", "last_name",
                  "email", "password", "re_password")

    def save(self):
        user = User.objects.create_user(first_name=self.cleaned_data['first_name'], last_name=self.cleaned_data['last_name'], is_active=False,
                                        email=self.cleaned_data['email'], username=self.cleaned_data['username'], password=self.cleaned_data['password'])
        code_inst = VerificationCode.objects.create(user=user, code=random_with_N_digits(
        ), label=VerificationCode.SIGNUP, email=user.email)
        context = {
            "activate_url": f"http://localhost:8000/activate-account/?code={code_inst.code}&email={code_inst.email}"}
        # send_email_custom(user.email, "Activate your account", context)
        return user


class CustomLoginForm(AuthenticationForm):
    pass