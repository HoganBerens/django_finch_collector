from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Finch, Hat
from .forms import FeedingForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
def home(request):
    return render(request, "home.html")


def about(request):
    return render(request, "about.html")


@login_required
def finches_index(request):
    finches = Finch.objects.filter(user=request.user)
    return render(request, "finches/index.html", {"finches": finches})


@login_required
def finches_detail(request, finch_id):
    finch = Finch.objects.get(id=finch_id)
    id_list = finch.hats.all().values_list("id")
    hats_finch_doesnt_have = Hat.objects.exclude(id__in=id_list)
    feeding_form = FeedingForm()
    return render(
        request,
        "finches/detail.html",
        {"finch": finch, "feeding_form": feeding_form, "hats": hats_finch_doesnt_have},
    )


@login_required
def add_feeding(request, finch_id):
    # create a ModelForm instance using the data in request.POST
    form = FeedingForm(request.POST)
    # validate the form
    if form.is_valid():
        # don't save the form to the db until it
        new_feeding = form.save(commit=False)
        new_feeding.finch_id = finch_id
        new_feeding.save()
    return redirect("detail", finch_id=finch_id)


class FinchCreate(LoginRequiredMixin, CreateView):
    model = Finch
    fields = ["name", "species", "description", "age"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class FinchUpdate(LoginRequiredMixin, UpdateView):
    model = Finch
    fields = "__all__"


class FinchDelete(LoginRequiredMixin, DeleteView):
    model = Finch
    success_url = "/finches"


@login_required
def hats_index(request):
    hats = Hat.objects.all()
    return render(request, "hats/index.html", {"hats": hats})


@login_required
class HatCreate(CreateView):
    model = Hat
    fields = ["color", "fabric"]
    success_url = "/hats"


@login_required
def assoc_hat(request, finch_id, hat_id):
    Finch.objects.get(id=finch_id).hats.add(hat_id)
    return redirect("detail", finch_id=finch_id)


@login_required
def unassoc_hat(request, finch_id, hat_id):
    Finch.objects.get(id=finch_id).hats.remove(hat_id)
    return redirect("detail", finch_id=finch_id)


def signup(request):
    error_message = ""
    if request.method == "POST":
        # This is how to create a 'user' form object
        # that includes the data from the browser
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # This will add the user to the database
            user = form.save()
            # This is how we log a user in via code
            login(request, user)
            return redirect("index")
        else:
            error_message = "Invalid sign up - try again"
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {"form": form, "error_message": error_message}
    return render(request, "registration/signup.html", context)
