from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("finches/", views.finches_index, name="index"),
    path("finches/<int:finch_id>/", views.finches_detail, name="detail"),
    path("finches/create/", views.FinchCreate.as_view(), name="finches_create"),
    path(
        "finches/<int:pk>/update/", views.FinchUpdate.as_view(), name="finches_update"
    ),
    path(
        "finches/<int:pk>/delete/", views.FinchDelete.as_view(), name="finches_delete"
    ),
    path("finches/<int:finch_id>/add_feeding/", views.add_feeding, name="add_feeding"),
    path(
        "finches/<int:finch_id>/assoc_hat/<int:hat_id>/",
        views.assoc_hat,
        name="assoc_hat",
    ),
    path(
        "finches/<int:finch_id>/unassoc_hat/<int:hat_id>/",
        views.unassoc_hat,
        name="unassoc_hat",
    ),
    path("hats/create/", views.HatCreate.as_view(), name="hats_create"),
    path("hats/", views.hats_index, name="hats_index"),
    path("accounts/signup/", views.signup, name="signup"),
]
