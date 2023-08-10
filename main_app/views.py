from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Finch, Hat
from .forms import FeedingForm


# Create your views here.
def home(request):
    return render(request, "home.html")


def about(request):
    return render(request, "about.html")


def finches_index(request):
    finches = Finch.objects.all()
    return render(request, "finches/index.html", {"finches": finches})


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


class FinchCreate(CreateView):
    model = Finch
    fields = ["name", "species", "description", "age"]


class FinchUpdate(UpdateView):
    model = Finch
    fields = "__all__"


class FinchDelete(DeleteView):
    model = Finch
    success_url = "/finches"


def hats_index(request):
    hats = Hat.objects.all()
    return render(request, "hats/index.html", {"hats": hats})


class HatCreate(CreateView):
    model = Hat
    fields = ["color", "fabric"]
    success_url = "/hats"


def assoc_hat(request, finch_id, hat_id):
    Finch.objects.get(id=finch_id).hats.add(hat_id)
    return redirect("detail", finch_id=finch_id)


def unassoc_hat(request, finch_id, hat_id):
    Finch.objects.get(id=finch_id).hats.remove(hat_id)
    return redirect("detail", finch_id=finch_id)
