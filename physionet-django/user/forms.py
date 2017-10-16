from django import forms
from .models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm, UsernameField


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password.

    This is a ModelForm which takes attributes from the User model.
    """

    # Since password is not a field in the User model, these form fields
    # must be specified here
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class LoginForm(AuthenticationForm):
    """
    Form for logging in.
    """
    username = UsernameField(
        max_length=254,
        widget=forms.TextInput(attrs={'autofocus': True, 'class':'form-control', 'placeholder':'Email Address'}),
    )
    password = forms.CharField(
        label= 'Password',
        strip=False,
        widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}),
    )

    remember = forms.BooleanField(label='Remember Me', required=False)