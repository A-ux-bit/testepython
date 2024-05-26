from django.db.models.fields import CommaSeparatedIntegerField
from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime

from .models import *
from . utils import cookieCart, cartData, guestPedido

def store(request):
   data = cartData(request)    
   cartItems = data['cartItems']
  

   produtos = Produto.objects.all()
   context = {'produtos':produtos, 'cartItems':cartItems}
   return render(request, 'store/store.html', context)

def cart(request):
    
     data = cartData(request)    
     cartItems = data['cartItems']
     pedido = data['pedido']
     items = data['items']           

     context = {'items':items, 'pedido':pedido, 'cartItems':cartItems}
     return render(request, 'store/cart.html', context)

def checkout(request):

     data = cartData(request)    
     cartItems = data['cartItems']
     pedido = data['pedido']
     items = data['items'] 

     context = {'items':items, 'pedido':pedido}
     return render(request, 'store/checkout.html', context)

def new_func(request):
    if request.user.is_authenticated:
         cliente = request.user.cliente
         pedido, created = Pedido.objects.get_or_create(cliente=cliente, complete=False)
         items = pedido.orderitem_set.all() 
         cartItems = pedido.get_cart_items        
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        pedido = cookieData['pedido']
        items = cookieData['items']
    return pedido,items

def updateItem(request):
     data = json.loads(request.body)
     produtoId = data['produtoId']
     action = data['action']

     print('Action:', action)
     print('produtoId:', produtoId)

     cliente = request.user.cliente
     produto = Produto.objects.get(id=produtoId)
     
     pedido, created = Pedido.objects.get_or_create(user=User, complete=False)

     if action == 'add':
          OrderItem.quantidade = (OrderItem.quantidade + 1)
     elif action == 'remove':
          OrderItem.quantidade = (OrderItem.quantidade - 1)

     OrderItem.save()

     if OrderItem.quantidade <= 0:
          OrderItem.delete()

     return JsonResponse('Item was added', safe=False)
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def procesOrder(request):
     transaction_id = datetime.datetime.now().timestamp()
     data = json.loads(request.body)

     if request.user.is_authenticated:
          cliente = request.user.cliente
          pedido, created = Pedido.objects.get_or_create(cliente=cliente, complete=False)

     
     else:
          cliente, pedido = guestPedido(request, data)
         
     
     total= float(data['form']['total'])
     pedido.transaction_id = transaction_id

     if total == float(pedido.get_cart_total):
           pedido.complete = True
     pedido.save()

     if pedido.shipping == True:
          ShippingAddress.objects.create(
               cliente=cliente,
               pedido=pedido,
               endereco=data['shipping']['endereco'],
               cidade=data['shipping']['cidade'],
               estado=data['shipping']['estado'],
               zipcode=data['shipping']['zipcode'],
          )
     
     
     return JsonResponse('Pagamento completo!', safe=False)