import datetime

from django import forms

from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import Division, Client, Scope, ItemType

User = get_user_model()

class RegisterForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100, widget=forms.TextInput(attrs={'class': 'login-input login-username'}))
    email = forms.EmailField(label="Email", max_length=100, widget=forms.TextInput(attrs={'class': 'login-input login-email'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'login-input login-password'}))
    confirm_password = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class': 'login-input login-password'}))

    ROLES = [
        ('estimator', 'Estimator'),
        ('manager', 'Manager'),
    ]

    role = forms.ChoiceField(label='Role', choices=ROLES)
    
    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords must match")

        return confirm_password
    

class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100, widget=forms.TextInput(attrs={'class': 'login-input login-username'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'login-input login-password'}))


class NewProjectForm(forms.Form):
    name = forms.CharField(label="Project Name", max_length=100)
    client = forms.ModelChoiceField(label="Client", queryset=Client.objects.all())
    address = forms.CharField(label="Address", max_length=100)
    description = forms.CharField(label="Description", max_length=500)

    STATUS = [
        ('bidding', 'Bidding'),
        ('awarded', 'Awarded'),
        ('pre-construction', 'Pre-construction'),
        ('course of construction', 'Course of Construction'),
    ]

    status = forms.ChoiceField(label='Status', choices=STATUS)

    area = forms.DecimalField(label="Area (sq.m)")
    bid_deadline = forms.DateField(label="Bid Deadline")
    estimator = forms.ModelChoiceField(label="Estimator", queryset=User.objects.filter(role='estimator'))
    manager = forms.ModelChoiceField(label="Manager", queryset=User.objects.filter(role='manager'))
    divisions = forms.ModelMultipleChoiceField(label="Divisions", queryset=Division.objects.all(), widget=forms.CheckboxSelectMultiple())


class NewClientForm(forms.Form):
    name = forms.CharField(label="New Client", max_length=100)
    address = forms.CharField(label="Address", max_length=100)
    image = forms.ImageField(required=False)


class AddDivisionsForm(forms.Form):
    divisions = forms.ModelMultipleChoiceField(label="", queryset=Division.objects.none(), widget=forms.CheckboxSelectMultiple())

    def __init__(self, project, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['divisions'].queryset = Division.objects.exclude(project=project)
        self.project = project


class AddScopeForm(forms.Form):
    name = forms.CharField(label="Scope", max_length=100)
    qty = forms.DecimalField(label="quantity", decimal_places=2)
    unit = forms.CharField(label="unit", max_length=100)
    divisions = forms.ModelChoiceField(label="Division", queryset=Division.objects.none())

    def __init__(self, project, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['divisions'].queryset = project.divisions.all()


class AddNewDivisionForm(forms.Form):
    name = forms.CharField(label="", max_length=100)


class AddItem(forms.Form):
    name = forms.CharField(label="Item", max_length=100)
    qty = forms.DecimalField(label="quantity", decimal_places=2)
    unit = forms.CharField(label="unit", max_length=100)
    unit_price = forms.DecimalField(label="unit price", decimal_places=2)
    scope = forms.ModelChoiceField(label="Scope", queryset=Scope.objects.none())
    type = forms.ModelChoiceField(label="Type", queryset=ItemType.objects.all())

    def __init__(self, project, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['scope'].queryset = project.scopes.all()
