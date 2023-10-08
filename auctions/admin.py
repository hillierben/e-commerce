from django.contrib import admin
from .models import User, AuctionListing, Bid, Comment, Watchlist

# Register your models here.
class AuctionListingAdmin(admin.ModelAdmin):
    list_display = ["id", "item", "description", "starting_bid", "image", "created", "user_id"]


class BidAdmin(admin.ModelAdmin):
    list_display = ["id", "amount", "item", "user"]


class WatchlistAdmin(admin.ModelAdmin):
    list_display = ["id", "item", "user"]


class CommentAdmin(admin.ModelAdmin):
    list_display = ["comment", "item", "user", "date"]


admin.site.register(AuctionListing, AuctionListingAdmin)
admin.site.register(User)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Watchlist, WatchlistAdmin)