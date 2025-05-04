from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout
from taggit.models import Tag

from social.forms import UserRegisterForm, UserEditForm, TicketForm, CreatePostForm
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
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
    return render(request, 'social/list.html', {'posts': posts, 'tag':tag})


@login_required
def create_post(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect('social:profile')
    else:
        form = CreatePostForm()
    return render(request, 'forms/create_post.html', {'form': form})



def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post_tag_ids = post.tags.values_list('id', flat=True)
    similar_post = Post.objects.filter(tags__in=post_tag_ids).exclude(id=post.id)
    similar_post = similar_post.annotate(same_tags =Count('tags')).order_by('-same_tags', '-created')[:2]
    context = {
        'post': post,
        'similar_post':similar_post,
    }

    return render(request, 'social/details.html', context)














