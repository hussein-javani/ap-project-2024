from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate , logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import *
from django.views import View
from .forms import *
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required

@login_required(login_url="login")
def home_view(request):
    if request.method == "GET":
        if not request.GET.get("vertical"):
            # TODO: getting most ordered products

            products = Products.objects.all()[0:10]
            for prod in products:
                prod.image = str(prod.image).replace("CoffeeSite/","")
            
            return render(request, "home.html", {"title":"محصولات پر فروش", "products":products, "slideshow":True})
        
        if request.GET.get("vertical"):
            vertical = request.GET.get("vertical")
            products = Products.objects.filter(vertical=vertical)
            for prod in products:
                prod.image = str(prod.image).replace("CoffeeSite/","")
            
            vertical_names = {"warm_drink": "نوشیدنی‌های گرم", "cold_drink":"نوشیدنی‌های سرد", "cake":"کیک‌ها"}

            return render(request, "home.html", {"title":vertical_names[vertical] , "products":products, "slideshow":False })
        



def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username_or_email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # redirect to admind page if user is admin
                if user.is_staff or user.is_superuser:
                    return redirect("stats")
                else:
                    #redirect to home page if user is not admin
                    return redirect('home')
            else:
                # return HttpResponse("User not valid", status=401)
                return render( request, "login.html", { "form":form, "error" : "نام کاربری یا رمز عبور اشتباه است"})
                
    else:
        # if request is GET, just show the empty form
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form, "error":""})

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # Extract cleaned data
            full_name = form.cleaned_data.get('full_name')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            # Create a new user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            user.full_name = full_name
            user.save()

            # Log the user in
            login(request, user)
           
            return redirect('home')  # Redirect to your home page
        else:
            return render(request, "signup.html", {"form":form, "error":"اطلاعات وارد شده معتبر نمی‌باشد"})
    else:
        form = SignupForm()
    
    return render(request, 'signup.html', {'form': form})

@login_required(login_url="login")
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to the homepage

@login_required(login_url="login")
def storage_view(request) : 
    if request.method == 'POST':
        form = WarehouseManagementForm(request.POST)
        if form.is_valid():
            # Get the form data
            sugar_amount = form.cleaned_data['sugar']
            raw_coffee_amount = form.cleaned_data['raw_coffee']
            flour_amount = form.cleaned_data['flour']
            chocolate_amount = form.cleaned_data['chocolate']

            # Update the Storage records
            if sugar_amount or sugar_amount==0:
                Storage.objects.filter(name='sugar').update(amount=int(sugar_amount))
            if raw_coffee_amount or raw_coffee_amount == 0:
                Storage.objects.filter(name='raw_coffee').update(amount=int(raw_coffee_amount))
            if flour_amount or flour_amount == 0: 
                Storage.objects.filter(name='flour').update(amount=int(flour_amount))
            if chocolate_amount or chocolate_amount==0:
                Storage.objects.filter(name='chocolate').update(amount=int(chocolate_amount))

            form = WarehouseManagementForm()
            sugar_amount = Storage.objects.get(name='sugar').amount
            raw_coffee_amount = Storage.objects.get(name='raw_coffee').amount
            flour_amount = Storage.objects.get(name='flour').amount
            chocolate_amount = Storage.objects.get(name='chocolate').amount
            return render(request , "storage.html" , {'form' : form, "sugar":sugar_amount, "chocolate":chocolate_amount, "raw_coffee":raw_coffee_amount, "flour":flour_amount, "message":"تغییرات با موفقیت اعمال شد.", "error":""})
        else:
            form = WarehouseManagementForm()
            sugar_amount = Storage.objects.get(name='sugar').amount
            raw_coffee_amount = Storage.objects.get(name='raw_coffee').amount
            flour_amount = Storage.objects.get(name='flour').amount
            chocolate_amount = Storage.objects.get(name='chocolate').amount
            return render(request , "storage.html" , {'form' : form, "sugar":sugar_amount, "chocolate":chocolate_amount, "raw_coffee":raw_coffee_amount, "flour":flour_amount, "message":"", "error":"اطلاعات ارسال شده معتبر نمی باشد."})  # Redirect to a success page or the home page
    
            
    else:
        form = WarehouseManagementForm()
        sugar_amount = Storage.objects.get(name='sugar').amount
        raw_coffee_amount = Storage.objects.get(name='raw_coffee').amount
        flour_amount = Storage.objects.get(name='flour').amount
        chocolate_amount = Storage.objects.get(name='chocolate').amount
        return render(request , "storage.html" , {'form' : form, "sugar":sugar_amount, "chocolate":chocolate_amount, "raw_coffee":raw_coffee_amount, "flour":flour_amount, "message":"", "error":""})  # Redirect to a success page or the home page
    

@login_required(login_url="login")
def add_product_view(request) : 
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            # Create a new Product instance
            product = Products(
                name=form.cleaned_data['name'],
                sugar=form.cleaned_data['sugar'],
                raw_coffee=form.cleaned_data['raw_coffee'],
                flour=form.cleaned_data['flour'],
                chocolate=form.cleaned_data['chocolate'],
                price=form.cleaned_data['price'],
                image=form.cleaned_data['image'],
                vertical=form.cleaned_data['vertical']
            )
            product.save()
            form = AddProductForm()
            return render(request , "add-product.html" , {"form" : form , "message" : "تغییرات با موفقیت اعمال شد" , "error" : ""})
        else : 
            form = AddProductForm()
            return render(request , "add-product.html" , {"form" : form , "message" : "" , "error" : "اطلاعات وارد شده معتبر نمی باشد."})
    else:
        form = AddProductForm()
        return render(request , "add-product.html" , {"form" : form , "message" : "" , "error" : ""})


def cart_view(request):
    
    open_orders = Orders.objects.filter(username=request.user.username, open=True).all()
    items = Orders_Product.objects.filter(order_id__in=open_orders)
    
    total_price = 0
    for item in items:
        item.product_id.image = str(item.product_id.image).replace("CoffeeSite", "")
        total_price += item.product_id.price
    
    return render(request, "cart.html", {"items":items, "total":total_price})


def add_to_cart_view(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Bad request")
    
    #check if user has open order:
    try:
        open_order = Orders.objects.get(username=request.user.username, open=True)
    except:
        open_order = Orders(username=request.user.username)
        open_order.save()
    
    product = Products.objects.get(id=request.POST.get("product_id"))

    order_product =  Orders_Product(
        order_id = open_order,
        product_id = product,
        quantity = 1,
    )
    order_product.save()

    return redirect("cart")
    

