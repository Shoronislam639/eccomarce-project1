from django.shortcuts import render, redirect
from userauth.form import UserRegistrationForm
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.conf import settings
from userauth.models import User

#User = settings.AUTH_USER_MODEL

def register_view(request):
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST or None)
        if form.is_valid():
            new_user=form.save()
            username=form.cleaned_data.get('username')
            messages.success(request, f'hey {username}your account was created succesfully!')
            new_user = authenticate(username=form.cleaned_data['email'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)
            return redirect('core:home')
            
    else:
        form = UserRegistrationForm()
    

    
    context = {
        'form': form,
    }
    return render(request, 'userauth/sign-up.html', context)





#login view

def Login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, f'You are already logged in')
        return redirect('core:home')
    
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You are logged in')
                return redirect('core:home')
            else:
                messages.warning(request, 'User does not exist, Create an account')
        except:
            messages.warning(request, f'user with {email} does not exist ')
            
        
    context={}
    return render(request, 'userauth/sign-in.html')




def logout_view(request):
    logout(request)
    messages.success(request, 'You are logged out')
    return redirect('userauth:sign-in')
           
# Create your views here.
