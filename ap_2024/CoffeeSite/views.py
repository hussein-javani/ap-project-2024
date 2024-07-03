from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate , logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import *
from django.db.models import Sum
from django.views.decorators.http import require_POST
from .forms import *
from django.http import HttpResponse, HttpResponseBadRequest, HttpRequest
import datetime

@login_required(login_url="login")
def home_view(request):
    
    # default home view: most ordered products
    if not request.GET.get("vertical"):
        # TODO: getting most ordered products

        products = Products.objects.all()
        
        products = Products.objects.annotate(total_count=Sum('orders_product__quantity'))
        products = products.order_by('-total_count')[0:10]
        
        title = "محصولات پر فروش"
        slideshow = True

    
    # filtering based on vertical
    if request.GET.get("vertical"):
        vertical = request.GET.get("vertical")

        if vertical == "all":
            products = Products.objects.all()
        else:
            products = Products.objects.filter(vertical=vertical)

        vertical_names = {  
                            "warm_drink": "نوشیدنی‌های گرم",
                            "cold_drink":"نوشیدنی‌های سرد",
                            "cake":"کیک‌ها",
                            "all":"همه محصولات",
                        }
        title = vertical_names[vertical]
        slideshow = False
    

    # check if there is enough storage items
    storage_flour = Storage.objects.get(name="flour")
    storage_raw_coffee = Storage.objects.get(name="raw_coffee")
    storage_sugar = Storage.objects.get(name="sugar")
    storage_chocolate = Storage.objects.get(name="chocolate")
        
    for prod in products:
        # prepare image urls for static load
        prod.image = str(prod.image).replace("CoffeeSite/","")
        # thousand seperator ( e.g.: 1,000,000 )
        prod.price = f"{prod.price:,}"

        if prod.flour > storage_flour.amount or \
        prod.raw_coffee > storage_raw_coffee.amount or \
        prod.chocolate > storage_chocolate.amount or \
        prod.sugar > storage_sugar.amount :
            
            prod.available = False
        else:
            prod.available = True
        

        

    
        
    return render(request, "home.html", {"title":title , "products":products, "slideshow":slideshow})
    



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
def stats_view(request):
    if not request.user.is_superuser:
        return render(request, "message.html", {"message_title":"ارور ۴۰۳", "message_body":"شما به این صفحه دسترسی ندارید"})

    all_products = Products.objects.all()
    if request.method == "GET":
        return render(request, "stats.html", {"products":all_products})
    if request.method == "POST":
        data = {}
        
        from_date = request.POST.get("from-date")
        from_date_list = from_date.split("-")
        to_date = request.POST.get("to-date")
        to_date_list = to_date.split("-")

        date_to_add = ""
        i = 0
        while True:
            date_to_add = datetime.date(int(from_date_list[0]), int(from_date_list[1]), int(from_date_list[2])) + datetime.timedelta(i)
            data[str(date_to_add)] = 0
            if str(date_to_add) == to_date:
                break
            i+=1
        
        
        orders = Orders.objects.filter(date__range=[request.POST.get("from-date"), request.POST.get("to-date")], open="False")
        products = Orders_Product.objects.filter( order_id__in=orders, product_id__id=request.POST.get("product") )
        for product in products:
            data[datetime.datetime.strftime(product.order_id.date, "%Y-%m-%d")] +=1
        
            
            
            
            

        return render(request, "stats.html", {"data_dict":data, "products":all_products, "data_product_name":products[0].product_id.name})

        




@login_required(login_url="login")
def storage_view(request) : 
    if not request.user.is_superuser:
        return render(request, "message.html", {"message_title":"ارور ۴۰۳", "message_body":"شما به این صفحه دسترسی ندارید"})

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
    if not request.user.is_superuser:
        return render(request, "message.html", {"message_title":"ارور ۴۰۳", "message_body":"شما به این صفحه دسترسی ندارید"})

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

@login_required(login_url="login")
def cart_view(request, message=""):
    msg_dict = {
        "add_product_ok": "محصول به سبد خرید اضافه شد",
        "remove_ok": "محصول از سبد خرید حذف شد",
        "takeout_ok": "نحوه ارسال با موفقیت تغییر کرد",
        "update_quantity_ok": "تعداد محصول با موفقیت تغییر کرد",
    }
    if request.GET.get("msg") in msg_dict.keys():
        message = msg_dict[ request.GET.get("msg") ]
    else:
        message = ""

    try:
        open_order = Orders.objects.get(username=request.user.username, open=True)
        items = Orders_Product.objects.filter(order_id=open_order)
        order_id = open_order.order_id
        is_takeout = open_order.is_takeout
    except:
        order_id = None
        is_takeout = None
        items = []
    
    total_price = 0
    for item in items:
        item.product_id.image = str(item.product_id.image).replace("CoffeeSite", "")
        total_price += item.product_id.price*item.quantity 
    total_price + 20000*is_takeout
    
    return render(request, "cart.html", {"items":items, "total":f'{total_price:,}', "message":message, "order_id": order_id, "is_takeout": is_takeout})

@login_required(login_url="login")
@require_POST
def add_to_cart_view(request):
    
    #check if user has open order:
    try:
        open_order = Orders.objects.get(username=request.user.username, open=True)
    #create new order :
    except:
        open_order = Orders(username=request.user.username)
        open_order.save()
    
    # get requested product object
    product = Products.objects.get(id=request.POST.get("product_id"))

    # check if the product is already added to cart
    try:
        order_product = Orders_Product.objects.get(order_id=open_order, product_id=product)
        order_product.quantity += 1

    # creating new order-product relation
    except:
        order_product =  Orders_Product(
            order_id = open_order,
            product_id = product,
            quantity = 1,
        )
        
    order_product.save()

    return redirect("/cart/?msg=add_product_ok")
    
@login_required(login_url="login")
@require_POST
def remove_product_view(request):
    Orders_Product.objects.get(id=request.POST.get("item-id")).delete()
    
    return redirect("/cart/?msg=remove_ok")

@login_required(login_url="login")
@require_POST
def update_product_view(request):
    item = Orders_Product.objects.get(id=request.POST.get("item-id"))
    item.quantity = request.POST.get("quantity")
    item.save()
    
    return redirect("/cart/?msg=update_quantity_ok")
    
@login_required(login_url="login")
@require_POST
def take_out_view(request):
    order = Orders.objects.get(order_id=request.POST.get("order-id"))
    if request.POST.get("takeout") == "0":
        order.is_takeout = False
    else:
        order.is_takeout = True
    
    order.save()
    
    return redirect("/cart/?msg=takeout_ok")

@require_POST
@login_required(login_url="login")
def finalize_order_view(request):
    try:
        open_order = Orders.objects.get(username=request.user.username, open=True)
    except:
        return message_view(request, title="ارور ۴۰۰", body="عملیات موفقیت آمیز نبود")
    
    open_order.open = False
    open_order.save()

    storage_flour = Storage.objects.get(name="flour")
    storage_raw_coffee = Storage.objects.get(name="raw_coffee")
    storage_sugar = Storage.objects.get(name="sugar")
    storage_chocolate = Storage.objects.get(name="chocolate")

    order_products = Orders_Product.objects.filter(order_id=open_order)

    for order_product in order_products:
        product = order_product.product_id
        # check if there is enough storage items
        if  product.flour * order_product.quantity > storage_flour.amount and \
            product.raw_coffee * order_product.quantity > storage_raw_coffee.amount and \
            product.chocolate * order_product.quantity > storage_chocolate.amount and \
            product.sugar * order_product.quantity > storage_sugar.amount :
            return HttpResponse("400 - Not enough storage items")
        
        # updating storage
        storage_chocolate.amount -= product.chocolate * order_product.quantity
        storage_sugar.amount -= product.sugar * order_product.quantity
        storage_raw_coffee.amount -= product.raw_coffee * order_product.quantity
        storage_flour.amount -= product.flour * order_product.quantity


    storage_chocolate.save()
    storage_sugar.save()
    storage_raw_coffee.save()
    storage_flour.save()
    
    return message_view(request, title="سفارش شما با موفقیت ثبت شد.", body="از اینکه استارداکس را انتخاب کردید سپاس گزاریم.")
    

@require_POST
@login_required(login_url="login")
def delete_order_view(request):
    
    Orders.objects.get(username=request.user.username, open=True).delete()
    return redirect("cart")

@login_required(login_url="login")
def history_view(request):
    orders = Orders.objects.filter(username=request.user.username, open=False)
    for order in orders:
        order.items = Orders_Product.objects.filter(order_id=order)
        order.delivery_cost = order.is_takeout*20000
        order.total = 0
        for item in order.items:
            order.total += item.product_id.price
        order.totla += order.delivery_cost
    return render(request, "orderhistory.html", {"orders":orders,})


def redirect_stats(request):
    return redirect("stats")


def message_view(request, title, body):
    return render(request, "message.html", {"message_title":title, "message_body":body,})




