import json
import re
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import User, Publication, User_followers, Categories


def index(request):
    publications = Publication.objects.all()
    return render(request, "devmo/index.html", {"list": publications})

def publication(request, publication_id):
    session_user = ""
    if request.user.id:
        session_user = (request.user).serialize()
    else:
        session_user = None
    publication = Publication.objects.get(id=publication_id)
    try:
        User_followers.objects.get(user_id=publication.user_p)
        publication_user = User_followers.objects.get(user_id=publication.user_p)
    except:
        publication_user = None
    user_info = User.objects.get(username=publication.user_p)
    isFollow= ""
    isLiked = ""
    isBookmarked = ""
    if publication_user != None:
        if request.user != publication.user_p and (request.user in publication_user.followers.all()):
            isFollow = "yes"
        elif request.user != publication.user_p and (request.user not in publication_user.followers.all()):
            isFollow = "no"
        else:
            isFollow = "your"
        if request.user in publication.favorites.all():
            isBookmarked = "yes"
        else:
            isBookmarked = "no"
        if request.user in publication.likes.all():
            isLiked = "yes"
        else:
            isLiked = "no"
    else:
        isFollow = "no"
        isBookmarked = "no"
        isLiked = "no"
    return render(request, "devmo/publication.html", {"publication": publication.serialize(), "isLiked": isLiked, "isBookmarked": isBookmarked, "isFollow": isFollow, "user_info": user_info.serialize(), "session_user": session_user})

@csrf_exempt
def like(request, publication_id):
    try:
        post = Publication.objects.get(pk=publication_id)
    except Publication.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.method == "GET":
        return JsonResponse({"error": f"{post}"}, status=404)

    # Update like's counter
    elif request.method == "POST":
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            return JsonResponse({"info": post.serialize(), "like": "no"}, safe=False)
        else:
            post.likes.add(request.user)
            return JsonResponse({"info": post.serialize(), "like": "yes"}, safe=False)
        return HttpResponse(status=204)
    else:
        return JsonResponse({
            "error": "GET or POST request required."
        }, status=400)

@csrf_exempt
def follow(request, username):
    # Query for requested email
    try:
        user_user = User.objects.get(username=username)
        user = User_followers.objects.get(user_id=user_user)
    except User_followers.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)

    if request.method == "GET":
        return JsonResponse({"error": f"{user}"}, status=404)

    elif request.method == "POST":
        if request.user.username != username:
            if request.user in user.followers.all():
                user.followers.remove(request.user)
                following = user_user.following.values_list("user_id__id", flat=True)
                return JsonResponse({"info":user.serialize(), "isFollow": "no", "following": following.count()}, safe=False)
            else:
                user.followers.add(request.user)
                following = user_user.following.values_list("user_id__id", flat=True)
                return JsonResponse({"info":user.serialize(), "isFollow": "yes", "following": following.count()}, safe=False)
            return HttpResponse(status=204)
        else:
            following = user_user.following.values_list("user_id__id", flat=True)
            return JsonResponse({"info":user.serialize(), "isFollow": "Your profile", "following": following.count()}, safe=False)

    # Follow must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or POST request required."
        }, status=400)

def profile_info(request, username):
    session_user = ""
    if request.user.id:
        session_user = (request.user).serialize()
    else:
        session_user = None
    user = User.objects.get(username=username)
    try:
        user_info = User_followers.objects.get(user_id=user)
        following = user.following.values_list("user_id__id", flat=True)
        posts = Publication.objects.filter(user_p=user)
    except User_followers.DoesNotExist:
        return JsonResponse({"error": "User doesnt have any followers."}, status=404)
    if request.user.username != username:
        if request.user in user_info.followers.all():
            return JsonResponse({"info":user_info.serialize(), "isFollow": "yes", "following": following.count(), "posts_count": posts.count(), "user": user.serialize(), "session_user": session_user }, safe=False)
        else:
            return JsonResponse({"info":user_info.serialize(), "isFollow": "no", "following": following.count(), "posts_count": posts.count(), "user": user.serialize(), "session_user": session_user }, safe=False)
    else:
        return JsonResponse({"info":user_info.serialize(), "button": "Your profile", "following": following.count(), "posts_count": posts.count(), "user": user.serialize(), "session_user": session_user }, safe=False)

def profile(request, username):
    user_profile = User.objects.get(username=username)
    publications = Publication.objects.filter(user_p=user_profile)
    return render(request, "devmo/profile.html", {"list": publications, "profile_user": user_profile})

@csrf_exempt
def newpost(request):
    if request.method == "GET":
        return render(request, "devmo/newpost.html")
    elif request.method == "POST":
        data = json.loads(request.body)
        if (data['content'] == "") or (data['title'] == "") or (data['image'] == ""):
            return JsonResponse({
                "error": "Publication cannot be empty."
            }, status=400)

        category = Categories.objects.get(categ=data.get("category"))
        content = data.get("content")
        title = data.get("title")
        image = data.get("image") 
        new_publication = Publication(
            content=content,
            user_p=request.user,
            title=title,
            image=image,
            category=category
        )
        new_publication.save()
        return JsonResponse(new_publication.serialize(), safe=False)
    else:
        return JsonResponse({"error": "POST or GET request required."}, status=400)

def category(request, category):
    post_categ = Categories.objects.get(categ=category)
    posts = Publication.objects.filter(category=post_categ)
    return JsonResponse([post.serialize() for post in posts ], safe=False)

def search(request):
    search_input = request.GET.get('search')
    object_list = Publication.objects.filter(Q(title__icontains=search_input) | Q(content__icontains=search_input))
    return render(request, "devmo/index.html", {"list": object_list})

@csrf_exempt
def bookmark(request, publication_id):
    user = request.user
    try:
        post = Publication.objects.get(pk=publication_id)
    except Publication.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.method == "GET":
        return JsonResponse({"error": f"{post}"}, status=404)

    elif request.method == "POST":
        if user in post.favorites.all():
            post.favorites.remove(user)
            return JsonResponse({"info": post.serialize(), "isBookmarked": "no"}, safe=False)
        else:
            post.favorites.add(user)
            return JsonResponse({"info": post.serialize(), "isBookmarked": "yes"}, safe=False)
        return HttpResponse(status=204)
    else:
        return JsonResponse({
            "error": "GET or POST request required."
        }, status=400)

def view_favorites(request):
    if request.method == "GET":
        publications = []
        user = request.user
        posts = Publication.objects.all()
        for post in posts:
            if user in post.favorites.all():
                publications.append(post.serialize())
        return render(request, "devmo/index.html", {"list": publications})
    else:
        return JsonResponse({
            "error": "GET request required."
        }, status=400)

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
            return render(request, "devmo/register.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "devmo/register.html")


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
            return render(request, "devmo/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            user_followers = User_followers(user_id=user)
            user_followers.save()
        except IntegrityError:
            return render(request, "devmo/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "devmo/register.html")
