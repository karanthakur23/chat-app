from django.shortcuts import render
from .forms import SignUpForm
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import logout as auth_logout

# Create your views here.

User = get_user_model()

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            new_user = User.objects.create_user(username=username, email=email, password=password)

            login(request, new_user)
            return HttpResponseRedirect(reverse('home'))
    else:
        form = SignUpForm()
    return render(request, 'accounts/register.html', {'form': form})

def loginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse("Account Not Active")
        else:
            context = {
                'notfound': True
            }
            return render(request, 'accounts/login.html', context)
    return render(request, 'accounts/login.html')

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('home'))