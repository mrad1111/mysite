from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import RegexValidator

from .models import Review


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-lg ps-5",
                "placeholder": "Username or Email",
                "autocomplete": "username",
                "id": "usernameInput",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-lg ps-5 pe-5",
                "placeholder": "Password",
                "autocomplete": "current-password",
                "id": "passwordInput",
            }
        )
    )



class RegisterForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-lg ps-5",
                "placeholder": "Choose a username",
                "autocomplete": "username",
            }
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control form-control-lg ps-5",
                "placeholder": "name@example.com",
                "autocomplete": "email",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-lg ps-5",
                "placeholder": "Create a strong password",
                "autocomplete": "new-password",
            }
        )
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
        ]



class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=120, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Your full name"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "you@example.com"}))
    phone = forms.CharField(
        max_length=10,
        min_length=10,
        validators=[RegexValidator(r"^\d{10}$", "Enter a valid 10-digit phone number.")],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "10-digit phone number",
                "type": "tel",
                "inputmode": "numeric",
                "pattern": "[0-9]{10}",
                "autocomplete": "tel",
                "data-numeric-only": "true",
            }
        ),
    )
    address = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Street address"}))
    city = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "City"}))
    zip_code = forms.CharField(max_length=20, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "ZIP code"}))
    payment_method = forms.ChoiceField(
        choices=[("cod", "Cash on Delivery")],
        widget=forms.Select(attrs={"class": "form-select"})
    )
    coupon_code = forms.CharField(required=False, max_length=20, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter coupon code"}))
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Any delivery notes?"}))


class ContactForm(forms.Form):
    full_name = forms.CharField(max_length=120, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Your full name"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "you@example.com"}))
    subject = forms.CharField(max_length=150, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Subject"}))
    message = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control", "rows": 5, "placeholder": "Your message"}))


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = [
            "rating",
            "comment",
        ]

        widgets = {
            "rating": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                    "max": 5,
                }
            ),
            "comment": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Write your review...",
                }
            ),
        }