from django.shortcuts import render,get_object_or_404
from core.models import Product,Category,Vendor,CartOrderItems,CartOrder,wishlist,Address,ProductImage,ProductReviews
from django.db.models import Count,Avg
from taggit.models import Tag
from core.forms import ProductReviewForm
from django.http import JsonResponse
from django.template.loader import render_to_string




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
    
    
    make_review = True
    if request.user.is_authenticated:
        user_review_count = ProductReviews.objects.filter(user=request.user,product=product).count()
        if user_review_count >0:
            make_review=False
        
    
    
    context = {
        "p":product,
        "p_image":p_image,
        "products":products,
        'reviews':reviews,
        'average_rating':average_rating,
        #from
        'review_form':review_form,
        'make_review':make_review,
    }
    return render(request,'product_detail_view.html',context)







def tag_list(request, tag_slug=None):
    products = Product.objects.filter(product_status='published').order_by("-id")
    
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag])  # double underscore here
        
    tags = Tag.objects.all()[:4]

    context = {
        "products": products,
        "tag": tag,
        "tags": tags,
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

    
    
    
    
    
    
def search_view(request):
    query = request.GET.get("q")
    
    products= Product.objects.filter(title__icontains=query).order_by("-date")
    
    context={
        "products":products,
        "query":query,
    }
    
    return render(request,"search.html",context)





def filter_product(request):
    categories = request.GET.getlist('category[]')
    vendors = request.GET.getlist('vendor[]')
    
    min_price = request.GET['min_price'] 
    max_price = request.GET['max_price']


    products = Product.objects.filter(product_status='published').order_by("-id").distinct()
    
    products = products.filter(price__gte=min_price)
    products = products.filter(price__lte=max_price)
    
    
    if categories:
        products = products.filter(Category_id__in=categories)

    if vendors:
        products = products.filter(vendor_id__in=vendors)


    data = render_to_string("async/product-list.html", {"products": products})
    return JsonResponse({"data": data})




def add_to_cart(request):
    Cart_product = {}
    
    Cart_product[str(request.GET['id'])]={
        'title' : request.GET['title'],
        'qty' : request.GET['qty'],
        'price' : request.GET['price'],
        'image' : request.GET['image'],
        'pid' : request.GET['pid'],
    }
    
    if 'Cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['Cart_data_obj']:
            Cart_data = request.session['Cart_data_obj']
            Cart_data[str(request.GET['id'])]['qty'] = int(Cart_product[str(request.GET['id'])]['qty'])
            Cart_data.update(Cart_data)
            request.session['Cart_data_obj'] = Cart_data
        else:
            Cart_data = request.session['Cart_data_obj']
            Cart_data.update(Cart_product)
            request.session['Cart_data_obj']=Cart_data
    else:
        request.session['Cart_data_obj'] = Cart_product
    return JsonResponse({"data":request.session['Cart_data_obj'],'totalcartitems':len(request.session['Cart_data_obj'])})        
        