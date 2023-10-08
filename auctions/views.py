from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Max
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from .models import User, AuctionListing, Bid, Watchlist, Comment


def index(request):
    
    return render(request, "auctions/index.html", {
        "auctions": AuctionListing.objects.filter(status=True),
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
    

def create(request):
    if request.method == "POST":
        item = request.POST["item"]
        description = request.POST["description"]
        image = request.POST["image"]
        category = request.POST["category"]
        starting_bid = request.POST["starting_bid"]
        user_id = request.user
        listing = AuctionListing(item=item, description=description, image=image, category=category, starting_bid=starting_bid, max_bid=0, user_id=user_id)
        listing.save()

        return HttpResponseRedirect(reverse("index"), {
            "message": "Listing Added"
        })
    return render(request, "auctions/create.html")


def listing(request, auction_id):
    print(auction_id)
    item = AuctionListing.objects.get(pk=auction_id)
    id = auction_id
    
    if not request.user.is_authenticated:
        return render(request, "auctions/listing.html", {
            "listing": item,
            "auction_id": auction_id
        })
    else:
        return userlisting(request, id)
    
    

# @login_required()
def userlisting(request, auction_id):
    if request.method == "POST":
        item = AuctionListing.objects.get(id=request.POST["status"])
        if item.status == True:
            item.status = False
        elif item.status == False:
            item.status = True
        item.save()
        print(item.status)

    item = AuctionListing.objects.get(pk=auction_id)

    person = str(item.user_id)

    if Watchlist.objects.filter(user=request.user, listing=item):
        watching = "Remove From Watchlist"
    else:
        watching = "Add To Watchlist"

    try:
        bids = Bid.objects.filter(listing=item).aggregate(Max("amount"))
        highest_bid = Bid.objects.get(amount=bids["amount__max"])
        highest_bidder = str(highest_bid.user)
    except:
        highest_bidder = ""
    
    comments = Comment.objects.filter(listing=item).order_by("date").reverse()
                                
    return render(request, "auctions/userlisting.html", {
            "listing": item,
            "watching": watching,
            "person": person,
            "highest_bidder": highest_bidder,
            "comments": comments
        })


def watchlist(request, item_id, user_id):
    if request.method == "POST":
        user = User.objects.get(pk=user_id)
        item = AuctionListing.objects.get(pk=item_id)

        if request.POST["watching"] == "Add To Watchlist":
            print("ADDED")
            watch = Watchlist.objects.create(
                user=user,
                listing=item
            )
            watch.save()
        elif request.POST["watching"] == "Remove From Watchlist":
            print("Removed") 
            Watchlist.objects.filter(user=request.user, listing=item).delete()
            
    if Watchlist.objects.filter(user=request.user, listing=item):
        watching = "Remove From Watchlist"
    else:
        watching = "Add To Watchlist"

    item = AuctionListing.objects.get(pk=item_id)

    person = str(item.user_id)

    try:
        bids = Bid.objects.filter(listing=item).aggregate(Max("amount"))
        highest_bid = Bid.objects.get(amount=bids["amount__max"])
        highest_bidder = str(highest_bid.user)
    except:
        highest_bidder = ""
        
    comments = Comment.objects.filter(listing=item)

    return render(request, "auctions/userlisting.html", {
        "listing": item,
        "watching": watching,
        "person": person,
        "highest_bidder": highest_bidder,
        "comments": comments
    })


def userwatching(request):
    watching = Watchlist.objects.filter(user=request.user)
    print(watching)
    print(AuctionListing.objects.all())

    for watch in watching:
        print(watch.id)

    return render(request, "auctions/userwatching.html", {
        "listings": watching
    })


def bid(request, item_id, user_id):
    if request.method == "POST":
        amount = request.POST["bid"]
        user = User.objects.get(pk=user_id)
        item = AuctionListing.objects.get(pk=item_id)
        print(amount, user, item)

        bids = Bid.objects.filter(listing=item).values_list('id', flat=True).aggregate(Max("amount"))
        print("Bid=", bids)
        print(item.max_bid)

        if Watchlist.objects.filter(user=request.user, listing=item):
            watching = "Remove From Watchlist"
        else:
            watching = "Add To Watchlist"

        comments = Comment.objects.filter(listing=item)

        try:
            if float(amount) > item.max_bid and float(amount) > item.starting_bid:
                bid = Bid.objects.create(
                amount=amount,
                user=user,
                listing=item
                )
                item.max_bid = float(amount)
                item.save()
                too_low = ""
            else:
                too_low = "Your Bid is Too Low."
        except:
            pass

    person = str(item.user_id)

    
    bids = Bid.objects.filter(listing=item).aggregate(Max("amount"))
    try:
        highest_bid = Bid.objects.get(amount=bids["amount__max"])
        highest_bidder = str(highest_bid.user)
    except:
        highest_bidder = None

    return render(request, "auctions/userlisting.html", {
        "listing": item,
        "highest_bidder": highest_bidder,
        "watching": watching,
        "comments": comments,
        "person": person,
        "too_low": too_low
    })


def mylistings(request):

    if request.method =="POST":
        item = AuctionListing.objects.get(id=request.POST["status"])
        if item.status == True:
            item.status = False
        elif item.status == False:
            item.status = True
        item.save()
        print(item.status)
        
        return render(request, "auctions/mylistings.html", {
        "listings": AuctionListing.objects.filter(user_id=request.user)
    })
    
    return render(request, "auctions/mylistings.html", {
        "listings": AuctionListing.objects.filter(user_id=request.user)
    })


def categories(request):
    category = AuctionListing.category
    return render(request, "auctions/categories.html")


def category(request, category):
    listings = AuctionListing.objects.filter(category=category, status=True)
    print(listings)
    return render(request, "auctions/category.html", {
        "listings": listings,
        "cat": category
    })


def add_comment(request, auction_id):
    if request.method == "POST":
        item = AuctionListing.objects.get(pk=auction_id)
        print(request.POST["comment"])
        com = Comment.objects.create(
            comment=request.POST["comment"],
            user=request.user,
            listing=item
            )

            
    if Watchlist.objects.filter(user=request.user, listing=item):
        watching = "Remove From Watchlist"
    else:
        watching = "Add To Watchlist"

    item = AuctionListing.objects.get(pk=auction_id)

    person = str(item.user_id)

    bids = Bid.objects.filter(listing=item).aggregate(Max("amount"))
    highest_bid = Bid.objects.get(amount=bids["amount__max"])
    highest_bidder = str(highest_bid.user)

    comments = Comment.objects.filter(listing=item).order_by("date").reverse()

    return render(request, "auctions/userlisting.html", {
        "listing": item,
        "watching": watching,
        "person": person,
        "highest_bidder": highest_bidder,
        "comments": comments
    })
