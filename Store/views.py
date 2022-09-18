from django.shortcuts import render,get_object_or_404
from Category.models import Categories,SubCategories
from Product.models import Product
from Cart.models import CartItem
from Cart.views import _cart_id
# Create your views here.
def store(request,category_slug = None ,sub_category_slug = None):
    categories = None
    sub_categories = None
    product = None

    if category_slug != None and category_slug == None:
        categories = get_object_or_404(Categories,slug = category_slug)
        product = Product.objects.filter(category_id = categories,is_active = True) 
        product_count = product.count()

    elif sub_category_slug != None and category_slug != None:
        sub_categories = get_object_or_404(SubCategories,slug = sub_category_slug)
        product = Product.objects.filter(subcategory_id = sub_categories, is_active = True) 
        product_count = product.count()

    else:
        product = Product.objects.all().filter(is_active = True)
        product_count = product.count()
    context = {
        'products': product,
        'product_count':product_count
    }
    return render(request,'UserSide/store.html',context)


def product_details(request,cat_slug,sub_cat_slug,product_slug):
    try:
        product = Product.objects.filter(subcategory_id__slug = sub_cat_slug, slug = product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request)).exists()
        
        print(in_cart)    
    except Exception as e:
        raise e

    context={
        'product':product,
        'in_cart':in_cart
    }

    return render(request,'UserSide/product-detail.html',context)


def brand_filtered(request,brand):
    product = Product.objects.filter(brand = brand,is_active = True)
    context={
        'products':product
    }
    return render(request,'UserSide/store.html',context)