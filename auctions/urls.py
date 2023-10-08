from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create/", views.create, name="create"),
    path("<int:auction_id>", views.listing, name="listing"), 
    path("<int:auction_id>", views.userlisting, name="userlisting"),
    path("watchlist/<int:item_id><int:user_id>", views.watchlist, name="watchlist"),
    path("userwatching", views.userwatching, name="userwatching"),
    path("bid/<int:item_id><int:user_id>", views.bid, name="bid"),
    path("mylistings/", views.mylistings, name="mylistings"),
    path("categories/", views.categories, name="categories"),
    path("category/<str:category>", views.category, name="category"),
    path("add_comment/<int:auction_id>", views.add_comment, name="add_comment"),
]
