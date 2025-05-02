from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import logout

from social.forms import UserRegisterForm, UserEditForm


# Create your views here.

def user_logout(request):
    logout(request)
    return HttpResponse("logout page")

def profile(request):
    return HttpResponse("profile page")

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            return render(request, 'registration/register_done.html', {'user': user})

    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def edit_user(request):
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user, files=request.FILES)
        if user_form.is_valid:
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)

    context = {
        'user_form': user_form,
    }
    return render(request, 'registration/edit_user.html', context)
