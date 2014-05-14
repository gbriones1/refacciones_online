from django import forms
from app.order.models import Order
from app.product.models import Product
from app.account.models import UserProfile


class OrderForm(forms.Form):
    charge = forms.DecimalField(required=True)
    product = forms.ModelMultipleChoiceField(queryset=Product.objects.all(), required=True)
    profile = forms.ModelChoiceField(queryset=UserProfile.objects.all(), required=True)

    class Meta:
        model = Order
        fields = ('charge', 'product', 'profile')

    def clean(self):
        cleaned_data = super(OrderForm, self).clean()
        profile = cleaned_data["profile"]
        if profile:
        	if not (profile.street1 and profile.zip_code and profile.city and profile.province and profile.country):
        		self._errors["profile_incomplete"] = self.error_class(["Profile incomplete"])
        return cleaned_data