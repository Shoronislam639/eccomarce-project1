from core.models import Product,Category,Vendor,CartOrderItems,CartOrder,wishlist,Address,ProductImage,ProductReviews
from ast import Add
from django.db.models import Min,Max
from django import template
from django.contrib import messages



def default(request): 
    categories=Category.objects.all() 
    vendors=Vendor.objects.all()
    
    
    min_max_price = Product.objects.aggregate(Min("price"), Max("price"))
    
   
    user_wishlist = []  
    if request.user.is_authenticated:
        user_wishlist = wishlist.objects.filter(user=request.user)

    try:
        address=Address.objects.get(user=request.user)   
    except:
        address=None
    return{ 
        "wishlist": user_wishlist,     
        "wishlist_count": len(user_wishlist), 
        "categories":categories,
        "address":address,
        "vendors":vendors,
        "min_max_price":min_max_price,
       }
    
    
# core/context_processors.py

def cart_context(request):
    cart_data = request.session.get('Cart_data_obj', {})
    return {
        'Cart_data': cart_data,
        'totalcartitems': len(cart_data),
        
    }



