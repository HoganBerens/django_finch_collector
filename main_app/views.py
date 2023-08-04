from django.shortcuts import render

finches = [
    {"name": "Amy", "species": "American Goldfinch", "description": "Yellow with black wings", "age": 2},
    {"name": "Paul", "species": "House finch", "description": "Grey with red head and chest", "age": 5},
    {"name": "Clint", "species": "Hawfinch", "description": "Orange with brown and black wings", "age": 1}
]

# Create your views here.
def home(request):
    return render(request, "home.html")

def about(request):
    return render(request, "about.html")

def finches_index(request):
    return render(request, "finches/index.html", {"finches": finches})