from core.models import Product,Category,Vendor,CartOrderItems,CartOrder,wishlist,Address,ProductImage,ProductReviews
from ast import Add
from django.db.models import Min,Max
from django import template


def default(request): 
    categories=Category.objects.all() 
    vendors=Vendor.objects.all()
    
    
    min_max_price = Product.objects.aggregate(Min("price"), Max("price"))
    
    try:
        address=Address.objects.get(user=request.user) 
        
    except:
        address=None
    return{ 
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



