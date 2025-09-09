from django.shortcuts import render,get_object_or_404
from core.models import Product,Category,Vendor,CartOrderItems,CartOrder,wishlist,Address,ProductImage,ProductReviews
from django.db.models import Count,Avg
from taggit.models import Tag
from core.forms import ProductReviewForm
from django.http import JsonResponse




def home(request):
    
    products = Product.objects.filter(product_status='published',popular=True)
    
    context = {
        "products":products
    }
    return render(request, 'index.html',context)


def product_list_view(request):
    
    products = Product.objects.filter(product_status='published')
    


    
    context = {
        "products":products,
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


def product_detail_view(request,pid):
    product=Product.objects.get(pid=pid)
    p_image = product.p_image.all()
    products = Product.objects.filter(Category=product.Category).exclude(pid=pid)[:4]
    reviews = ProductReviews.objects.filter(product=product).order_by("-date")
    
    #product rating from
    average_rating=ProductReviews.objects.filter(product=product).aggregate(rating=Avg('rating'))
    
    #Product review from
    review_form =ProductReviewForm()
    
    
    context = {
        "p":product,
        "p_image":p_image,
        "products":products,
        'reviews':reviews,
        'average_rating':average_rating,
        #from
        'review_form':review_form
    }
    return render(request,'product_detail_view.html',context)







def tag_list(request, tag_slug=None):
    products = Product.objects.filter(product_status='published').order_by("-id")
    
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag])  # double underscore here

    context = {
        "products": products,
        "tag": tag,
    }
    return render(request, 'tag.html', context)



def ajax_add_review(request,pid):
    product = Product.objects.get(pk=pid)
    
    user = request.user
    
    review = ProductReviews.objects.create(
        user=user,
        product=product,
        review=request.POST['review'],
        rating=int(request.POST['rating']), 
    )
    
    context={
        'user':user.username,
        'review':request.POST['review'],
        'rating':request.POST['rating'],
    }

    average_reviews = ProductReviews.objects.filter(product=product).aggregate(rating=Avg('rating'))
    
    return JsonResponse({
    'bool': True,
    'context': context,
    'average_reviews': average_reviews
})

    
    