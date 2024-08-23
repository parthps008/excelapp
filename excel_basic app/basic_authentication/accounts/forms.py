from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    # Additional fields for user registration
    public_visibility = forms.BooleanField(required=False, label='Public Visibility')
    birth_year = forms.IntegerField(required=False, label='Birth Year', widget=forms.NumberInput(attrs={'placeholder': 'YYYY'}))
    address = forms.CharField(required=False, label='Address', widget=forms.Textarea(attrs={'placeholder': 'Your address'}))
    age = forms.IntegerField(required=False, label='Age')  # Make sure to validate this field appropriately

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('public_visibility', 'birth_year', 'address', 'age')

    def clean_age(self):
        # Custom validation for age if needed
        age = self.cleaned_data.get('age')
        if age and age <= 0:
            raise forms.ValidationError("Age must be a positive number.")
        return age

class CustomUserLoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False, label='Remember me')

    def confirm_login_allowed(self, user):
        # Additional custom logic for login validation if needed
        pass
