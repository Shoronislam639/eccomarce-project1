from django.shortcuts import render,get_object_or_404,redirect
from core.models import Product,Category,Vendor,CartOrderItems,CartOrder,wishlist,Address,ProductImage,ProductReviews
from django.db.models import Count,Avg
from taggit.models import Tag
from core.forms import ProductReviewForm
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib import messages
from datetime import date
from django.contrib.auth.decorators import login_required



from django.urls import reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm



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




  
        
def cart_view(request):
    cart_total_amount = 0
    cart_data = request.session.get('Cart_data_obj', {})
    

    # Update each item's total price
    for item in cart_data.values():
        try:
            qty = int(item.get('qty', 0))
            price = float(item.get('price', 0.0))
            item['total_price'] = qty * price
            cart_total_amount += item['total_price']
        except (ValueError, TypeError):
            item['total_price'] = 0

    if not cart_data:
        messages.warning(request, 'Your Cart is empty')
        return redirect('core:home')

    return render(request, "cart.html", {
        'Cart_data': cart_data,
        'totalcartitems': len(cart_data),
        'cart_total_amount': cart_total_amount
    })
    
    
    
                #Update Cart#

def delete_item_from_cart(request):
    product_id = request.GET.get('id')  # ✅ fixed

    if 'Cart_data_obj' in request.session:
        if product_id in request.session['Cart_data_obj']:
            cart_data = request.session['Cart_data_obj']
            del cart_data[product_id]  # ✅ cleaned
            request.session['Cart_data_obj'] = cart_data

    # Initialize values
    cart_total_amount = 0
    cart_data = request.session.get('Cart_data_obj', {})

    # Update total price per item
    for item in cart_data.values():
        try:
            qty = int(item.get('qty', 0))
            price = float(item.get('price', 0.0))
            item['total_price'] = qty * price
            cart_total_amount += item['total_price']
        except (ValueError, TypeError):
            item['total_price'] = 0

    # Render updated cart list
    context = render_to_string("async/cart-list.html", {
        'Cart_data': cart_data,
        'totalcartitems': len(cart_data),
        'cart_total_amount': cart_total_amount,
    })

    return JsonResponse({
        "data": context,
        "totalcartitems": len(cart_data),
    })

    
    
    
    
    
def update_item_cart(request):
    product_id = request.GET.get('id')
    product_qty = request.GET.get('qty')

    if 'Cart_data_obj' in request.session:
        cart_data = request.session['Cart_data_obj']

        if product_id in cart_data:
            try:
                product_qty = int(product_qty)
                if product_qty < 1:
                    product_qty = 1
            except ValueError:
                product_qty = 1

            cart_data[product_id]['qty'] = product_qty  
            request.session['Cart_data_obj'] = cart_data

    cart_total_amount = 0
    cart_data = request.session.get('Cart_data_obj', {})

    # Update total price per item
    for item in cart_data.values():
        try:
            qty = int(item.get('qty', 0))
            price = float(item.get('price', 0.0))
            item['total_price'] = qty * price
            cart_total_amount += item['total_price']
        except (ValueError, TypeError):
            item['total_price'] = 0

    # Render updated cart list
    context = render_to_string("async/cart-list.html", {
        'Cart_data': cart_data,
        'totalcartitems': len(cart_data),
        'cart_total_amount': cart_total_amount,
    })

    return JsonResponse({
        "data": context,
        "totalcartitems": len(cart_data),
    })


@login_required
def checkout_view(request):
    total_amount = 0
    cart_total_amount = 0
    cart_order_products = []

    if 'Cart_data_obj' in request.session:
        for p_id, item in request.session['Cart_data_obj'].items():
            qty = int(item['qty'])
            price = float(item['price'])
            item_total = qty * price
            total_amount += item_total
            cart_total_amount += item_total

        order = CartOrder.objects.create(
            user=request.user,
            price=total_amount
        )

        for p_id, item in request.session['Cart_data_obj'].items():
            cart_order_product = CartOrderItems.objects.create(
                order=order,
                invoice_no="INVOICE_NO-" + str(order.id),
                item=item['title'],
                image=item['image'],
                qty=item['qty'],
                price=item['price'],
                total=float(item['qty']) * float(item['price'])
            )
            cart_order_products.append(cart_order_product)

    host = request.get_host()
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': cart_total_amount,
        'item_name': 'Order-Item-No-' + str(order.id),
        'invoice': 'Invoice_NO-' + str(order.id),
        'currency_code': 'USD',  
        'notify_url': 'http://{}{}'.format(host, reverse('core:paypal-ipn')),
        'cancel_url': 'http://{}{}'.format(host, reverse('core:payment_failed')),
        'return_url': 'http://{}{}'.format(host, reverse('core:payment_completed')),
    }

    paypal_payment_button = PayPalPaymentsForm(initial=paypal_dict)

    return render(request, "checkout.html", {
        'Cart_data': request.session['Cart_data_obj'],
        'totalcartitems': len(request.session['Cart_data_obj']),
        'paypal_payment_button': paypal_payment_button,
        'cart_order_products': cart_order_products,
        'cart_total_amount': cart_total_amount, 
    })

    
    
@login_required    
def payment_completed_view(request):
    
    cart_total_amount = 0
    cart_data = request.session.get('Cart_data_obj', {})

    
    for item in cart_data.values():
        cart_total_amount = 0
        cart_data = request.session.get('Cart_data_obj', {})

    
        for item in cart_data.values():
            try:
                qty = int(item.get('qty', 0))
                price = float(item.get('price', 0.0))
                item['total_price'] = qty * price
                cart_total_amount += item['total_price']
                
                
            except (ValueError, TypeError):
                item['total_price'] = 0
    return render(request,"payment-completed.html", {
        'Cart_data': cart_data,
        'totalcartitems': len(cart_data),
        'cart_total_amount': cart_total_amount,
        'today': date.today(),
        
        
       
    })



@login_required    
def payment_failed_view(request):
    return render(request,'payment-failed.html')




@login_required
def customer_dashboard(request):
    orders = CartOrder.objects.filter(user=request.user).order_by("-id")
    address = Address.objects.filter(user=request.user)
    
    if request.method == 'POST':
        address_text = request.POST.get('address')
        mobile_number = request.POST.get('mobile_number')
        new_address = Address.objects.create(
                user=request.user,
                address=address_text,
                mobile_number=mobile_number
            )
        messages.success(request,"Address added Succesfully.")
        return redirect('core:user-dashboard')

    context = {
        "orders": orders,
        "address":address,
    }
    return render(request,'dashboard.html',context)




def order_detail(request, id):
    order = get_object_or_404(CartOrder, id=id)  
    order_item = CartOrderItems.objects.filter(order=order)  
    context = {
        'order': order,
        'order_item': order_item,
    }
    return render(request, 'order-detail.html', context)


@login_required
def wishlist_view(request):
    wishlist_items = wishlist.objects.all() 
    context = {
        "w": wishlist_items
    }
    return render(request, "wishlist.html", context)
    

def add_to_wishlist(request):
    product_id = request.GET['id']
    product = Product.objects.get(id=product_id)

    context = {}

    wishlist_count = wishlist.objects.filter(
        product=product,
        user=request.user
    ).count()

    print(wishlist_count)

    if wishlist_count > 0:
        context = {
            "bool": False  # not added again
        }
    else:
        new_wishlist = wishlist.objects.create(
            product=product,
            user=request.user
        )
        context = {
            "bool": True  # added now
        }

    return JsonResponse(context)