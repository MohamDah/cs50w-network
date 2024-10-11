from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse, resolve
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from django.core.paginator import Paginator

import datetime
import json

from .models import User, post, follow, likes


def index(request):
    posts = post.objects.all().order_by("-date")
    if posts.count() <= 10:
        if request.user.is_authenticated:
            liked_list = request.user.likeds.values_list('liked', flat=True)
        else:
            liked_list = []
        return render(request, "network/index.html", {
            "posts": posts,
            "liked_list": liked_list
        })

    else:
        return HttpResponseRedirect(reverse('paged', args=(1,)))


def paged_index(request, PAGE):
    posts = post.objects.all().order_by("-date")
    if posts.count() <= 10:
        return HttpResponseRedirect(reverse('index'))

    pag = Paginator(posts, 10)
    try:
        page = pag.page(PAGE)
    except:
        return HttpResponseRedirect(reverse('paged', args=(1,)))
    posts = page.object_list
    amount = range(1, pag.num_pages + 1)

    if request.user.is_authenticated:
        liked_list = request.user.likeds.values_list('liked', flat=True)
    else:
        liked_list = []

    return render(request, "network/paged.html", {
        "page": page,
        "posts": posts,
        "amount": amount,
        "liked_list": liked_list
    })
# NEXT IMPLEMENT THE PAGINATION IN THE FOLLOWING PAGE

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required(login_url='/login')
def newpost(request):
    if request.method == "POST":
        poster = request.user.username
        text = request.POST["text"]
        if not text:
            return render(request, "network/newpost.html", {
                "message": "Post can't be empty"
            })
        date = datetime.datetime.now()

        p = post(poster=poster, text=text, date=date)
        p.save()

        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/newpost.html")

def profile(request, user_id):
    if request.method == "POST":
        target = User.objects.get(pk=user_id)
        if request.POST["reason"] == "follow":
            f = follow(following_user=request.user, followed_user=target)
            f.save()
        elif request.POST["reason"] == "unfollow":
            f = follow.objects.get(following_user=request.user, followed_user=target)
            f.delete()

        return HttpResponseRedirect(reverse("profile", args=(user_id,)))
    else:
        following = follow.objects.filter(following_user=user_id)
        profile = User.objects.get(pk=user_id)
        followers = follow.objects.filter(followed_user=user_id)
        status = follow.objects.filter(following_user=request.user.pk, followed_user=user_id)
        posts = post.objects.filter(poster=profile.username).order_by("-date")

        if request.user.is_authenticated:
            liked_list = request.user.likeds.values_list('liked', flat=True)
        else:
            liked_list = []

        return render(request, "network/profile.html", {
            "following": following,
            "profile": profile,
            "followers": followers,
            "status": status,
            "posts": posts,
            "liked_list": liked_list
        })

@login_required(login_url='/login')
def following_page(request):
    f = follow.objects.filter(following_user=request.user.pk).values_list('followed_user', flat=True)
    names = User.objects.filter(pk__in=f).values_list('username', flat=True)
    posts = post.objects.filter(poster__in=names).order_by("-date")
    if posts.count() > 10:
        return HttpResponseRedirect(reverse('paged_following', args=(1,)))

    if request.user.is_authenticated:
        liked_list = request.user.likeds.values_list('liked', flat=True)
    else:
        liked_list = []

    if posts.count() <= 10:
        return render(request, "network/following.html", {
            "posts": posts,
            "liked_list": liked_list
        })
    else:
        return HttpResponseRedirect(reverse('paged_following', args=(1,)))


@login_required(login_url='/login')
def paged_following(request, PAGE):
    f = follow.objects.filter(following_user=request.user.pk).values_list('followed_user', flat=True)
    names = User.objects.filter(pk__in=f).values_list('username', flat=True)
    posts = post.objects.filter(poster__in=names).order_by("-date")
    if posts.count() <= 10:
        return HttpResponseRedirect(reverse('following_page'))

    pag = Paginator(posts, 10)
    try:
        page = pag.page(PAGE)
    except:
        return HttpResponseRedirect(reverse('paged_following', args=(1,)))
    posts = page.object_list
    amount = range(1, pag.num_pages + 1)

    if request.user.is_authenticated:
        liked_list = request.user.likeds.values_list('liked', flat=True)
    else:
        liked_list = []

    return render(request, "network/paged_following.html", {
        "page": page,
        "posts": posts,
        "amount": amount,
        "liked_list": liked_list
    })

@login_required(login_url='/login')
def editpost(request):
    if request.method == "POST":
        text = request.POST["text"]
        postpk = request.POST["postpk"]
        the_post = post.objects.get(pk=postpk)
        if the_post.poster != request.user.username:
            return render(request, "network/apology.html")

        the_post.text = text
        the_post.save(update_fields=["text"])
        url = request.POST["url"]
        return HttpResponseRedirect(url)

@csrf_exempt
def like_fun(request):
    if request.method == "POST":
        data = json.loads(request.body)
        post_id = data.get("post_id", "")
        thepost = post.objects.get(pk=post_id)

        if data.get("reason", "") == "like":
            newlike = likes(liker=request.user, liked=thepost)
            newlike.save()
            amount = thepost.likers.count()
            return JsonResponse({"amount": amount}, status=201)
        elif data.get("reason", "") == "unlike":
            like = likes.objects.get(liker=request.user, liked=thepost)
            like.delete()
            amount = thepost.likers.count()
            return JsonResponse({"amount": amount}, status=201)


# route for accessing profile from posts
def access_profile(request, username):
    user = User.objects.get(username=username)
    user_id = user.pk
    return HttpResponseRedirect(reverse('profile', args=(user_id,)))