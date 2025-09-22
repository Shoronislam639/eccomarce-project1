from django.urls import path
from . import views
from core.views import search_view,ajax_add_review,tag_list,vendor_detail_view,filter_product,add_to_cart,cart_view,delete_item_from_cart

app_name = 'core'  

urlpatterns = [
    #home
    path('', views.home, name='home'), 
    path('products/', views.product_list_view, name='product_list_view'), 
    path('products/<pid>/', views.product_detail_view, name='product_detail_view'), 
    #category
    path('category', views.cetagory_list_view, name='cetagory_list_view'), 
    path('category/<cid>/', views.product_cetagory_list_view, name='product_cetagory_list_view'),
    #vendor
    path('vendor/', views.vendor_list_view, name='vendor_list_view'), 
    path('vendor/<vid>/', vendor_detail_view, name='vendor_detail_view'),
    #tags
    path('products/tags/<slug:tag_slug>/', tag_list, name='tag_list'), 
    
    #review
    path('ajax-add-review/<int:pid>/',ajax_add_review,name='ajax-add-review'),
    
    #search
    
    path('search/',search_view,name='search_view'),
    #filter product url
    path('filter-product/',filter_product,name='filter_product'),
    
    #add to cart url
    path("add-to-cart/",add_to_cart,name="add-to-cart"),
    #Cart url
    path("cart/",cart_view,name="cart"),
    
    #delete-from-cart
    path("delete-from-cart/",delete_item_from_cart,name="delete-from-cart"),
    
    ]