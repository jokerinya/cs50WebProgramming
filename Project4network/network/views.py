import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post

class NewPostForm(forms.Form):
    post = forms.CharField(widget=forms.Textarea(attrs={
        'class':'form-control',
        'placeholder':'Write your new post here'
        }),label="New Post", max_length=280)

def post_pagination(post_list, page):
    paginator = Paginator(post_list, 10)  # Show 10 posts per page
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)
    return posts


def index(request):
     # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NewPostForm(request.POST)
        user = request.user
        # check whether it's valid:
        if form.is_valid() and (user is not None):
            # process the data in form.cleaned_data as required
            content = form.cleaned_data["post"]
            # Check 280 char rule
            if len(content) <= 280:
                new_post = Post(creater=user, content=content)
                new_post.save()  # save to db
                form = NewPostForm()  # empty form
    # if a GET (or any other method) we'll create a blank form
    else:
        form = NewPostForm()
    
    # Pagination #
    post_list = Post.objects.all()
    page = request.GET.get('page')

    context = {
        "posts" : post_pagination(post_list, page),
        "form" : form
    }
    return render(request, "network/index.html", context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("network:index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("network:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("network:index"))
    else:
        return render(request, "network/register.html")

@login_required(login_url="/login")
def following_view(request):
    if request.method == "GET":
        user = request.user
        posts = Post.objects.filter(creater__in=[u.id for u in user.following_users.all()])
        context = {
            # Pagination
            "posts" : post_pagination(posts, request.GET.get('page')),
            "followings" : user.following_users.count()
        }
        return render(request, "network/followings.html", context)

@csrf_exempt
@login_required(login_url="/login")
def post_edit_view(request, post_id):
    # Query for requested post
    try:
        user = request.user
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("isLiked") is not None:
            user_liked_post = data["isLiked"]  # will be True or False
            if user_liked_post:
                post.liked_users.add(user)
            else:
                post.liked_users.remove(user)
        if data.get("edittedPost") is not None:
            editted_post = data["edittedPost"]
            if len(editted_post) > 280 or len(editted_post) == 0:
                return JsonResponse({"error": "Post is not valid."}, status=422)
            post.content = editted_post
        post.save()
        likeNum = post.liked_users.count()
        return JsonResponse({"likeNum": likeNum, "postRecorded": True}, status=201)
    # Must PUT method
    else:
        return JsonResponse({"error": "PUT request required."}, status=400)

@login_required(login_url="/login")
def profile_view(request):
    if request.method == "GET":
        user = request.user
        posts = user.posts.all()
        users = User.objects.exclude(id=user.id).exclude(is_superuser=True)
        context = {
            "user": user,
            "users": users,
            "posts" : post_pagination(posts, request.GET.get('page'))
        }
        return render(request, "network/profile.html", context)

@csrf_exempt
@login_required(login_url="/login")
def user_follow_view(request, user_id):
    try:
        user = request.user
        fuser = User.objects.get(id=user_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    # Users cannot follow themselves
    if user == fuser:
        return JsonResponse({"error": "Users cannot follow themselves."}, status=404)

    if request.method == "PUT":
        data = json.loads(request.body)
        result = {}
        if data.get("willFollow") is not None:
            user_willfollow_fuser = data["willFollow"]  # will be True or False
            if user_willfollow_fuser:
                user.following_users.add(fuser)
                result["isFollowing"] = True
            else:
                user.following_users.remove(fuser)
                result["isFollowing"] = False
            result["followings"] = user.following_users.count()
            result["followers"] = user.followers.count()
        return JsonResponse(result, status=201)
    # Must PUT method
    else:
        return JsonResponse({"error": "PUT request required."}, status=400)