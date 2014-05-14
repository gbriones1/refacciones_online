from decimal import *

from graphics_builder import *
from app.account.models import *
from app.product.models import *
from app.order.models import *

def get_login_form(request):
	form = Form(text="Log in", attributes={"action":".", "method":"POST", "style":"padding-top: 50px;"}, item_list=[
		FormGroup(label="Correo electronico", input=Text(attributes={"name":"email"})),
		FormGroup(label="Contrasena:", input=Password(attributes={"name":"password"})),
		Hidden(attributes={"name":"csrfmiddlewaretoken", "value":request.COOKIES["csrftoken"]}),
		Button(text="Iniciar sesion", attributes={"class":Button.PRIMARY}),
	])
	return form

def get_register_prompt():
	div = Div(attributes={"style":"padding-top: 50px;padding-bottom: 50px;"}, children=[H3(text="No estas registrado aun?"),
		A(text="Registrarse", attributes={"class":"btn btn-success", "href":"/account/register/"}),
	])
	return div

def get_singup_form(request):
	form = Form(text="Sign up", attributes={"action":".", "method":"POST", "style":"padding-top: 50px;"}, item_list=[
		FormGroup(label="Correo electronico:", input=Text(attributes={"name":"email"})),
		FormGroup(label="Contrasena:", input=Password(attributes={"name":"password"})),
		FormGroup(label="Nombre(s):", input=Text(attributes={"name":"first_name"})),
		FormGroup(label="Apellido(s):", input=Text(attributes={"name":"last_name"})),
		Hidden(attributes={"name":"csrfmiddlewaretoken", "value":request.COOKIES["csrftoken"]}),
		Button(text="Registrarse", attributes={"class":Button.PRIMARY}),
	])
	return form

def get_login_prompt():
	div = Div(attributes={"style":"padding-top: 50px;padding-bottom: 50px;"}, children=[H3(text="Ya tienes una cuenta?"),
		A(text="Iniciar Sesion", attributes={"class":"btn btn-success", "href":"/account/login/"}),
	])
	return div

def get_new_user_welcome():
	pass

def get_home_carousel():
	carousel = Carousel(
		attributes={"id":"main-carousel", "style":"margin-bottom: 20px;"},
		slide_img_src=["/static/img/back_pic01.jpg","/static/img/back_pic02.jpg","/static/img/back_pic03.jpg"],
		interval=5000,
	)
	return carousel

def get_product_table(products):
	table = Table(attributes={"class":Table.HOVER})
	thead = THead(children=[
		TR(children=[
			TH(text="Imagen"),
			TH(text="Codigo"),
			TH(text="Nombre"),
			TH(text="Descripcion"),
			TH(text="Marca"),
			TH(text="Precio"),
			TH(text="Cantidad"),
		])
	])
	tbody = TBody()
	tbody.children = []
	for product in products:
		tr = TR()
		tr.children = []
		if product.picture:
			tr.children.append(TD(attributes={"style":"width: 100px;text-align: center;"}, children=[Img(attributes={"src":product.picture.url})]))
		else:
			tr.children.append(TD(attributes={"style":"width: 100px;text-align: center;"}))
		tr.children.append(TD(text=product.code))
		tr.children.append(TD(text=product.name))
		tr.children.append(TD(text=product.description))
		tr.children.append(TD(text=product.brand.name))
		tr.children.append(TD(text=product.price))
		tr.children.append(TD(attributes={"style":"width: 100px;text-align: center;"}, children=[
			Input(attributes={"type":"number", "name":"quantity", "min":0, "value":0, "style":"width: 50px", "id":product.id}),
			Button(text="Agregar al carrito", attributes={
				"id":product.id,
				"name":product.name,
				"class":Button.INFO+"add2cart",
				"data-toggle":"modal",
				"data-target":"#id_add2cart_modal",
				"style":"margin-top: 10px;",
			})
		]))
		tbody.children.append(tr)
	table.children = [thead, tbody]
	return table

def get_add_to_cart_modal():
	modal = Modal(
		title="Agregar al carrito",
		attributes={"id":"id_add2cart_modal"},
		body_item_list=[
			Div(text="Aqui va el texto", attributes={"class":"add2cart"}),
			Hidden(attributes={"class":"add2cart", "id":"product"}),
			Hidden(attributes={"class":"add2cart", "id":"quantity"}),
		],
		footer_item_list=[Button(text="Aceptar", attributes={"class":Button.PRIMARY, "id":"add2cart"})],
		close_btn_text="Cancelar",
	)
	return modal

def get_add_to_cart_response_modal():
	modal = Modal(
		title="Agregar al carrito",
		attributes={"id":"id_add2cart_response_modal"},
		body_item_list=[
			Div(text="Tus productos fueron agregados"),
		],
		close_btn_text="OK",
	)
	return modal

def get_product_search_nav(selected_code, selected_name, selected_brand_id, selected_appliance_id):
	brand_options = [Option()]
	for brand in Brand.objects.all():
		if selected_brand_id and int(selected_brand_id) == brand.id:
			brand_options.append(Option(text=brand.name, attributes={"value":brand.id, "selected":"selected"}))
		else:
			brand_options.append(Option(text=brand.name, attributes={"value":brand.id}))
	appliance_options = [Option()]
	for appliance in Appliance.objects.all():
		if selected_appliance_id and int(selected_appliance_id) == appliance.id:
			appliance_options.append(Option(text=appliance.name, attributes={"value":appliance.id, "selected":"selected"}))
		else:
			appliance_options.append(Option(text=appliance.name, attributes={"value":appliance.id}))
	code_input = Text(attributes={"name":"code"})
	if selected_code:
		code_input.attributes["value"] = selected_code
	name_input = Text(attributes={"name":"name"})
	if selected_name:
		name_input.attributes["value"] = selected_name
	form = Form(text="Filtra tu busqueda", attributes={"action":".", "method":"GET"}, item_list=[
		FormGroup(label="Codigo:", input=code_input),
		FormGroup(label="Nombre:", input=name_input),
		FormGroup(label="Marca:", input=Select(attributes={"name":"brand"}, children=brand_options)),
		FormGroup(label="Aplicacion:", input=Select(attributes={"name":"appliance"}, children=appliance_options)),
		Button(text="Buscar", attributes={"class":Button.PRIMARY}),
	])
	return form

def get_cart_table(cart):
	table = Table(attributes={"class":Table.HOVER})
	thead = THead(children=[
		TR(children=[
			TH(text="Imagen"),
			TH(text="Codigo"),
			TH(text="Nombre"),
			TH(text="Descripcion"),
			TH(text="Marca"),
			TH(text="Precio"),
			TH(text="Cantidad"),
			TH(text="Total"),
			TH(),
		])
	])
	tbody = TBody()
	tbody.children = []
	total = Decimal(0)
	for product_id in cart.keys():
		product = Product.objects.get(id=product_id)
		tr = TR(attributes={"class":"product_row", "id":product_id})
		tr.children = []
		if product.picture:
			tr.children.append(TD(attributes={"style":"width: 100px;text-align: center;"}, children=[Img(attributes={"src":product.picture.url})]))
		else:
			tr.children.append(TD(attributes={"style":"width: 100px;text-align: center;"}))
		tr.children.append(TD(text=product.code))
		tr.children.append(TD(text=product.name))
		tr.children.append(TD(text=product.description))
		tr.children.append(TD(text=product.brand.name))
		tr.children.append(TD(text=product.price))
		tr.children.append(TD(text=cart[product_id]))
		tr.children.append(TD(text=product.price*cart[product_id]))
		tr.children.append(TD(attributes={"style":"width: 100px;text-align: center;"}, children=[
			A(text="Quitar", attributes={
				"href":"/remove2cart/"+product_id+"/",
				"class":"btn "+Button.DANGER,
			})
		]))
		tbody.children.append(tr)
		total += product.price*cart[product_id]
	tfoot = TFoot(children=[
		TR(children=[
			TH(),
			TH(),
			TH(),
			TH(),
			TH(),
			TH(text="Total de la compra", attributes={'colspan':2}),
			TH(text=total, attributes={"id":"charge"}),
			TH(attributes={"style":"width: 100px;text-align: center;"}, children=[
				Button(text="Comprar", attributes={
					"class":Button.SUCCESS,
					"type": "submit",
				})
			]),
		])
	])
	table.children = [thead, tbody, tfoot]
	return table

def get_cart_submit_form(request, cart):
	profile_id = ""
	profile_query = UserProfile.objects.filter(user=request.user.id)
	if profile_query.exists():
		profile_id = profile_query[0].id
	product_select = Select(attributes={"name":"product", "style":"display: none;"})
	product_select.children = []
	for product_id in cart.keys():
		product_select.children.append(Option(attributes={"value":product_id, "selected":"selected"}))
	form = Form(attributes={"action":"/order/", "method":"POST", "id":"id_cart_submit_form"}, item_list=[
		Hidden(attributes={"name":"csrfmiddlewaretoken", "value":request.COOKIES["csrftoken"]}),
		Hidden(attributes={"name":"profile", "value":profile_id}),
		product_select,
		Hidden(attributes={"name":"charge", "value":"", "id":"id_charge_input"}),
	])
	form.children.append(get_cart_table(cart))
	return form

def get_cart_empty_info():
	div = Div(attributes={"style":"padding-top: 50px;padding-bottom: 50px;"}, children=[H3(text="Tu carrito de compras esta vacio."),
			A(text="Buscar productos", attributes={"class":"btn btn-primary", "href":"/product/"})
	])
	return div

def get_bad_flow_info():
	div = Div(attributes={"style":"padding-top: 50px;padding-bottom: 50px;"}, children=[H3(text="Este flujo no es autorizado"),
	])
	return div

def get_bad_order_info(errors):
	div = Div(attributes={"style":"padding-top: 50px;padding-bottom: 50px;"})
	if "profile" in errors:
		div.children = [
			H3(text="No has iniciado sesion"),
			P(text="Para confirmar tu orden debes iniciar sesion", attributes={"class":P.TEXT_WARNING}),
			A(text="Iniciar Sesion", attributes={"class":"btn btn-success", "href":"/account/login/?next=/cart/"})
		]
	elif "profile_incomplete" in errors:
		div.children = [
			H3(text="Perfil incompleto"),
			P(text="Para confirmar tu orden debes completar la informacion que hace falta en tu perfil", attributes={"class":P.TEXT_WARNING}),
			A(text="Ver perfil", attributes={"class":"btn btn-primary", "href":"/account/"})
		]
	return div
