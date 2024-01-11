from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Profile, Post
from itertools import chain
from django.urls import reverse


def index(request):
    return render(request, 'index.html')


# stop accessing to home page without loging in

@login_required(login_url='user_login')
def homepage(request):
    user_object = User.objects.get(username=request.user.username)
    try:
        user_profile = Profile.objects.get(user=user_object)
    except Profile.DoesNotExist:
        # Create a Profile for the user if it doesn't exist
        user_profile = Profile.objects.create(user=user_object)

    # # make feature  users can see post from people geographically close to them.

    posts = Post.objects.all()
    return render(request, 'Pp_homepage.html', {'user_profile': user_profile, 'posts': posts})


# @login_required(login_url='user_login')
# def wink(request, pk):
#     postwink = get_object_or_404(Profile, id=request.POST.get('id_profile'))
#     postwink.no_of_winks.add(request.user)
#     return HttpResponseRedirect(reverse('profile', args=[str(pk)]))


@login_required(login_url='user_login')
def profile(request, pk):

    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_post_length = len(user_posts)

    nu_context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
    }

    return render(request, 'profile.html', nu_context)


@login_required(login_url='user_login')
def nu_context_for_winks(kwargs):
    context = {}
    primary_key_recovery = get_object_or_404(Profile, id=kwargs['pk'])
    total_winks = primary_key_recovery.total_winks()
    context['total_winks'] = total_winks

    return context


@login_required(login_url='user_login')
def search(request):
    user_objects = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_objects)

    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(user_id=ids)
            username_profile_list.append(profile_lists)

            username_profile_list = list(chain(*username_profile_list))
    return render(request, 'search.html', {'user_profile': user_profile, 'username_profile_list': username_profile_list})


@login_required(login_url='user_login')
def settings(request):
    user_profle = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        if request.FILES.get('image') == None:
            image = user_profle.profileimg
            bio = request.POST['bio']
            location = request.POST['location']

            user_profle.profileimg = image
            user_profle.bio = bio
            user_profle.location = location
            user_profle.save()

        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']

            user_profle.profileimg = image
            user_profle.bio = bio
            user_profle.location = location
            user_profle.save()

        return redirect('settings')

    return render(request, 'settings.html', {'user_profile': user_profle})


@login_required(login_url='user_login')
def upload(request):
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        if image:
            new_post = Post.objects.create(
                user=user, image=image, caption=caption)
            new_post.save()

        return redirect('homepage')
    else:
        return redirect('homepage')


@login_required(login_url='user_login')
def delete_post(request, post_id):
    post_uploaded = get_object_or_404(
        Post, id=post_id, user=request.user.username)

    if request.method == 'POST':
        post_uploaded.delete()

    return redirect('homepage')


def signup(request):
    if request.method == 'POST':
        username = request.POST['Username']
        email = request.POST['Email']
        password = request.POST['Password']
        password2 = request.POST['Password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(
                    username=username, email=email, password=password)
                user.save()

                # Log user and redirect to the login setting page

                user_login = auth.authenticate(
                    username=username, password=password)
                auth.login(request, user_login)

                # create a Profile object for the new user

                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(
                    user=user_model, id_profile=user_model.id)
                new_profile.save()
                # setting user page later (video 1:53)
                return redirect('settings')

        else:
            messages.info(request, 'The Password Is Not Matching')
            return redirect('signup')

    else:
        return render(request, 'signup.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['Username']
        password = request.POST['Password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:  # if user is present in our database
            auth.login(request, user)
            return redirect('homepage')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('user_login')
    else:
        return render(request, 'login.html')


@login_required(login_url='user_login')
# stop accessing to home page without loging in
def logout(request):
    auth.logout(request)
    return redirect('user_login')
