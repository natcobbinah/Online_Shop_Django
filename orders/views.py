from django.shortcuts import render, redirect
from django.urls import reverse
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created

# Create your views here.


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # clear cart
            cart.clear()
            # launch asynchronous task sending email to user
            order_created.delay(order.id)
            # set the order in the session
            request.session['order_id'] = order.id
            # redirect for payment
            return redirect(reverse('payment:process'))
            """ 
            #Thank you page not used anymore, as we'll redirect to stripe checkout to
            complete payments
            return render(request,
                          'order/created.html', {
                              'order': order
                          }) """
    else:
        form = OrderCreateForm()
    return render(request,
                  'order/create.html', {
                      'cart': cart,
                      'form': form
                  })
