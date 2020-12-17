from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.http.response import Http404
from django.db.models import Max
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .forms import CommentForm, ListingForm, BidForm
from .models import *


def index(request):
    listings = Listing.objects.exclude(is_active=False)
    context = {
        "listings": listings
    }
    return render(request, "auctions/index.html", context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")


@login_required(login_url="/login")
def watch_view(request):
    # pass
    if request.method == "POST":
        id = request.POST.get("id", None)
        if id:
            listing = Listing.objects.get(pk=id)
            user = request.user
            watching_query = Watching.objects.get_or_create(
                listing=listing, user=user)  # returns tuple(Queryobj, Boolen)
            watching = watching_query[0]
            watching.watching = False if watching.watching else True
            watching.save()
            return HttpResponseRedirect(reverse("auctions:detail", args=[listing.id]))
        else:
            return Http404()
    else:
        user = request.user
        watchings = user.watching.exclude(watching=False)
        context = {
            "watchings": watchings
        }
        return render(request, "auctions/watch.html", context)


@login_required(login_url="/login")
def create_view(request):
    form = ListingForm(request.POST or None)
    if form.is_valid():
        # For adding creater
        listing = form.save(commit=False)
        listing.creater = request.user
        # Many to many fields reqirement first save and add related field
        listing.save()
        categories = request.POST.getlist('categories', None)
        if categories:
            for id in categories:
                category = Category.objects.get(id=id)
                listing.categories.add(category)
        return HttpResponseRedirect(reverse("auctions:detail", args=[listing.id]))
    context = {
        "form": form
    }
    return render(request, "auctions/create.html", context)


def detail_view(request, id):
    listing = get_object_or_404(Listing, id=id)
    categories = listing.categories.all()
    comments = listing.comments.all()
    context = {
        "listing": listing,
        "categories": categories,
        "comments": comments,
        "color": ["primary", "info", "success", "warning"]
    }
    # Get winner if auctions closed
    if listing.is_active == False:
        price = listing.bids.aggregate(Max("price"))["price__max"]
        winner = listing.bids.get(price=price).user
        context["winner"] = winner
    # Make listing price increase after a bid
    if request.method == "POST":
        bid = BidForm(request.POST)
        if bid.is_valid():
            offer = int(request.POST["price"])
            if offer > listing.price:
                bid = Bid(user=request.user, listing=listing, price=offer)
                bid.save()
                listing.price = offer
                listing.save()
            else:
                context[
                    "message"] = f"Bid must be greater than current price. Your offer was, ${offer}."
    # Extra details for authenticated users
    if request.user.is_authenticated:
        watching_query = Watching.objects.get_or_create(
            listing=listing, user=request.user)  # returns tuple(Queryobj, Boolen)
        watching = watching_query[0]
        context["watching"] = watching
        context["form"] = BidForm()
        # if user made a bid before
        bid_done = listing.bids.filter(user=request.user).exists()
        context["bid_done"] = bid_done
        # Commentform for user
        context["comment_form"] = CommentForm()

    return render(request, "auctions/detail.html", context)


def close_view(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        listing.is_active = False
        listing.save()
    return HttpResponseRedirect(reverse("auctions:detail", args=[listing_id]))


def categories_view(request):
    categories = Category.objects.all()
    context = {
        "categories": categories
    }
    return render(request, "auctions/categories.html", context)


def category_list_view(request, category_id):
    category = Category.objects.get(pk=category_id)
    listings = category.listings.all()
    context = {
        "category": category,
        "listings": listings
    }
    return render(request, "auctions/category_list.html", context)


@login_required(login_url="/login")
def comment_view(request, listing_id):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            user = request.user
            listing = Listing.objects.get(pk=listing_id)
            comment = request.POST["comment"]
            Comment.objects.create(user=user, listing=listing, comment=comment)
    return HttpResponseRedirect(reverse("auctions:detail", args=[listing_id]))
