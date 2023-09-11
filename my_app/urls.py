from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create-listing", views.CreateListing.as_view(), name="create-listing"),
    path("find", views.Find.as_view(), name="find"),
    path("filter", views.filter, name="filter"),
    path("user-listings", views.UserListing.as_view(), name="user-listings"),
    path("saved", views.Saved.as_view(), name="saved"),
    path("requests", views.requests, name="requests"),
    path("reset", views.reset, name="reset"),
    path("save/<int:listing_id>", views.save, name="save"),
    path("<int:listing_id>", views.listing_details, name="listing-details"),
]