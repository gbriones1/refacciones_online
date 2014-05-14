from django.template import loader, RequestContext
import pdb

def cart_counter(request):
	setup = {'cart_counter': 0}
	cart = request.session.get('cart', None)
	if cart:
		setup['cart_counter'] = sum(cart.values())
	return setup