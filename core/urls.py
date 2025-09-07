from django.urls import path
from . import views

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
    path('vendor/<vid>/', views.vendor_detail_view, name='vendor_detail_view'),
    #tags
    path('products/tags/<slug:tag_slug>/', views.tag_list, name='tag_list'), 
    ]