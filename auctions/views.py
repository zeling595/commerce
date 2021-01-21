from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.forms import ModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing

class ListingForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ListingForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
        })

    class Meta:
        model = Listing
        fields = ['title', 'description', 'current_price', 'image', 'category']

def index(request):
    return render(request, "auctions/index.html", {
        "active_listings" : Listing.objects.all()
    })

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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def createListing(request):
    if request.method == "POST":
        listing_data = ListingForm(request.POST, request.FILES)
        if listing_data.is_valid():
            title = listing_data['title']
            description = listing_data.cleaned_data['description']
            current_price = listing_data.cleaned_data['current_price']
            if listing_data.cleaned_data['image']:
                image = listing_data.cleaned_data['image']
            else:
                image = None
            category = listing_data.cleaned_data['category']
            listing = Listing(title=title, description=description, current_price=current_price, image=image, category=category)
            listing.save()
            return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/createListing.html", {
        "listingForm" : ListingForm()
    })