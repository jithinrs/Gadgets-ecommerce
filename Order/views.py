from django.shortcuts import render,redirect
from Cart.models import CartItem
from .forms import OrderForm
from .models import Order
import datetime 
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

            # to generate order number
            # year = int(datetime.date.today().strftime('%Y'))
            # date = int(datetime.date.today().strftime('%d'))
            # month = int(datetime.date.today().strftime('%m'))
            # day = datetime.date(year,date,month)
            # current_date = day.strftime("%Y%m%d")

            # # 'current_date' + 'order_id' 
            # order_number = current_date + str(data.id)
            # data.order_number = order_number
            # data.save()


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
    return render(request,'UserSide/payment.html')