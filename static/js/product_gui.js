$('button.add2cart').each(function(){
	$(this).click(function(){
		item_id = $(this).attr("id")
		quantity = $('input[id='+item_id+']').val();
		if (quantity == '0'){
			return false;
		}
		else{
			$('div.modal div.add2cart').text("Quieres agregar "+quantity+" "+$(this).attr("name")+"(s) al carrito de compras?")
			$('div.modal input#product.add2cart').attr("value", item_id)
			$('div.modal input#quantity.add2cart').attr("value", quantity)
		}
	})
});
$('div.modal button#add2cart').click(function(){
	$.ajaxSetup({
        cache: false
    });
	$.get("/add2cart/",
		{product:$('div.modal input#product.add2cart').val(), quantity:$('div.modal input#quantity.add2cart').val()},
		function(data,status,xhr){
			console.log(data);
		}
	);
	$('div#id_add2cart_modal').modal('hide');
	$('div#id_add2cart_response_modal').modal('show');
});

$('div#id_add2cart_response_modal').on('hidden.bs.modal', function(){
	window.location.reload();
});

$('form#id_cart_submit_form').submit(function(){
	$('#id_charge_input').val($('th#charge').text());
});