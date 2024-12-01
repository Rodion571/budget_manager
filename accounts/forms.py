from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model


class UserRegisterForm(UserCreationForm):
    """
    Form for registering a new user.

    Attributes:
        email (forms.EmailField): The email field for the registration form.
    """
    email: forms.EmailField = forms.EmailField(required=True)

    class Meta:
        """
        Meta class to define the model and fields.

        Attributes:
            model: The user model.
            fields: The fields to include in the form.
        """
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self) -> str:
        """
        Validate that the provided email is unique.

        Raises:
            forms.ValidationError: If the email is already in use.

        Returns:
            str: The cleaned email.
        """
        email = self.cleaned_data.get('email')
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Email is already in use.')
        return email


class UserLoginForm(AuthenticationForm):
    """
    Form for logging in a user.

    Attributes:
        username (forms.CharField): The username field for the login form.
        password (forms.CharField): The password field for the login form.
    """
    username: forms.CharField = forms.CharField(max_length=100)
    password: forms.CharField = forms.CharField(widget=forms.PasswordInput)
