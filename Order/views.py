from django.shortcuts import render,redirect
from Cart.models import CartItem
from Product.models import Product
from .forms import OrderForm
from .models import Order, OrderProduct, Payment
import datetime 
import json
from django.http import JsonResponse
# Create your views here.


def place_order(request,total=0,quantity=0):
    user  = request.user
    
    #if not cartitem redirect to shop

    cart_items = CartItem.objects.filter(user = user)
    cart_count =    cart_items.count()
    if cart_count <= 0:
        return redirect('store')
    
    delivery_charge = 0
    grand_total = 0

    for cart_item in cart_items:
            total += int(cart_item.product.price)*int(cart_item.quantity)
            quantity += cart_item.quantity
    delivery_charge = 50 if total<=500 else 0
    grand_total = total+ delivery_charge


    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            # store  the billing informations
            data = Order()
            data.user=user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.delivery_charge = delivery_charge
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()



            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d") #20210305
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            order = Order.objects.get(user = user, is_ordered = False, order_number = order_number)
            
            context={
                'order':order,
                'cart_items':cart_items,
                'total':total,
                'grand_total':grand_total,
                'delivery_charge':delivery_charge
            }
            return render(request,'UserSide/payment.html',context)
    
    else:
        return redirect('checkout')


def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(user = request.user, is_ordered = False, order_number = body['orderID'])
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status =body['status']
    )
    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.save()

    # Move cart item to orderd product table
    cart_items = CartItem.objects.filter(user = request.user)

    for cart_item in cart_items:
        order_product =  OrderProduct()
        order_product.order_id = order.id
        order_product.payment = payment
        order_product.user_id =  request.user.id
        order_product.product_id = cart_item.product_id
        order_product.quantity =  cart_item.quantity
        order_product.product_price = cart_item.product.price
        order_product.ordered = True
        order_product.save()

    #Reduce Quantity of procut
        product = Product.objects.get( id = cart_item.product_id)
        product.stock -= cart_item.quantity
        product.save()
    
    #clear cart
    CartItem.objects.filter(user = request.user).delete()

    #send order number and Transaction id to Web page using 
    data = {
        'order_number': order.order_number,
        'transID':payment.payment_id
    }
    return JsonResponse(data)


def payments_completed(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')
    try:
        order = Order.objects.get(order_number = order_number, is_ordered=True)
        print('try')
        ordered_products = OrderProduct.objects.filter(order_id=order.id)

        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity

        payment = Payment.objects.get(payment_id=transID)

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
        }
        return render(request, 'UserSide/payment-success.html', context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        print('exception')
        return redirect('home')