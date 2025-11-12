from django import forms
from dashboard.models import Product, Purchase, Type, Sale, BC, Number8, Ds9c, Np7a, Customer, BCPurchase, BCSale, NPurchase, NSale, DsPurchase, DSSale, N7Purchase, N7Sale
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

class BcForm(forms.ModelForm):
    item_id = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Item id',
    }))
    
    name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Item Name',
    }))
    
    unit = forms.DecimalField(widget=forms.NumberInput(attrs={
        'placeholder': 'Enter Item Cost per unit',
        'class': 'form-control'
    }),required=False)
    type = forms.ModelChoiceField(
    queryset=Type.objects.all(),
    required=True,  # This goes here
    widget=forms.Select(attrs={
        'class': 'form-control form-select',
    }))
    current_stock = forms.IntegerField(widget=forms.NumberInput(attrs={
        'placeholder': 'Enter Item current stock',
        'class': 'form-control'
    }),required=False)
    
    total_sold = forms.IntegerField(
        widget=forms.NumberInput(attrs={
        'placeholder': 'Enter Item Total sold',
        'class': 'form-control'
    }),required=False)
    
    total_cost_value = forms.DecimalField(widget=forms.NumberInput(attrs={
        'placeholder': 'Enter Item total cost value',
        'class':'form-control'
    }),required=False)
    
    class Meta:
        model = BC
        fields = ['item_id', 'name', 'unit', 'type', 'current_stock', 'total_sold', 'total_cost_value']
        
class NumberForm(forms.ModelForm):
    item_id = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Item id',
    }))
    
    name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Item Name',
    }))
    
    unit = forms.DecimalField(widget=forms.NumberInput(attrs={
        'placeholder': 'Enter Item Cost per unit',
        'class': 'form-control'
    }),required=False)
    type = forms.ModelChoiceField(
    queryset=Type.objects.all(),
    required=True,  # This goes here
    widget=forms.Select(attrs={
        'class': 'form-control form-select',
    }))
    current_stock = forms.IntegerField(widget=forms.NumberInput(attrs={
        'placeholder': 'Enter Item current stock',
        'class': 'form-control'
    }),required=False)
    
    total_sold = forms.IntegerField(
        widget=forms.NumberInput(attrs={
        'placeholder': 'Enter Item Total sold',
        'class': 'form-control'
    }),required=False)
    
    total_cost_value = forms.DecimalField(widget=forms.NumberInput(attrs={
        'placeholder': 'Enter Item total cost value',
        'class':'form-control'
    }),required=False)
    
    class Meta:
        model = Number8
        fields = ['item_id', 'name', 'unit', 'type', 'current_stock', 'total_sold', 'total_cost_value']
        
class DcForm(forms.ModelForm):
    item_id = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Item id',
    }))
    
    name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Item Name',
    }))
    
    unit = forms.DecimalField(widget=forms.NumberInput(attrs={
        'placeholder': 'Enter Item Cost per unit',
        'class': 'form-control'
    }),required=False)
    
    type = forms.ModelChoiceField(
    queryset=Type.objects.all(),
    required=True,  # This goes here
    widget=forms.Select(attrs={
        'class': 'form-control form-select',
    }))
    current_stock = forms.IntegerField(widget=forms.NumberInput(attrs={
        'placeholder': 'Enter Item current stock',
        'class': 'form-control'
    }),required=False)
    
    total_sold = forms.IntegerField(
        widget=forms.NumberInput(attrs={
        'placeholder': 'Enter Item Total sold',
        'class': 'form-control'
    }),required=False)
    
    total_cost_value = forms.DecimalField(widget=forms.NumberInput(attrs={
        'placeholder': 'Enter Item total cost value',
        'class':'form-control'
    }),required=False)
    
    class Meta:
        model = Ds9c
        fields = ['item_id', 'name', 'unit', 'type', 'current_stock', 'total_sold', 'total_cost_value']
        

class NpForm(forms.ModelForm):
    item_id = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Item id',
    }))
    
    name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Item Name',
    }))
    
    unit = forms.DecimalField(widget=forms.NumberInput(attrs={
        'placeholder': 'Enter Item Cost per unit',
        'class': 'form-control'
    }),required=False)
    
    type = forms.ModelChoiceField(
    queryset=Type.objects.all(),
    required=True,  # This goes here
    widget=forms.Select(attrs={
        'class': 'form-control form-select',
    }))
    current_stock = forms.IntegerField(widget=forms.NumberInput(attrs={
        'placeholder': 'Enter Item current stock',
        'class': 'form-control'
    }),required=False)
    
    total_sold = forms.IntegerField(
        widget=forms.NumberInput(attrs={
        'placeholder': 'Enter Item Total sold',
        'class': 'form-control'
    }),required=False)
    
    total_cost_value = forms.DecimalField(widget=forms.NumberInput(attrs={
        'placeholder': 'Enter Item total cost value',
        'class':'form-control'
    }),required=False)
    
    class Meta:
        model = Np7a
        fields = ['item_id', 'name', 'unit', 'type', 'current_stock', 'total_sold', 'total_cost_value']


class ProductForm(forms.ModelForm):   
    item_id = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Item id',
    }))
    
    name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Item Name',
    }))
    
    type = forms.ModelChoiceField(
    queryset=Type.objects.all(),
    required=True,  # This goes here
    widget=forms.Select(attrs={
        'class': 'form-control form-select',
    }))
    cost_per_unit = forms.DecimalField(widget=forms.NumberInput(attrs={
        'placeholder': 'Enter Item Cost per unit',
        'class': 'form-control'
    }),required=False)
    
    current_stock = forms.IntegerField(widget=forms.NumberInput(attrs={
        'placeholder': 'Enter Item current stock',
        'class': 'form-control'
    }),required=False)
    
    total_sold = forms.IntegerField(
        widget=forms.NumberInput(attrs={
        'placeholder': 'Enter Item Total sold',
        'class': 'form-control'
    }),required=False)
    
    total_cost_value = forms.DecimalField(widget=forms.NumberInput(attrs={
        'placeholder': 'Enter Item total cost value',
        'class':'form-control'
    }),required=False)
    
    class Meta:
        model = Product
        fields = ['item_id', 'name', 'type', 'cost_per_unit', 'current_stock', 'total_sold', 'total_cost_value']
        


class PurchaseForm(forms.ModelForm):
    product = forms.ModelChoiceField(
    queryset=Product.objects.all(),
    required=True,  # This goes here
    widget=forms.Select(attrs={
        'class': 'form-control form-select',
    }))
        
    purchase_date = forms.DateField(widget=forms.DateInput(attrs={
        'placeholder': 'DD-MM-YYYY',
        'type': 'date',
        'class': 'form-control'
    }))
        
    price = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Price',
    }))
    
    unit_purchased = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Unit Purchased',
    }))
    
    point_of_contact = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Point of Contact',
    }),required=False)
    type = forms.ModelChoiceField(
    queryset=Type.objects.all(),
    required=True,  # This goes here
    widget=forms.Select(attrs={
        'class': 'form-control form-select',
    }))
    
    notes = forms.CharField(widget=forms.Textarea(attrs={
    'placeholder': 'Enter Notes',
    'rows': 3,
    'class': 'form-control',  # optional for Bootstrap styling
    }),required=False)

    class Meta:
        model = Purchase                 
        fields = ['product', 'purchase_date', 'type', 'price', 'unit_purchased', 'point_of_contact', 'notes']
        

class BCPurchaseForm(forms.ModelForm):
    product = forms.ModelChoiceField(
    queryset=BC.objects.all(),
    required=True,  # This goes here
    widget=forms.Select(attrs={
        'class': 'form-control form-select',
    }))
        
    purchase_date = forms.DateField(widget=forms.DateInput(attrs={
        'placeholder': 'DD-MM-YYYY',
        'type': 'date',
        'class': 'form-control'
    }))
        
    price = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Price',
    }))
    
    unit_purchased = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Unit Purchased',
    }))
    
    point_of_contact = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Point of Contact',
    }),required=False)
    type = forms.ModelChoiceField(
    queryset=Type.objects.all(),
    required=True,  # This goes here
    widget=forms.Select(attrs={
        'class': 'form-control form-select',
    }))
    
    notes = forms.CharField(widget=forms.Textarea(attrs={
    'placeholder': 'Enter Notes',
    'rows': 3,
    'class': 'form-control',  # optional for Bootstrap styling
    }),required=False)

    class Meta:
        model = BCPurchase                 
        fields = ['product', 'purchase_date', 'type', 'price', 'unit_purchased', 'point_of_contact', 'notes']
    

class BCSaleForm(forms.ModelForm):
    product = forms.ModelChoiceField(
    queryset=BC.objects.all(),
    required=True,  # This goes here
    widget=forms.Select(attrs={
        'class': 'form-control form-select',
    }))
        
    sales_date = forms.DateField(widget=forms.DateInput(attrs={
        'placeholder': 'DD-MM-YYYY',
        'type': 'date',
        'class': 'form-control'
    }))
        
    price = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Price',
    }))
    
    unit_sold = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Unit Purchased',
    }))
    
    point_of_contact = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Point of Contact',
    }),required=False)
    type = forms.ModelChoiceField(
    queryset=Type.objects.all(),
    required=True,  # This goes here
    widget=forms.Select(attrs={
        'class': 'form-control form-select',
    }))
    
    notes = forms.CharField(widget=forms.Textarea(attrs={
    'placeholder': 'Enter Notes',
    'rows': 3,
    'class': 'form-control',  # optional for Bootstrap styling
    }),required=False)

    class Meta:
        model = BCSale                 
        fields = ['product', 'sales_date', 'type', 'price', 'unit_sold', 'point_of_contact', 'notes']
        
class NSaleForm(forms.ModelForm):
    product = forms.ModelChoiceField(
    queryset=Number8.objects.all(),
    required=True,  # This goes here
    widget=forms.Select(attrs={
        'class': 'form-control form-select',
    }))
        
    sales_date = forms.DateField(widget=forms.DateInput(attrs={
        'placeholder': 'DD-MM-YYYY',
        'type': 'date',
        'class': 'form-control'
    }))
        
    price = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Price',
    }))
    
    unit_sold = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Unit Purchased',
    }))
    
    point_of_contact = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Point of Contact',
    }),required=False)
    type = forms.ModelChoiceField(
    queryset=Type.objects.all(),
    required=True,  # This goes here
    widget=forms.Select(attrs={
        'class': 'form-control form-select',
    }))
    
    notes = forms.CharField(widget=forms.Textarea(attrs={
    'placeholder': 'Enter Notes',
    'rows': 3,
    'class': 'form-control',  # optional for Bootstrap styling
    }),required=False)

    class Meta:
        model = NSale                 
        fields = ['product', 'sales_date', 'type', 'price', 'unit_sold', 'point_of_contact', 'notes']
        
class SaleForm(forms.ModelForm):
    product = forms.ModelChoiceField(
    queryset=Product.objects.all(),
    required=True,  # This goes here
    widget=forms.Select(attrs={
        'class': 'form-control form-select',
    }))
        
    sales_date = forms.DateField(widget=forms.DateInput(attrs={
        'placeholder': 'DD-MM-YYYY',
        'type': 'date',
        'class': 'form-control'
    }))
        
    price = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Price',
    }))
    
    unit_sold = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Unit Purchased',
    }))
    
    point_of_contact = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Point of Contact',
    }),required=False)
    type = forms.ModelChoiceField(
    queryset=Type.objects.all(),
    required=True,  # This goes here
    widget=forms.Select(attrs={
        'class': 'form-control form-select',
    }))
    
    notes = forms.CharField(widget=forms.Textarea(attrs={
    'placeholder': 'Enter Notes',
    'rows': 3,
    'class': 'form-control',  # optional for Bootstrap styling
    }),required=False)

    class Meta:
        model = Sale                 
        fields = ['product', 'sales_date', 'type', 'price', 'unit_sold', 'point_of_contact', 'notes']     
    
class NPurchaseForm(forms.ModelForm):
    product = forms.ModelChoiceField(
    queryset=Number8.objects.all(),
    required=True,  # This goes here
    widget=forms.Select(attrs={
        'class': 'form-control form-select',
    }))
        
    purchase_date = forms.DateField(widget=forms.DateInput(attrs={
        'placeholder': 'DD-MM-YYYY',
        'type': 'date',
        'class': 'form-control'
    }))
        
    price = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Price',
    }))
    
    unit_purchased = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Unit Purchased',
    }))
    
    point_of_contact = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Point of Contact',
    }),required=False)
    type = forms.ModelChoiceField(
    queryset=Type.objects.all(),
    required=True,  # This goes here
    widget=forms.Select(attrs={
        'class': 'form-control form-select',
    }))
    
    notes = forms.CharField(widget=forms.Textarea(attrs={
    'placeholder': 'Enter Notes',
    'rows': 3,
    'class': 'form-control',  # optional for Bootstrap styling
    }),required=False)

    class Meta:
        model =  NPurchase                
        fields = ['product', 'purchase_date', 'type', 'price', 'unit_purchased', 'point_of_contact', 'notes']


class DsPurchaseForm(forms.ModelForm):
    product = forms.ModelChoiceField(
    queryset=Ds9c.objects.all(),
    required=True,  # This goes here
    widget=forms.Select(attrs={
        'class': 'form-control form-select',
    }))
        
    purchase_date = forms.DateField(widget=forms.DateInput(attrs={
        'placeholder': 'DD-MM-YYYY',
        'type': 'date',
        'class': 'form-control'
    }))
        
    price = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Price',
    }))
    
    unit_purchased = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Unit Purchased',
    }))
    
    point_of_contact = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Point of Contact',
    }),required=False)
    type = forms.ModelChoiceField(
    queryset=Type.objects.all(),
    required=True,  # This goes here
    widget=forms.Select(attrs={
        'class': 'form-control form-select',
    }))
    
    notes = forms.CharField(widget=forms.Textarea(attrs={
    'placeholder': 'Enter Notes',
    'rows': 3,
    'class': 'form-control',  # optional for Bootstrap styling
    }),required=False)

    class Meta:
        model =  DsPurchase                
        fields = ['product', 'purchase_date', 'type', 'price', 'unit_purchased', 'point_of_contact', 'notes']
        
class N7PurchaseForm(forms.ModelForm):
    product = forms.ModelChoiceField(
    queryset=Np7a.objects.all(),
    required=True,  # This goes here
    widget=forms.Select(attrs={
        'class': 'form-control form-select',
    }))
        
    purchase_date = forms.DateField(widget=forms.DateInput(attrs={
        'placeholder': 'DD-MM-YYYY',
        'type': 'date',
        'class': 'form-control'
    }))
        
    price = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Price',
    }))
    
    unit_purchased = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Unit Purchased',
    }))
    
    point_of_contact = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Point of Contact',
    }),required=False)
    type = forms.ModelChoiceField(
    queryset=Type.objects.all(),
    required=True,  # This goes here
    widget=forms.Select(attrs={
        'class': 'form-control form-select',
    }))
    
    notes = forms.CharField(widget=forms.Textarea(attrs={
    'placeholder': 'Enter Notes',
    'rows': 3,
    'class': 'form-control',  # optional for Bootstrap styling
    }),required=False)

    class Meta:
        model = N7Purchase                 
        fields = ['product', 'purchase_date', 'type', 'price', 'unit_purchased', 'point_of_contact', 'notes']
    
class N7SaleForm(forms.ModelForm):
    product = forms.ModelChoiceField(
    queryset=Np7a.objects.all(),
    required=True,  # This goes here
    widget=forms.Select(attrs={
        'class': 'form-control form-select',
    }))
        
    sales_date = forms.DateField(widget=forms.DateInput(attrs={
        'placeholder': 'DD-MM-YYYY',
        'type': 'date',
        'class': 'form-control'
    }))
        
    price = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Price',
    }))
    
    unit_sold = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Unit Purchased',
    }))
    
    point_of_contact = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Point of Contact',
    }),required=False)
    type = forms.ModelChoiceField(
    queryset=Type.objects.all(),
    required=True,  # This goes here
    widget=forms.Select(attrs={
        'class': 'form-control form-select',
    }))
    
    notes = forms.CharField(widget=forms.Textarea(attrs={
    'placeholder': 'Enter Notes',
    'rows': 3,
    'class': 'form-control',  # optional for Bootstrap styling
    }),required=False)

    class Meta:
        model = N7Sale                 
        fields = ['product', 'sales_date', 'type', 'price', 'unit_sold', 'point_of_contact', 'notes']
        
class DSSaleForm(forms.ModelForm):
    product = forms.ModelChoiceField(
    queryset=Ds9c.objects.all(),
    required=True,  # This goes here
    widget=forms.Select(attrs={
        'class': 'form-control form-select',
    }))
        
    sales_date = forms.DateField(widget=forms.DateInput(attrs={
        'placeholder': 'DD-MM-YYYY',
        'type': 'date',
        'class': 'form-control'
    }))
        
    price = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Price',
    }))
    
    unit_sold = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Unit Purchased',
    }))
    
    point_of_contact = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Point of Contact',
    }),required=False)
    type = forms.ModelChoiceField(
    queryset=Type.objects.all(),
    required=True,  # This goes here
    widget=forms.Select(attrs={
        'class': 'form-control form-select',
    }))
    
    notes = forms.CharField(widget=forms.Textarea(attrs={
    'placeholder': 'Enter Notes',
    'rows': 3,
    'class': 'form-control',  # optional for Bootstrap styling
    }),required=False)

    class Meta:
        model = DSSale                 
        fields = ['product', 'sales_date', 'type', 'price', 'unit_sold', 'point_of_contact', 'notes']
class TypeForm(forms.ModelForm):       
    name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Name',
    }))
    class Meta:
        model = Type                 
        fields = ['name']
        



class LoginForm(AuthenticationForm):
    
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your username',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password',
        'class': 'pass-input'
    }))
        
        
class AdminProfileForm(forms.ModelForm):
    password = forms.CharField(
        label="New Password",
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter new password', 'class': 'pass-input'})
    )
    password2 = forms.CharField(
        label="Confirm Password",
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password', 'class': 'pass-input'})
    )
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}),
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
        }
        
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password or password2:
            if password != password2:
                raise forms.ValidationError("Passwords do not match.")

        return cleaned_data
    
    
    
class CustomerForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Your Name',
    }))
    
    email = forms.EmailField(
    widget=forms.EmailInput(attrs={
        'placeholder': 'Enter Your Email',
        "class":"form-control"
    })
)
    
    phone = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Your Phone Number',
    }))
    
    address = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': "Enter your Address", 
        "class":"form-control"
    }))
    
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'address']

    
    
    
    
    
    