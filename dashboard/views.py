from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm, PurchaseForm, SaleForm, TypeForm, AdminProfileForm, BcForm, DcForm, NumberForm, NpForm, CustomerForm
from django.contrib import messages
from dashboard.models import Product, Purchase, Sale, Type, Notification, BC, Number8, Ds9c, Np7a, Customer, BCPurchase, BCSale, DSSale, N7Sale, NSale, N7Purchase, NPurchase, DsPurchase
from django.db.models import Sum, F, FloatField, DecimalField, Value as V
from django.db.models.functions import Coalesce
import calendar
from django.utils.timezone import now
from django.db.models.functions import TruncMonth

from django.db.models import Sum, F, FloatField, Value as V
from django.db.models.functions import Coalesce, TruncMonth
from django.utils.timezone import now
import calendar
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from itertools import chain
from django.utils.timezone import now
from datetime import date
today = date.today()

@login_required
def index(request):

    products = Product.objects.all()
    bc_products= BC.objects.all()
    number8_products = Number8.objects.all()
    ds9c_products = Ds9c.objects.all()
    np7a_products = Np7a.objects.all()
    
    today = date.today()
    
    all_items = list(chain(products, bc_products, number8_products, ds9c_products, np7a_products))
    
    total_current_stock = sum([p.current_stock or 0 for p in all_items])

# 💰 Total Revenue = Sum of all sales (unit_sold * price) from all product models
    total_revenue = (
    (Sale.objects.aggregate(revenue=Sum(F('unit_sold') * F('price'), output_field=FloatField()))['revenue'] or 0) +
    (BCSale.objects.aggregate(revenue=Sum(F('unit_sold') * F('price'), output_field=FloatField()))['revenue'] or 0) +
    (NSale.objects.aggregate(revenue=Sum(F('unit_sold') * F('price'), output_field=FloatField()))['revenue'] or 0) +
    (DSSale.objects.aggregate(revenue=Sum(F('unit_sold') * F('price'), output_field=FloatField()))['revenue'] or 0) +
    (N7Sale.objects.aggregate(revenue=Sum(F('unit_sold') * F('price'), output_field=FloatField()))['revenue'] or 0)
)
# 💸 Total Cost = Sum of all purchases (unit_purchased * price) from all product models
    total_cost = (
    Purchase.objects.aggregate(cost=Sum(F('unit_purchased') * F('price'), output_field=FloatField()))['cost'] or 0
) + (
    BCPurchase.objects.aggregate(cost=Sum(F('unit_purchased') * F('price'), output_field=FloatField()))['cost'] or 0
) + (
    NPurchase.objects.aggregate(cost=Sum(F('unit_purchased') * F('price'), output_field=FloatField()))['cost'] or 0
) + (
    N7Purchase.objects.aggregate(cost=Sum(F('unit_purchased') * F('price'), output_field=FloatField()))['cost'] or 0
) + (
    DsPurchase.objects.aggregate(cost=Sum(F('unit_purchased') * F('price'), output_field=FloatField()))['cost'] or 0
)


# 🏪 Inventory Value = Sum of (product.current_stock * product.average_cost()) for each product
    inventory_value = 0
    for product in products:
        inventory_value += (product.current_stock or 0) * float(product.average_cost())
    for bc_product in bc_products:
        inventory_value += (bc_product.current_stock or 0) * float(bc_product.average_cost())
    for number8_product in number8_products:
        inventory_value += (number8_product.current_stock or 0) * float(number8_product.average_cost())
    for ds9c_product in ds9c_products:
        inventory_value += (ds9c_product.current_stock or 0) * float(ds9c_product.average_cost())
    for np7a_product in np7a_products:
        inventory_value += (np7a_product.current_stock or 0) * float(np7a_product.average_cost())
        
    # Total units sold today
    total_sold = Sale.objects.aggregate(total=Sum('unit_sold'))['total'] or 0


    # 📊 Monthly sales vs purchase chart
    current_year = now().year

    sales_by_month = (
         Sale.objects
         .filter(sales_date__year=current_year)
         .annotate(month=TruncMonth('sales_date'))
         .values('month')
         .annotate(
          total_sales=Coalesce(
            Sum(F('unit_sold') * F('price'), output_field=FloatField()),
            V(0),
            output_field=FloatField()
        )
    )
    .order_by('month')
)


    purchases_by_month = (
      Purchase.objects
      .filter(purchase_date__year=current_year)
      .annotate(month=TruncMonth('purchase_date'))
      .values('month')
      .annotate(
        total_purchase=Coalesce(
            Sum(F('unit_purchased') * F('price'), output_field=FloatField()),
            V(0),
            output_field=FloatField()
        )
    )
    .order_by('month')
)


    monthly_data = {}
    for i in range(1, 13):
        month_name = calendar.month_abbr[i]
        monthly_data[month_name] = {'sales': 0, 'purchase': 0}

    for entry in sales_by_month:
        month = calendar.month_abbr[entry['month'].month]
        monthly_data[month]['sales'] = round(entry['total_sales'], 2)

    for entry in purchases_by_month:
        month = calendar.month_abbr[entry['month'].month]
        monthly_data[month]['purchase'] = round(entry['total_purchase'], 2)

    # Prepare chart lists
    labels = list(monthly_data.keys())
    sales = [monthly_data[m]['sales'] for m in labels]
    purchases = [monthly_data[m]['purchase'] for m in labels]
    profits = [s - p for s, p in zip(sales, purchases)]
    
    
    recent_products = Product.objects.order_by('-id')[:5]
    recent_bc = BC.objects.order_by('-id')[:5]
    recent_number8 = Number8.objects.order_by('-id')[:5]
    recent_ds9c = Ds9c.objects.order_by('-id')[:5]
    recent_np7a = Np7a.objects.order_by('-id')[:5]
    
    # Sort by total_sold descending and get the top one
    
    for item in all_items:
        if item.total_sold is None:
            item.total_sold = 0
        
    top_sold_items = sorted(all_items, key=lambda x: x.total_sold, reverse=True)[:5]
    
    # Today
    today_revenue = Sale.objects.filter(sales_date=today).aggregate(
    revenue=Sum(F('price') * F('unit_sold'), output_field=DecimalField())
    )['revenue'] or 0
    
    
    month_revenue = Sale.objects.filter(
    sales_date__year=today.year,
    sales_date__month=today.month
).aggregate(
    revenue=Sum(F('price') * F('unit_sold'), output_field=DecimalField())
)['revenue'] or 0

# This Year Revenue
    year_revenue = Sale.objects.filter(
    sales_date__year=today.year
    ).aggregate(
    revenue=Sum(F('price') * F('unit_sold'), output_field=DecimalField())
    )['revenue'] or 0

    

    # Final context
    context = {
        'labels': labels,
        'sales_data': sales,
        'purchase_data': purchases,
        'profit_data': profits,
        'products':products,
        'bc_products':bc_products,
        'number8_products':number8_products,
        'ds9c_products':ds9c_products,
        'np7a_products':np7a_products,
        'total_revenue': round(total_revenue, 2),
        'total_cost': round(total_cost, 2),
        'inventory_value': round(inventory_value, 2),
        'recent_products': recent_products,
        'recent_bc': recent_bc,
        'recent_number8': recent_number8,
        'recent_ds9c': recent_ds9c,
        'recent_np7a': recent_np7a,
        'top_sold_items':top_sold_items,
        'today_revenue': today_revenue,
        'month_revenue': month_revenue,
        'year_revenue': year_revenue,
        'total_sold':total_sold,
        'total_current_stock': total_current_stock,
    }

    return render(request, 'dashboard/index.html', context)



######## product function ############

@login_required
def addbc(request):
    if request.method == "POST":
        form = BcForm(request.POST, request.FILES)
        try:
            if form.is_valid():
                product = form.save(commit=False)
                product.created_by = request.user
                product.save()

                # Create a Notification
                Notification.objects.create(
                    user=request.user,
                    message=f"Product '{product.name}' was added successfully."
                )

                messages.success(request, "Product Added Successfully.")
                return redirect("dashboard:bclist")
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field.capitalize()}: {error}")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}")
    else:
        form = BcForm()
    return render(request, "dashboard/addbc.html", {"form": form})

def adddc(request):
    if request.method == "POST":
        form = DcForm(request.POST, request.FILES)
        try:
            if form.is_valid():
                product = form.save(commit=False)
                product.created_by = request.user
                product.save()

                # Create a Notification
                Notification.objects.create(
                    user=request.user,
                    message=f"Product '{product.name}' was added successfully."
                )

                messages.success(request, "Product Added Successfully.")
                return redirect("dashboard:dclist")
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field.capitalize()}: {error}")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}")
    else:
        form = DcForm()
    return render(request, "dashboard/adddc.html", {"form": form})

def addnumber(request):
    if request.method == "POST":
        form = NumberForm(request.POST, request.FILES)
        try:
            if form.is_valid():
                product = form.save(commit=False)
                product.created_by = request.user
                product.save()

                # Create a Notification
                Notification.objects.create(
                    user=request.user,
                    message=f"Product '{product.name}' was added successfully."
                )

                messages.success(request, "Product Added Successfully.")
                return redirect("dashboard:numlist")
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field.capitalize()}: {error}")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}")
    else:
        form = NumberForm()
    return render(request, "dashboard/addnum.html", {"form": form})

def addnp(request):
    if request.method == "POST":
        form = NpForm(request.POST, request.FILES)
        try:
            if form.is_valid():
                product = form.save(commit=False)
                product.created_by = request.user
                product.save()

                # Create a Notification
                Notification.objects.create(
                    user=request.user,
                    message=f"Product '{product.name}' was added successfully."
                )

                messages.success(request, "Product Added Successfully.")
                return redirect("dashboard:nplist")
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field.capitalize()}: {error}")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}")
    else:
        form = NpForm()
    return render(request, "dashboard/addnp.html", {"form": form})


@login_required
def addproduct(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        try:
            if form.is_valid():
                product = form.save(commit=False)
                product.created_by = request.user
                product.save()

                # Create a Notification
                Notification.objects.create(
                    user=request.user,
                    message=f"Product '{product.name}' was added successfully."
                )

                messages.success(request, "Product Added Successfully.")
                return redirect("dashboard:productlist")
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field.capitalize()}: {error}")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}")
    else:
        form = ProductForm()
    return render(request, "dashboard/addproduct.html", {"form": form})

     
@login_required
def editproduct(request, pk):
    product = get_object_or_404(Product, pk=pk, created_by=request.user)
    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            Notification.objects.create(
                    user=request.user,
                    message=f"Product '{product.name}' was edited successfully."
                )
            messages.success(request, "Product Updated Successfully.")
            return redirect('dashboard:productlist')
        else:
            messages.error(request, "Error updating Product")
    return render(request, 'dashboard/editproduct.html', {'form': form})
 
@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk, created_by=request.user)
    product_name = product.name
    product.delete()
    Notification.objects.create(
                    user=request.user,
                    message=f"Product '{product_name}' was deleted successfully."
                )
    messages.success(request, "product has been deleted successfully")
    return redirect("dashboard:productlist")
 
@login_required
def productlist(request):
   
   product = Product.objects.all().order_by('-id')
   
   context = {
       "product": product,
   }
   return render(request, "dashboard/productlist.html", context)



@login_required
def bclist(request):
   
   product = BC.objects.all().order_by('-id')
   
   context = {
       "product": product,
   }
   return render(request, "dashboard/bc.html", context)

@login_required
def editbc(request, pk):
    product = get_object_or_404(BC, pk=pk, created_by=request.user)
    form = BcForm(instance=product)
    if request.method == 'POST':
        form = BcForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            Notification.objects.create(
                    user=request.user,
                    message=f"Product '{product.name}' was edited successfully."
                )
            messages.success(request, "Product Updated Successfully.")
            return redirect('dashboard:bclist')
        else:
            messages.error(request, "Error updating Product")
    return render(request, 'dashboard/editbc.html', {'form': form})
 
@login_required
def delete_bc(request, pk):
    product = get_object_or_404(BC, pk=pk, created_by=request.user)
    product_name = product.name
    product.delete()
    Notification.objects.create(
                    user=request.user,
                    message=f"Product '{product_name}' was deleted successfully."
                )
    messages.success(request, "product has been deleted successfully")
    return redirect("dashboard:bclist")



@login_required
def delete_num(request, pk):
    product = get_object_or_404(Number8, pk=pk, created_by=request.user)
    product_name = product.name
    product.delete()
    Notification.objects.create(
                    user=request.user,
                    message=f"Product '{product_name}' was deleted successfully."
                )
    messages.success(request, "product has been deleted successfully")
    return redirect("dashboard:numlist")

@login_required
def editnum(request, pk):
    product = get_object_or_404(Number8, pk=pk, created_by=request.user)
    form = NumberForm(instance=product)
    if request.method == 'POST':
        form = NumberForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            Notification.objects.create(
                    user=request.user,
                    message=f"Product '{product.name}' was edited successfully."
                )
            messages.success(request, "Product Updated Successfully.")
            return redirect('dashboard:numlist')
        else:
            messages.error(request, "Error updating Product")
    return render(request, 'dashboard/editnum.html', {'form': form})

@login_required
def numlist(request):
   
   product =  Number8.objects.all().order_by('-id')
   
   context = {
       "product": product,
   }
   return render(request, "dashboard/num.html", context)

@login_required
def dclist(request):
   
   product = Ds9c.objects.all().order_by('-id')
   
   context = {
       "product": product,
   }
   return render(request, "dashboard/dc.html", context)

@login_required
def delete_dc(request, pk):
    product = get_object_or_404(Ds9c, pk=pk, created_by=request.user)
    product_name = product.name
    product.delete()
    Notification.objects.create(
                    user=request.user,
                    message=f"Product '{product_name}' was deleted successfully."
                )
    messages.success(request, "product has been deleted successfully")
    return redirect("dashboard:dclist")

@login_required
def editdc(request, pk):
    product = get_object_or_404(Ds9c, pk=pk, created_by=request.user)
    form = DcForm(instance=product)
    if request.method == 'POST':
        form = DcForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            Notification.objects.create(
                    user=request.user,
                    message=f"Product '{product.name}' was edited successfully."
                )
            messages.success(request, "Product Updated Successfully.")
            return redirect('dashboard:dclist')
        else:
            messages.error(request, "Error updating Product")
    return render(request, 'dashboard/editdc.html', {'form': form})


@login_required
def nplist(request):
   
   product =  Np7a.objects.all().order_by('-id')
   
   context = {
       "product": product,
   }
   return render(request, "dashboard/np.html", context)


@login_required
def editnp(request, pk):
    product = get_object_or_404(Np7a, pk=pk, created_by=request.user)
    form = NpForm(instance=product)
    if request.method == 'POST':
        form = NpForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            Notification.objects.create(
                    user=request.user,
                    message=f"Product '{product.name}' was edited successfully."
                )
            messages.success(request, "Product Updated Successfully.")
            return redirect('dashboard:nplist')
        else:
            messages.error(request, "Error updating Product")
    return render(request, 'dashboard/editnp.html', {'form': form})
######### purchse functions #########
@login_required
def delete_np(request, pk):
    product = get_object_or_404(Np7a, pk=pk, created_by=request.user)
    product_name = product.name
    product.delete()
    Notification.objects.create(
                    user=request.user,
                    message=f"Product '{product_name}' was deleted successfully."
                )
    messages.success(request, "product has been deleted successfully")
    return redirect("dashboard:nplist")


@login_required
def addpurchase(request):
    form = PurchaseForm()
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        try:
            if form.is_valid():
                purchase = form.save(commit=False)
                purchase.created_by = request.user
                purchase.save()

                # Create notification
                Notification.objects.create(
                    user=request.user,
                    message=f"New purchase added for ({purchase.unit_purchased} units at ₦{purchase.price})"
                )

                messages.success(request, "Purchase Added Successfully.")
                return redirect('dashboard:purchaselist')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field.capitalize()}: {error}")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}")
    else:
        form = PurchaseForm()
    
    return render(request, 'dashboard/addpurchase.html', {'form': form})

@login_required 
def edit_purchase(request, pk):
    purchase = get_object_or_404(Purchase, pk=pk, created_by=request.user)
    form = PurchaseForm(instance=purchase)
    if request.method == 'POST':
        form = PurchaseForm(request.POST, instance=purchase)
        if form.is_valid():
            form.save()
            Notification.objects.create(
                    user=request.user,
                    message=f"New purchase edited for({purchase.unit_purchased} units at ₦{purchase.price})"
                )
            messages.success(request, "Purchase Updated Successfully.")
            return redirect('dashboard:purchaselist')
        else:
            messages.error(request, "Error updating purchase.")
    return render(request, 'dashboard/editpurchase.html', {'form': form})
 
@login_required
def purchaselist(request):
    purchases = Purchase.objects.all().order_by('-id')
    context = {
        "purchases": purchases,
    }
    return render(request, "dashboard/purchaselist.html", context)
@login_required
def delete_purchase(request, pk):
    purchase = get_object_or_404(Purchase, pk=pk, created_by=request.user)
    purchase_name = purchase.product.name
    purchase.delete()
    Notification.objects.create(
                    user=request.user,
                    message=f"Purchase '{purchase_name}' was deleted successfully."
                )
    messages.success(request, "purchase has been deleted successfully")
    return redirect("dashboard:purchaselist")
 
########## sale functions #########
@login_required
def addsale(request):
    form = SaleForm()
    
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            try:
                sales = form.save(commit=False)
                sales.created_by = request.user
                sales.save()

                Notification.objects.create(
                    user=request.user,
                    message=f"New Sale added for ({sales.unit_sold} units at ₦{sales.price})"
                )

                messages.success(request, "Sale Added Successfully.")
                return redirect('dashboard:salelist')

            except ValidationError as ve:
                messages.error(request, ve.message)
            except Exception as e:
                messages.error(request, f"An unexpected error occurred: {str(e)}")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")

    return render(request, 'dashboard/addsale.html', {'form': form})

@login_required
def edit_sale(request, pk):
    purchase = get_object_or_404(Sale, pk=pk, created_by=request.user)
    form = SaleForm(instance=purchase)
    if request.method == 'POST':
        form = SaleForm(request.POST, instance=purchase)
        if form.is_valid():
            form.save()
            Notification.objects.create(
                    user=request.user,
                    message=f"New Sales edited for({purchase.unit_sold} units at ₦{purchase.price})"
                )
            messages.success(request, "Purchase Updated Successfully.")
            return redirect('dashboard:salelist')
        else:
            messages.error(request, "Error updating purchase.")
    return render(request, 'dashboard/editsale.html', {'form': form})
@login_required  
def salelist(request):
    sales = Sale.objects.all().order_by('-id')
    context = {
        "sales": sales,
    }
    return render(request, "dashboard/saleslist.html", context)
 
@login_required
def delete_sale(request, pk):
    sale = get_object_or_404(Sale, pk=pk, created_by=request.user)
    sale_name = sale.product.name
    sale.delete()
    Notification.objects.create(
                    user=request.user,
                    message=f"Sale '{sale_name}' was deleted successfully."
                )
    messages.success(request, "sale has been deleted successfully")
    return redirect("dashboard:salelist")
 
 
 ###### Type Controller #########
@login_required
def type(request):
    type = Type.objects.all()
    context = {
        "type": type,
    }
    return render(request, "dashboard/type.html", context)

@login_required
def addtype(request):
    form = TypeForm()
    if request.method == 'POST':
        form = TypeForm(request.POST)
        try:
            if form.is_valid():
                form.save()  
                Notification.objects.create(
                    user=request.user,
                    message=f"You added a new '{form.cleaned_data['name']}' type."
                )
                messages.success(request, "Type added successfully.")
                return redirect('dashboard:type')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field.capitalize()}: {error}")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}")
    
    # Move this out of the else block so GET and failed POST still work
    return render(request, 'dashboard/addtype.html', {'form': form})
   
@login_required
def edit_type(request, pk):
    purchase = get_object_or_404(Type, pk=pk)
    form = TypeForm(instance=purchase)
    if request.method == 'POST':
        form = TypeForm(request.POST, instance=purchase)
        if form.is_valid():
            form.save()
            Notification.objects.create(
                    user=request.user,
                    message=f"Type '{purchase.name}' was added successfully."
                )
            messages.success(request, "type Updated Successfully.")
            return redirect('dashboard:type')
        else:
            messages.error(request, "Error updating type.")
    return render(request, 'dashboard/edittype.html', {'form': form})

@login_required
def delete_type(request, pk):
    sale = get_object_or_404(Type, pk=pk)
    sale_name = sale.name
    sale.delete()
    Notification.objects.create(
                    user=request.user,
                    message=f"Type '{sale_name}' was deleted successfully."
                )
    messages.success(request, "Type has been deleted successfully")
    return redirect("dashboard:type")


def Login(request):
    if request.method =='POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        try:
            user = User.objects.get(username=username)
            user = authenticate(request,username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, "You are logged in")
                return redirect("dashboard:index")
            else:
                messages.warning(request, "username or password does not exist")
                return redirect("dashboard:login")
        except:
            messages.warning(request, f"User with this {username} does not exist")
                      
    if request.user.is_authenticated:
            messages.warning(request, "You are already logged in")
            return redirect("dashboard:index")
    return render(request, "dashboard/signin.html")

def logoutView(request):
      logout(request)
      messages.success(request, "You have been logged out")
      return redirect("dashboard:login")
  
  
@login_required
def notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'notifications': notifications,
    }
    return render(request, 'dashboard/activities.html', context)

####### Edit Admin Profile ########


@login_required
def edit_admin_profile(request):
    user = request.user
    form = AdminProfileForm(instance=user)

    if request.method == 'POST':
        form = AdminProfileForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')

            if password:
                user.set_password(password)
                update_session_auth_hash(request, user)  # 👈 Prevents logout

            user.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('dashboard:edit_admin')

    return render(request, 'dashboard/profile.html', {'form': form})


##Inventory

@login_required
def inventory(request):
    products = Product.objects.all()
    today = date.today()
    current_stock = Product.objects.aggregate(total=Sum('current_stock'))['total'] or 0
    

    # Revenue Calculations
    today_revenue = Sale.objects.filter(sales_date=today).aggregate(
        revenue=Sum(F('price') * F('unit_sold'), output_field=DecimalField())
    )['revenue'] or 0

    month_revenue = Sale.objects.filter(
        sales_date__year=today.year,
        sales_date__month=today.month
    ).aggregate(
        revenue=Sum(F('price') * F('unit_sold'), output_field=DecimalField())
    )['revenue'] or 0

    year_revenue = Sale.objects.filter(
        sales_date__year=today.year
    ).aggregate(
        revenue=Sum(F('price') * F('unit_sold'), output_field=DecimalField())
    )['revenue'] or 0
    

    # Inventory Data
    inventory_data = []
    for product in products:
        units_bought = Purchase.objects.filter(product=product).aggregate(
            total=Sum('unit_purchased')
        )['total'] or 0

        units_sold = Sale.objects.filter(product=product).aggregate(
            total=Sum('unit_sold')
        )['total'] or 0

        current_inventory = units_bought - units_sold

        if current_inventory == 0:
            status = "Out of Stock"
        elif current_inventory < 10:
            status = "Low Stock"
        else:
            status = "In Stock"

        inventory_data.append({
            'item_name': product.name,
            'item_id': product.item_id,
            'unit_bought': units_bought,
            'unit_sold': units_sold,
            'inventory': current_inventory,
            'status': status,
        })
    total_sold = Sale.objects.aggregate(total=Sum('unit_sold'))['total'] or 0
    

    context = {
        'today_revenue': today_revenue,
        'month_revenue': month_revenue,
        'year_revenue': year_revenue,
        'total_sold':total_sold,
        'inventory_data': inventory_data,
        'current_stock':current_stock
    }

    return render(request, 'dashboard/inventory.html', context)



def addcustomer(request):
    if request.method == "POST":
        form = CustomerForm(request.POST, request.FILES)
        try:
            if form.is_valid():
                product = form.save(commit=False)
                product.created_by = request.user
                product.save()

                # Create a Notification
                Notification.objects.create(
                    user=request.user,
                    message=f"customer '{product.name}' was added successfully."
                )

                messages.success(request, "customer Added Successfully.")
                return redirect("dashboard:customerlist")
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field.capitalize()}: {error}")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}")
    else:
        form = CustomerForm()
    return render(request, "dashboard/add-cutomer.html", {"form": form})

@login_required
def customer_list(request):
    customers = Customer.objects.all().order_by('-created_at')
    return render(request, 'dashboard/customer-list.html', {'customers': customers})

@login_required
def delete_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    product_name = customer.name
    customer.delete()
    Notification.objects.create(
                    user=request.user,
                    message=f"customer '{product_name}' was deleted successfully."
                )
    messages.success(request, "customer has been deleted")
    return redirect("dashboard:customerlist")
    
@login_required
def editcutomer(request, pk):
    product = get_object_or_404(Customer, pk=pk)
    form = CustomerForm(instance=product)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            Notification.objects.create(
                    user=request.user,
                    message=f"Customer '{product.name}' was edited successfully."
                )
            messages.success(request, "Customer Updated Successfully.")
            return redirect('dashboard:customerlist')
        else:
            messages.error(request, "Error updating Customer")
    return render(request, 'dashboard/edit-customer.html', {'form': form})