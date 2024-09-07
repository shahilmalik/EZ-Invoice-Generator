
# Create your views here.
from django.shortcuts import render, redirect
from .forms import CreateUserForm,AddClientForm,AddServiceForm, AddProfileForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

#reset_password
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth import get_user_model

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.contrib.auth.models import User
from .models import Service,Client, Profile

def reset_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            current_site = get_current_site(request)
            subject = 'Reset your password'
            message = render_to_string('reset_password.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            message = Mail(
                from_email='shahilabdul001@gmail.com',
                to_emails=email,
                subject=subject,
                html_content=message)
            try:
                sg = SendGridAPIClient('API')
                response = sg.send(message)
                print("It Worked")
                print(response.status_code)
                print(response.body)
                print(response.headers)
            except Exception as e:
                print(str(e))
                print("It did'nt")
            return redirect('login')
    else:
        form = PasswordResetForm()
    return render(request, 'forgotps.html', {'form': form})


def home_view(request, *args, **kwargs):
    return render(request, "newapp.html", {})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method=='POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.info(request,'User or Password is incorrect')
    return render(request,"login.html",{})


def forgotps_view(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(request=request)
            # Display success message
            return redirect(reverse_lazy('login') + '?reset')

    else:
        form = PasswordResetForm()
    return render(request, 'forgotps.html', {'form': form})



def register_view(request):
    form = CreateUserForm()
    if request.method == "POST":
        form =CreateUserForm(request.POST)
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('register')

        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
        if form.is_valid():
            user = form.save()
            profile = Profile.objects.create(user=user)
            profile.company_name = 'Company Name'
            profile.company_gst = 'company GST'
            profile.company_address_line1 = "Line 1..",
            profile.company_address_line2 = "Line 2..",
            profile.company_city = "City",
            profile.company_state = "State",
            profile.company_pincode = "pin..",
            profile.account_name = "Account Name",
            profile.account = "Account No.",
            profile.ifsc = "IFSC"
            # set other profile fields as necessary
            profile.save()
            fname= form.cleaned_data.get('username')
            messages.success(request,"Account successfully created for "+fname )
            return redirect('login')
        else:
            messages.info(request,'The password should be an alphanumeric >7 & should hava a special character')
    context = {'form':form}
    return render(request, "signup.html", context)



def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def dashboard_view(request):
    return render(request,"dashboard.html",{})

@login_required(login_url='login')
def clients_view(request):
    if request.method == 'POST':
        form = AddClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.user = request.user
            client.save()
            return redirect('clients')
    else:
        form = AddClientForm()

    clients = Client.objects.filter(user=request.user)
    return render(request, 'clients2.html', {'clients': clients, 'form': form})


@login_required(login_url='login')
def services_view(request):
    if request.method == 'POST':
        form = AddServiceForm(request.POST)
        if form.is_valid():
            services = form.save(commit=False)
            services.user = request.user
            services.save()
            return redirect('services')
    else:
        form = AddServiceForm()

    services = Service.objects.filter(user=request.user)
    return render(request, 'services.html', {'services': services, 'form': form})


@login_required(login_url='login')
def profile_view(request):
    profile=Profile.objects.get(user=request.user)
    return render(request,'profile.html',{'profile':profile})


@login_required(login_url='login')
def profile_edit_view(request):
    # get the profile object from the database
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        # get the updated company name from the form input
        new_name=request.POST.get('username')
        request.user.username = new_name
        profile.company_name = request.POST.get('company_name')
        profile.company_gst = request.POST.get('company_gst')
        profile.company_address_line1 = request.POST.get('company_line1')
        profile.company_address_line2 = request.POST.get('company_line2')
        profile.company_city = request.POST.get('city')
        profile.company_state = request.POST.get('state')
        profile.company_pincode = request.POST.get('pin')
        profile.account = request.POST.get('account')
        profile.account_name = request.POST.get('account_name')
        profile.ifsc = request.POST.get('ifsc')
        profile.phone_number = request.POST.get('phone')
        # update the company_name field of the profile objec
        # save the updated profile object to the database
        profile.save()
        request.user.save()

        # redirect to a success page or render a success message
        return redirect('profile')

    context = {'profile': profile}
    return render(request, 'profile_edit.html', context)


