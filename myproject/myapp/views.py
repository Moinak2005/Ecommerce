from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import CustomUserCreationForm, UserUpdateForm, UserProfileForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Category, Product, UserProfile, Order, OrderItem, WishlistItem
def apply_filters(request, products):
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    has_discount = request.GET.get('has_discount')
    
    if min_price and min_price.replace('.','',1).isdigit():
        products = products.filter(price__gte=float(min_price))
    if max_price and max_price.replace('.','',1).isdigit():
        products = products.filter(price__lte=float(max_price))
    if has_discount == 'true':
        products = products.filter(discount_price__isnull=False)
        
    stars = request.GET.get('stars')
    if stars and stars.isdigit():
        products = products.filter(rating__gte=int(stars))
        
    sort_by = request.GET.get('sort')
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    elif sort_by == 'best_sellers':
        from django.db.models import Sum, Q
        from django.db.models.functions import Coalesce
        products = products.annotate(
            total_sold=Coalesce(Sum('orderitem__quantity', filter=Q(orderitem__order__is_complete=True)), 0)
        ).order_by('-total_sold', '-id')
    elif sort_by == 'featured':
        products = products.order_by('-rating', '-rating_count', '-id')
    
    return products

# Create your views here.
def index(request):
    categories = Category.objects.all()
    from django.db.models import Sum, Q
    from django.db.models.functions import Coalesce
    products = Product.objects.filter(is_active=True)
    
    # Best Selling: Highest total quantity in completed orders
    best_selling = products.annotate(
        total_sold=Coalesce(Sum('orderitem__quantity', filter=Q(orderitem__order__is_complete=True)), 0)
    ).order_by('-total_sold', '-id')[:5]
    
    # Featured: Highest rated products
    featured = products.order_by('-rating', '-rating_count', '-id')[:5]
    
    # Popular: Most number of ratings
    popular = products.order_by('-rating_count', '-rating', '-id')[:5]
    
    latest = products.order_by('-created_at', '-id')[:5]
    
    carousel_category_names = [
        "Fruits and Vegetables", "Dairy and Eggs", "Meat and Poultry", 
        "Fish & Seafood", "Bakery and Bread", "Canned Goods", 
        "Frozen Foods", "Pasta and Rice", "Breakfast Foods", 
        "Snacks and Chips", "Beverages", "Baby Food and Formula", 
        "Health and Wellness", "Household Supplies", "Personal Care", 
        "Pet Food and Supplies", "Spices and Seasonings"
    ]
    # Preserve order of the list
    carousel_categories = []
    for name in carousel_category_names:
        for cat in categories:
            if cat.name == name:
                carousel_categories.append(cat)
                break
    
    context = {
        'categories': categories,
        'carousel_categories': carousel_categories,
        'best_selling': best_selling,
        'featured': featured,
        'popular': popular,
        'latest': latest,
    }
    return render(request, 'index.html', context)

def shop(request):
    categories = Category.objects.all()
    products = Product.objects.filter(is_active=True)
    products = apply_filters(request, products)
    return render(request, 'shop.html', {'categories': categories, 'products': products})

def search(request):
    q = request.GET.get('q', '')
    categories = Category.objects.all()
    if q:
        products = Product.objects.filter(is_active=True, name__icontains=q)
        products = apply_filters(request, products)
    else:
        products = Product.objects.none()
    return render(request, 'shop.html', {'categories': categories, 'products': products, 'search_query': q})

def category_view(request, slug):
    try:
        category = Category.objects.get(slug=slug)
        products = Product.objects.filter(category=category, is_active=True)
        products = apply_filters(request, products)
    except Category.DoesNotExist:
        messages.error(request, "Category not found.")
        return redirect('home')
    
    categories = Category.objects.all()
    context = {
        'category': category,
        'products': products,
        'categories': categories,
    }
    return render(request, 'shop.html', context)

def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')

@login_required(login_url='login')
def cart(request):
    order, created = Order.objects.get_or_create(user=request.user, is_complete=False)
    items = order.orderitem_set.all()
    return render(request, 'cart.html', {'order': order, 'items': items})

@login_required(login_url='login')
def add_to_cart(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        order, created = Order.objects.get_or_create(user=request.user, is_complete=False)
        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
        
        if request.method == 'POST':
            quantity = int(request.POST.get('quantity', 1))
            action = request.POST.get('action')
            
            if action == 'set':
                orderItem.quantity = quantity
            elif created:
                orderItem.quantity = quantity
            else:
                orderItem.quantity += quantity
        else:
            orderItem.quantity += 1
            
        if orderItem.quantity <= 0:
            orderItem.delete()
        else:
            orderItem.save()
    except Product.DoesNotExist:
        messages.error(request, "Product does not exist.")
        
    return redirect(request.META.get('HTTP_REFERER', 'shop'))

@login_required(login_url='login')
def remove_from_cart(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        order = Order.objects.filter(user=request.user, is_complete=False).first()
        if order:
            orderItem = OrderItem.objects.filter(order=order, product=product).first()
            if orderItem:
                orderItem.delete()
    except Product.DoesNotExist:
        pass
    return redirect(request.META.get('HTTP_REFERER', 'cart'))

@login_required(login_url='login')
def clear_cart(request):
    if request.method == 'POST':
        order = Order.objects.filter(user=request.user, is_complete=False).first()
        if order:
            order.orderitem_set.all().delete()
            messages.success(request, "Your cart has been cleared.")
    return redirect(request.META.get('HTTP_REFERER', 'cart'))

import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

@login_required(login_url='login')
def checkout(request):
    if not request.user.is_superuser:
        if not hasattr(request.user, 'profile') or not request.user.profile.is_complete():
            messages.warning(request, "Please complete your profile (Address and Phone Number) before confirming your order.")
            return redirect('account')
            
    order, created = Order.objects.get_or_create(user=request.user, is_complete=False)
    items = order.orderitem_set.all()
    
    if not items.exists():
        messages.error(request, "You cannot checkout with an empty cart.")
        return redirect('cart')
    
    if request.method == 'POST':
        payment_method = request.POST.get('paymentMethod', 'cod')
        if payment_method == 'cod':
            import uuid
            order.transaction_id = str(uuid.uuid4())
            order.is_complete = True
            order.save()
            messages.success(request, "Your order has been placed successfully via Cash on Delivery!")
            return redirect('home')
            
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    
    amount = int(order.get_cart_total * 100) # Amount in paise
    try:
        razorpay_order = client.order.create({
            "amount": amount,
            "currency": "INR",
            "payment_capture": "1"
        })
        order.transaction_id = razorpay_order['id']
        order.save()
    except Exception as e:
        messages.error(request, f"Error communicating with payment gateway: {str(e)}")
        return redirect('cart')
        
    context = {
        'order': order,
        'items': items,
        'razorpay_order_id': razorpay_order['id'],
        'razorpay_merchant_key': settings.RAZORPAY_KEY_ID,
        'razorpay_amount': amount,
        'currency': 'INR',
    }
    return render(request, 'checkout.html', context)

@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_signature = request.POST.get('razorpay_signature')
        
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }
        try:
            client.utility.verify_payment_signature(params_dict)
            order = Order.objects.get(transaction_id=razorpay_order_id, is_complete=False)
            order.is_complete = True
            order.save()
            messages.success(request, "Payment successful! Your order has been placed.")
            return redirect('home')
        except razorpay.errors.SignatureVerificationError:
            messages.error(request, "Payment verification failed. Please try again.")
            return redirect('checkout')
        except Order.DoesNotExist:
            messages.error(request, "Order not found or already completed.")
            return redirect('home')
    return redirect('home')

@login_required(login_url='login')
def account_view(request):
    profile = getattr(request.user, 'profile', None)
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            # Link profile to user if it didn't exist before
            profile = profile_form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('account')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=profile)
        
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'account.html', context)

@login_required(login_url='login')
def orders_view(request):
    orders = Order.objects.filter(user=request.user, is_complete=True).order_by('-date_ordered')
    return render(request, 'orders.html', {'orders': orders})

def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("home")
        
        # Display specific form validation errors as alert messages
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"{error}")
    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form})

from django.db.models import Q
from django.contrib.auth import get_user_model

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("home")
            else:
                messages.error(request, "Invalid login credentials.")
        else:
            # Form is invalid, let's provide specific feedback
            username = request.POST.get('username')
            password = request.POST.get('password')
            User = get_user_model()
            user = User.objects.filter(Q(username__iexact=username) | Q(email__iexact=username)).first()
            if not user:
                messages.error(request, "Invalid email or username.")
            elif not user.check_password(password):
                messages.error(request, "Invalid password.")
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("home")

@login_required
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    item, created = WishlistItem.objects.get_or_create(user=request.user, product=product)
    
    if not created:
        item.delete()
        messages.success(request, f"{product.name} removed from your wishlist!")
    else:
        messages.success(request, f"{product.name} added to your wishlist!")
        
    return redirect(request.META.get('HTTP_REFERER', 'shop'))

from django.http import JsonResponse
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg

@csrf_exempt
def rate_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if not request.session.session_key:
        request.session.create()
    
    from myapp.models import UserRating
    
    if request.user.is_authenticated:
        user_rating = UserRating.objects.filter(product=product, user=request.user).first()
    else:
        user_rating = UserRating.objects.filter(product=product, session_key=request.session.session_key, user__isnull=True).first()

    if request.method == 'GET':
        if user_rating:
            return JsonResponse({
                'score': user_rating.score,
                'review_text': user_rating.review_text or '',
                'image_url': user_rating.image.url if user_rating.image else ''
            })
        return JsonResponse({'score': 0, 'review_text': '', 'image_url': ''})

    if request.method == 'POST':
        if request.GET.get('action') == 'delete':
            if user_rating:
                user_rating.delete()
            avg = product.user_ratings.filter(score__gt=0).aggregate(Avg('score'))['score__avg'] or 0
            count = product.user_ratings.filter(score__gt=0).count()
            product.rating = Decimal(avg)
            product.rating_count = count
            product.save()
            return JsonResponse({'success': True, 'new_rating': float(product.rating), 'new_count': product.rating_count})
        
        try:
            score = int(request.POST.get('score', 0))
            if score < 0 or score > 5:
                return JsonResponse({'error': 'Invalid score'}, status=400)
            
            review_text = request.POST.get('review_text', '')
            image = request.FILES.get('image')
            
            if user_rating:
                user_rating.score = score
                user_rating.review_text = review_text
                if image:
                    user_rating.image = image
                elif request.POST.get('remove_image') == '1':
                    user_rating.image = None
                user_rating.save()
            else:
                if request.user.is_authenticated:
                    UserRating.objects.create(product=product, user=request.user, score=score, review_text=review_text, image=image)
                else:
                    UserRating.objects.create(product=product, session_key=request.session.session_key, user=None, score=score, review_text=review_text, image=image)
            
            # Recalculate true average, excluding 0 scores
            avg = product.user_ratings.filter(score__gt=0).aggregate(Avg('score'))['score__avg'] or 0
            count = product.user_ratings.filter(score__gt=0).count()
            
            product.rating = Decimal(avg)
            product.rating_count = count
            product.save()
            
            return JsonResponse({
                'success': True,
                'new_rating': float(product.rating),
                'new_count': product.rating_count
            })
        except (ValueError, TypeError):
            return JsonResponse({'error': 'Invalid format'}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def product_reviews(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    from myapp.models import UserRating
    from django.db.models import Q
    reviews = UserRating.objects.filter(product=product).exclude(
        Q(score=0) & 
        (Q(review_text__isnull=True) | Q(review_text='')) & 
        (Q(image__isnull=True) | Q(image=''))
    ).select_related('user').order_by('-id')
    review_list = []
    for r in reviews:
        is_own = False
        if request.user.is_authenticated and r.user == request.user:
            is_own = True
        elif not request.user.is_authenticated and r.session_key and r.session_key == request.session.session_key:
            is_own = True
        review_list.append({
            'username': r.user.username if r.user else 'Anonymous',
            'score': r.score,
            'review_text': r.review_text or '',
            'image_url': r.image.url if r.image else '',
            'is_own': is_own,
        })
    return JsonResponse({'reviews': review_list})


from django.views.decorators.http import require_POST
from django.db import transaction
from .ai_services import get_ai_stylist_recommendation
import json

@require_POST
def ai_stylist_chat(request):
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        if not user_message:
            return JsonResponse({'error': 'Prompt cannot be empty'}, status=400)
            
        chat_history = request.session.get('ai_chat_history', [])

        ai_reply = get_ai_stylist_recommendation(user_message, request.user, chat_history)
        
        chat_history.append({'role': 'user', 'text': user_message})
        chat_history.append({'role': 'model', 'text': ai_reply})
        request.session['ai_chat_history'] = chat_history[-10:]
        
        return JsonResponse({'reply': ai_reply})

    except Exception as e:
        error_msg = str(e) if str(e).strip() else repr(e)
        print(f"AI Chatbot Error: {error_msg}")
        return JsonResponse({'error': error_msg}, status=500)

@require_POST
def add_bundle_to_cart(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Please log in to add items to cart'}, status=401)

    data = json.loads(request.body)
    product_ids = data.get('product_ids', [])

    if not product_ids:
        return JsonResponse({'error': 'No items selected'}, status=400)

    added_items = []
    with transaction.atomic():
        order, created = Order.objects.get_or_create(user=request.user, is_complete=False)
        for pid in product_ids:
            product = get_object_or_404(Product, id=pid, is_active=True)
            cart_item, created = OrderItem.objects.get_or_create(
                order=order,
                product=product,
            )
            cart_item.quantity = (cart_item.quantity or 0) + 1
            cart_item.save()
            added_items.append(product.name)

    return JsonResponse({
        'status': 'success',
        'message': f'Added {len(added_items)} items to your cart!',
        'items': added_items
    })

