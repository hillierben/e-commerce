from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Max


class User(AbstractUser):
    pass


class AuctionListing(models.Model):
    item = models.CharField(max_length=64)
    description = models.TextField(max_length=1000)
    image = models.URLField()
    starting_bid = models.FloatField(max_length=64)
    max_bid = models.FloatField(blank=True, max_length=64, default=0)
    category = models.CharField(blank=True, max_length=64)
    created = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    status = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Item: {self.item}, Description: {self.description}, Starting Bid: {self.starting_bid}, Created: {self.created}"


class Bid(models.Model):
    amount = models.FloatField(default=0, max_length=64)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, default=0, related_name="bids")

    def item(self):
        return self.listing.item


class Comment(models.Model):
    comment = models.TextField(max_length=200, default="Add Comment")
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, default=0, related_name="comment")

    def item(self):
        return self.listing.item


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, default=0, related_name="userwatch")
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)

    def item(self):
        return self.listing.item
    def description(self):
        return self.listing.description
    def image(self):
        return self.listing.image
    def starting_bid(self):
        return self.listing.starting_bid
    def category(self):
        return self.listing.category
    def max_bid(self):
        return self.listing.max_bid
    
    
    