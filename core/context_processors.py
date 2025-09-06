from core.models import Product,Category,Vendor,CartOrderItems,CartOrder,wishlist,Address,ProductImage,ProductReviews

def default(request):
    categories=Category.objects.all()
    return{
        "categories":categories
    }