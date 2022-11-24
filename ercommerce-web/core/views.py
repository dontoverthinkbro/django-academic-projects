from django.shortcuts import render, redirect
from django.db.models import Q
# Create your views here.
from django.contrib.auth import login
from product.models import Product, Category
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required


def frontpage(request):
    # get first 8 products (latest because in model we -added_date)
    products = Product.objects.all()[0:8]
    return render(request, "core/frontpage.html", {"products": products})


def signup(request):
    # if click submit then this true
    print(request.method)
    if request.method == "POST":
        form = SignUpForm(request.POST)
        print("vo 1")

        if form.is_valid():
            print("vo 2")
            user = form.save()
            print("vo 3")
            login(request, user)
            print("vo 4")
            return redirect("/")
    else:
        form = SignUpForm()
        print("vo 5")
    # tuc la neu lan dau vao "signup" thi day la get, thi se tra lai form nay
    return render(request, "core/signup.html", {"form": form})


@login_required
def profile(request):
    print("no vo day")
    return render(request, "core/profile.html")


@login_required
def edit_profile(request):
    print(request.method)
    if request.method == "POST":
        user = request.user
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.email = request.POST.get("email")
        print(request.POST.get("first_name"), request.POST.get(
            "last_name"), request.POST.get("email"))
        user.save()
        # redirect se tro ve name variable trong urls.py
        return redirect("profile")

    return render(request, "core/edit_profile.html")


def shop(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    active_category = request.GET.get("category", "")

    if active_category:
        # private slug
        products = products.filter(category__slug=active_category)

    query = request.GET.get("txt_search", "")
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query))

    context = {
        "categories": categories,
        "active_category": active_category,
        "products": products
    }
    return render(request, "core/shop.html", context)
