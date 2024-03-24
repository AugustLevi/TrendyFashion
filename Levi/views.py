from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from django.contrib.auth import login,logout,authenticate
from Levi.models import Category,Products,Order,Size,UserProfile
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def home(request):
    return render(request,'home.html')

def test(request):
    return render(request,'category.html')

def register(request):
    if request.method == "POST":
        username = request.POST.get('name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            messages.error(request, "Your passwords didn't match!!")
            return render(request,'/signup/')
        else:
            myuser = User.objects.create_user(username,email,password1)
            myuser.save()
            messages.success(request,"Your account has been successfully created.")
            return redirect('/signin/')
    return render(request,'signup.html')

def signin(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        username = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=username,email=email, password=password) 
        if user is not None:
            login(request, user)
            if UserProfile.objects.filter(user=user).exists():
                return redirect('/home/')
            else:
                return redirect('/complete_profile/')
    return render(request,'login.html')

@login_required
def category_view(request):
    category = Category.objects.all()
    return render(request, 'category.html', {'category': category})
    
@login_required
def product_list(request,category_id):
    category = Category.objects.get(id=category_id)
    products = Products.objects.filter(category=category)
    return render(request,'product_list.html',{'products':products,'category':category})

def signout(request):
    logout(request)
    return redirect('/signin/') 
@login_required
def buy_now(request, product_id):
    # product = get_object_or_404(Products, pk=product_id)
    product = Products.objects.get(id=product_id)
    user = request.user
    if request.method == 'POST':
        name = request.POST.get('name')
        contact = request.POST.get('contact')
        address = request.POST.get('address')
        payment_method = request.POST.get('payment_method')
        quantity = int(request.POST.get('quantity', default = 1))
        size_id = request.POST.get('size') 
        selected_size = get_object_or_404(Size, pk=size_id) 
        # selected_size = Size.objects.get(id = size_id)
        total_price = quantity * product.price
        order = Order.objects.create(user=user, product=product, quantity=quantity, total_price=total_price, size=selected_size)
        context = {'product': product, 'order': order}
        return render(request, 'order.html', context)
    sizes = product.sizes.all() 
    context = {'product': product, 'sizes': sizes}
    return render(request, 'buynow_confirmation.html', context)
def edit_profile(request):
    user_profile = request.user.profile

    if request.method == 'POST':
        bio = request.POST.get('bio', '')
        profile_picture = request.FILES.get('profile_picture', None)

        user_profile.bio = bio
        if profile_picture:
            user_profile.profile_picture = profile_picture

        user_profile.save()
        return redirect('profile')  

    return render(request, 'edit_profile.html', {'user_profile': user_profile})
@login_required
def complete_profile(request):
    if request.method == "POST":
        bio = request.POST.get('bio')
        image = request.FILES.get('image')

        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        user_profile.bio = bio
        user_profile.profile_picture = image
        user_profile.save()

        return redirect('home') 

    return render(request, 'complete_profile.html')
@login_required
def add_to_cart(request, product_id):
    # product = get_object_or_404(Products, pk=product_id)
    product = Products.objects.get(id = product_id)
    user = request.user

    if request.method == 'POST':
        order, created = Order.objects.get_or_create(
            user=user,
            product=product,
            defaults={'quantity': 0, 'total_price': 0} 
        )
        order.quantity += 1
        order.total_price += product.price
        order.save()

        messages.success(request, f"{product.name} added to your cart.")
        return redirect('pdlist', category_id=product.category.id)
    return redirect('pdlist', category_id=product.category.id)
@login_required
def view_cart(request):
    user = request.user
    cart_items = Order.objects.filter(user=user)

    context = {
        'cart_items': cart_items,
    }

    return render(request, 'view_cart.html', context)

@login_required
def checkout(request):
    user = request.user
    cart_items = Order.objects.filter(user=user)
    total_price = sum(item.total_price for item in cart_items)

    if request.method == 'POST':
        name = request.POST.get('name')
        contact = request.POST.get('contact')
        address = request.POST.get('address')
        payment_method = request.POST.get('payment_method')
        cart_items.delete()
        return redirect('home')

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }

    return render(request, 'checkout.html', context)

@login_required
def confirm_checkout(request):
    user = request.user
    cart_items = Order.objects.filter(user=user)
    cart_items.delete()

    messages.success(request, "Checkout successful! Your order has been placed.")

    return redirect('checkout')

def custom_404_view(request):
    return render(request,'404.html',status=404)












