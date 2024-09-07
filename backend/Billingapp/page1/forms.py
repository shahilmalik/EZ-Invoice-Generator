from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Service,Client, Profile


class AddClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'gst', 'phone','email','address_line1','address_line2','city','state','pincode']


class AddServiceForm(ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'price']



class AddProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['company_name', 'company_gst', 'company_address_line1', 'company_address_line2', 'company_city',
                  'company_state', 'company_pincode', 'account', 'account_name', 'ifsc']
        company_name = forms.CharField(max_length=100)
        company_gst = forms.CharField(max_length=100)
        company_address_line1 = forms.CharField(max_length=100)
        company_address_line2 = forms.CharField(max_length=100)
        company_city = forms.CharField(max_length=100)
        company_state = forms.CharField(max_length=100)
        company_pincode = forms.CharField(max_length=100)
        account = forms.CharField(max_length=100)
        account_name = forms.CharField(max_length=100)
        ifsc = forms.CharField(max_length=100)
        phone_number = forms.CharField(max_length=10)

        def __init__(self, *args, **kwargs):
            super(AddProfileForm, self).__init__(*args, **kwargs)

            # Set the same attributes for all fields
            for field in self.fields:
                placeholder = self.fields[field].initial if self.fields[field].initial else field.title().replace('_', ' ')
                self.fields[field].widget.attrs.update({'class': 'my-inp', 'placeholder': placeholder})


class CreateUserForm(UserCreationForm):
    # first_name = forms.CharField(max_length=30, required=True, help_text='Required.',widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    # last_name = forms.CharField(max_length=30, required=True, help_text='Required.',widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))

    class Meta:
        model=User
        fields=["first_name","last_name","username","email","password1","password2"]
