from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import logout

from social.forms import UserRegisterForm, UserEditForm, TicketForm
from social.models import Post


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

def ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            message = f'{cd["name"]}\n{cd["email"]}\n{cd["phone"]}\n\n{cd["message"]}'
            send_mail(cd["subject"], message, 'shahmoradinrges@gmail.com',
                      ['venusshahmoradi3@gmail.com'])
            messages.success(request, 'Your ticket has been sent.')
    else:
        form = TicketForm()
    return render(request, 'forms/ticket.html', {'form': form})


def post_list(request, tag_slug=None):
    posts = Post.objects.all()
    return render(request, 'social/list.html', {'posts': posts})