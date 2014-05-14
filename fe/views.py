# Create your views here.
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from ro_graphics import *

from app.account.forms import SignUpForm, LogInForm
from app.account.models import UserProfile
from app.product.models import Product
from app.order.models import Order
from app.order.forms import OrderForm

import json
import pdb


def login(request):
	if request.POST:
		form = LogInForm(request.POST)
		if form.is_valid():
			profile = UserProfile()
			if profile.login_user(request, form):
				return HttpResponseRedirect('/')
			else:
				graphic_content = []
		else:
			graphic_content = [get_login_form(request), get_register_prompt()]
	else:
		graphic_content = [get_login_form(request), get_register_prompt()]
	return render_to_response('sections/bootstrap-clean.html', locals(), context_instance=RequestContext(request))

def register(request):
	if request.POST:
		form = SignUpForm(request.POST)
		if form.is_valid():
			profile = UserProfile()
			profile.create_user(request, form)
			graphic_content = []
		else:
			graphic_content = [get_singup_form(request), get_login_prompt()]
	else:
		graphic_content = [get_singup_form(request), get_login_prompt()]
	return render_to_response('sections/bootstrap-clean.html', locals(), context_instance=RequestContext(request))

def logout(request):
	if request.user.is_authenticated():
		request.user.userprofile.logout_user(request)
	return HttpResponseRedirect('/account/login/')

def account(request):
	response = HttpResponseRedirect('/account/login/?next=/account/')
	if request.user.is_authenticated():
		response = HttpResponseRedirect('/account/'+str(request.user.userprofile.id)+"/")
	return response

def view_account(request, account_id):
	graphic_content = [get_profile_info(account_id)]
	return render_to_response('sections/bootstrap-clean.html', locals(), context_instance=RequestContext(request))

def product(request):
	products_list = Product.objects.all()
	nav_area = get_product_search_nav(None, None, None, None)
	if request.GET:
		code = request.GET.get('code', None)
		name = request.GET.get('name', None)
		brand = request.GET.get('brand', None)
		appliance = request.GET.get('appliance', None)
		if code:
			products_list=products_list.filter(code=code)
		if name:
			products_list=products_list.filter(name=name)
		if brand:
			products_list=products_list.filter(brand=brand)
		if appliance:
			products_list=products_list.filter(appliance=appliance)
		nav_area = get_product_search_nav(code, name, brand, appliance)
	graphic_content=[
		get_product_table(products_list),
		get_add_to_cart_modal(),
		get_add_to_cart_response_modal(),
	]
	return render_to_response('sections/bootstrap-base.html', locals(), context_instance=RequestContext(request))

def index(request):
	graphic_content=[get_home_carousel()]
	return render_to_response('sections/bootstrap-home.html', locals(), context_instance=RequestContext(request))

def add2cart(request):
	response = {'status':True, 'description':""}
	if request.GET:
		product_id = request.GET.get('product', None)
		quantity = request.GET.get('quantity', None)
		if product_id and quantity:
			cart = request.session.get('cart', None)
			if cart:
				product_quantity = int(cart.get(product_id, 0))
				if product_quantity:
					cart[product_id] += int(quantity)
				else:
					cart[product_id] = int(quantity)
				request.session['cart'] = cart
			else:
				request.session['cart'] = {product_id:int(quantity)}
		else:
			response['status'] = False
			response['description'] = "Missed Data"
	else:
		response['status'] = False
		response['description'] = "Missed Data"
	return HttpResponse(json.dumps(response), content_type="application/json")

def cart(request):
	cart = request.session.get('cart', None)
	if cart:
		graphic_content=[get_cart_submit_form(request, cart)]
	else:
		graphic_content=[get_cart_empty_info()]
	return render_to_response('sections/bootstrap-base.html', locals(), context_instance=RequestContext(request))

def remove2cart(request, product_id):
	cart = request.session.get('cart', None)
	if cart:
		cart.pop(product_id)
		request.session['cart'] = cart
	return HttpResponseRedirect('/cart/')

def order(request):
	if request.POST:
		form = OrderForm(request.POST)
		if form.is_valid():
			order = form.get_instance()
			return HttpResponseRedirect('/order/'+order.id+'/')
		else:
			graphic_content = [get_bad_order_info(form.errors)]
	else:
		graphic_content = [get_bad_flow_info()]
	return render_to_response('sections/bootstrap-clean.html', locals(), context_instance=RequestContext(request))

def order_confirmation(request, order_id):
	return render_to_response('sections/bootstrap-base.html', locals(), context_instance=RequestContext(request))