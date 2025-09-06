from django.shortcuts import render
from core.models import Product,Category,Vendor,CartOrderItems,CartOrder,wishlist,Address,ProductImage,ProductReviews
from django.db.models import Count

def home(request):
    
    products = Product.objects.filter(product_status='published',popular=True)
    
    context = {
        "products":products
    }
    return render(request, 'index.html',context)


def product_list_view(request):
    
    products = Product.objects.all(product_status='published')
    
    context = {
        "products":products
    }
    return render(request, 'product-lists.html',context)


def cetagory_list_view(request):
    
    categories = Category.objects.all().annotate(product_count=Count('cetegories'))
    
    context = {
        "categories":categories
    }
    return render(request, 'category-list.html',context)





def product_cetagory_list_view(request,cid):
    
    cetegories = Category.objects.get(cid=cid)
    products = Product.objects.filter(product_status='published',Category=cetegories)
    context = {
        "cetegories":cetegories,
        "products":products,
    }
    return render(request, 'product-category-list.html',context)




def vendor_list_view(request):
    vendors = Vendor.objects.all()
    context = {
        "vendors":vendors
    }
    return render(request, 'vendor-list.html',context)






def vendor_detail_view(request,vid):
    vendor = Vendor.objects.get(vid=vid)
    products = Product.objects.filter(product_status='published',vendor=vendor) 
    context = {
        "vendor":vendor,
        "products":products,
    }
    return render(request, 'vendor-detail.html',context)






