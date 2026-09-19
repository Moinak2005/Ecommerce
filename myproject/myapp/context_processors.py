from .models import Order, Category, WishlistItem

def cart_processor(request):
    cart_items = 0
    order = None
    items = []
    cart_quantities = {}
    wishlist_items = []
    wishlist_count = 0
    
    if request.user.is_authenticated:
        order = Order.objects.filter(user=request.user, is_complete=False).first()
        if order:
            cart_items = order.get_cart_items
            items = order.orderitem_set.all()
            cart_quantities = {item.product.id: item.quantity for item in items}
        
        wishlist_objs = WishlistItem.objects.filter(user=request.user)
        wishlist_items = [w.product for w in wishlist_objs]
        wishlist_count = wishlist_objs.count()
            
    global_categories = Category.objects.all()
    
    return {
        'cart_items_count': cart_items,
        'global_categories': global_categories,
        'cart_order': order,
        'cart_items': items,
        'cart_quantities': cart_quantities,
        'wishlist_items': wishlist_items,
        'wishlist_count': wishlist_count,
    }


