from django import forms
from accounts.forms import BootstrapStyledForm
from .models import Order
from django.contrib.auth import get_user_model

User = get_user_model()

class OrderForm(BootstrapStyledForm, forms.ModelForm):
    comment = forms.CharField(required = False, label='Комментарий к заказу', widget=forms.Textarea(attrs={'style': 'height: 70px;'}))
    
    
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'comment']
        
