from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from dashboard.models import  Type, Notification, BC, Number8, Ds9c, Np7a, Customer, BCPurchase, BCSale, NPurchase, NSale, DsPurchase, DSSale, N7Purchase
from .forms import BCPurchaseForm, BCSaleForm, NPurchaseForm, NSaleForm, DsPurchaseForm, DSSaleForm, N7PurchaseForm, N7SaleForm, N7Sale
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db.models import Sum, F, FloatField, Value as V

@login_required
def addbcpurchase(request):
    form = BCPurchaseForm()
    if request.method == 'POST':
        form = BCPurchaseForm(request.POST)
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
                return redirect('dashboard:bcplist')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field.capitalize()}: {error}")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}")
    else:
        form = BCPurchaseForm()
    
    return render(request, 'dashboard/addbcpurchase.html', {'form': form})



@login_required
def bcpurchaselist(request):
    purchases = BCPurchase.objects.all().order_by('-id')
    context = {
        "purchases": purchases,
    }
    return render(request, "dashboard/bcpurchaselist.html", context)


@login_required
def delete_bcpurchase(request, pk):
    purchase = get_object_or_404(BCPurchase, pk=pk, created_by=request.user)
    purchase_name = purchase.product.name
    purchase.delete()
    Notification.objects.create(
                    user=request.user,
                    message=f"Purchase '{purchase_name}' was deleted successfully."
                )
    messages.success(request, "purchase has been deleted successfully")
    return redirect("dashboard:bcplist")

@login_required 
def edit_bcpurchase(request, pk):
    purchase = get_object_or_404(BCPurchase, pk=pk, created_by=request.user)
    form = BCPurchaseForm(instance=purchase)
    if request.method == 'POST':
        form = BCPurchaseForm(request.POST, instance=purchase)
        if form.is_valid():
            form.save()
            Notification.objects.create(
                    user=request.user,
                    message=f"New purchase edited for({purchase.unit_purchased} units at ₦{purchase.price})"
                )
            messages.success(request, "Purchase Updated Successfully.")
            return redirect('dashboard:bcplist')
        else:
            messages.error(request, "Error updating purchase.")
    return render(request, 'dashboard/editbcpurchase.html', {'form': form})

# sales for bc

@login_required
def addbcsale(request):
    form = BCSaleForm()
    
    if request.method == 'POST':
        form = BCSaleForm(request.POST)
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
                return redirect('dashboard:bcsalelist')

            except ValidationError as ve:
                messages.error(request, ve.message)
            except Exception as e:
                messages.error(request, f"An unexpected error occurred: {str(e)}")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")

    return render(request, 'dashboard/addbcsale.html', {'form': form})

def bcsalelist(request):
    sales = BCSale.objects.all().order_by('-id')
    context = {
        "sales": sales,
    }
    return render(request, "dashboard/bcsaleslist.html", context)

@login_required
def delete_bcsale(request, pk):
    sale = get_object_or_404(BCSale, pk=pk, created_by=request.user)
    sale_name = sale.product.name
    sale.delete()
    Notification.objects.create(
                    user=request.user,
                    message=f"BC211-Sale '{sale_name}' was deleted successfully."
                )
    messages.success(request, "sale has been deleted successfully")
    return redirect("dashboard:bcsalelist")

@login_required
def bcedit_sale(request, pk):
    purchase = get_object_or_404(BCSale, pk=pk, created_by=request.user)
    form = BCSaleForm(instance=purchase)
    if request.method == 'POST':
        form = BCSaleForm(request.POST, instance=purchase)
        if form.is_valid():
            form.save()
            Notification.objects.create(
                    user=request.user,
                    message=f"New Sales edited for({purchase.unit_sold} units at ₦{purchase.price})"
                )
            messages.success(request, "Purchase Updated Successfully.")
            return redirect('dashboard:bcsalelist')
        else:
            messages.error(request, "Error updating purchase.")
    return render(request, 'dashboard/bceditsale.html', {'form': form})
 
# Number 8
 
@login_required
def addnpurchase(request):
    form = NPurchaseForm()
    if request.method == 'POST':
        form = NPurchaseForm(request.POST)
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
                return redirect('dashboard:npurchaselist')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field.capitalize()}: {error}")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}")
    else:
        form = NPurchaseForm()
    
    return render(request, 'dashboard/addnpurchase.html', {'form': form})


@login_required
def npurchaselist(request):
    purchases = NPurchase.objects.all().order_by('-id')
    context = {
        "purchases": purchases,
    }
    return render(request, "dashboard/npurchaselist.html", context)

@login_required
def delete_npurchase(request, pk):
    purchase = get_object_or_404(NPurchase, pk=pk, created_by=request.user)
    purchase_name = purchase.product.name
    purchase.delete()
    Notification.objects.create(
                    user=request.user,
                    message=f"Purchase '{purchase_name}' was deleted successfully."
                )
    messages.success(request, "purchase has been deleted successfully")
    return redirect("dashboard:npurchaselist")


@login_required 
def edit_npurchase(request, pk):
    purchase = get_object_or_404(NPurchase, pk=pk, created_by=request.user)
    form = NPurchaseForm(instance=purchase)
    if request.method == 'POST':
        form = NPurchaseForm(request.POST, instance=purchase)
        if form.is_valid():
            form.save()
            Notification.objects.create(
                    user=request.user,
                    message=f"New purchase edited for({purchase.unit_purchased} units at ₦{purchase.price})"
                )
            messages.success(request, "Purchase Updated Successfully.")
            return redirect('dashboard:npurchaselist')
        else:
            messages.error(request, "Error updating purchase.")
    return render(request, 'dashboard/editnpurchase.html', {'form': form})


@login_required
def addnsale(request):
    form = NSaleForm()
    
    if request.method == 'POST':
        form = NSaleForm(request.POST)
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
                return redirect('dashboard:nsalelist')

            except ValidationError as ve:
                messages.error(request, ve.message)
            except Exception as e:
                messages.error(request, f"An unexpected error occurred: {str(e)}")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")

    return render(request, 'dashboard/addnsale.html', {'form': form})


def nsalelist(request):
    sales = NSale.objects.all().order_by('-id')
    context = {
        "sales": sales,
    }
    return render(request, "dashboard/nsaleslist.html", context)


@login_required
def delete_nsale(request, pk):
    sale = get_object_or_404(NSale, pk=pk, created_by=request.user)
    sale_name = sale.product.name
    sale.delete()
    Notification.objects.create(
                    user=request.user,
                    message=f"80800 '{sale_name}' was deleted successfully."
                )
    messages.success(request, "sale has been deleted successfully")
    return redirect("dashboard:nsalelist")


@login_required
def nedit_sale(request, pk):
    purchase = get_object_or_404(NSale, pk=pk, created_by=request.user)
    form = NSaleForm(instance=purchase)
    if request.method == 'POST':
        form = NSaleForm(request.POST, instance=purchase)
        if form.is_valid():
            form.save()
            Notification.objects.create(
                    user=request.user,
                    message=f"New Sales edited for({purchase.unit_sold} units at ₦{purchase.price})"
                )
            messages.success(request, "Purchase Updated Successfully.")
            return redirect('dashboard:nsalelist')
        else:
            messages.error(request, "Error updating purchase.")
    return render(request, 'dashboard/neditsale.html', {'form': form})


@login_required
def add_dspurchase(request):
    form = DsPurchaseForm()
    if request.method == 'POST':
        form = DsPurchaseForm(request.POST)
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
                return redirect('dashboard:dpurchaselist')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field.capitalize()}: {error}")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}")
    else:
        form = DsPurchaseForm()
    
    return render(request, 'dashboard/addnpurchase.html', {'form': form})

@login_required
def dspurchaselist(request):
    purchases = DsPurchase.objects.all().order_by('-id')
    context = {
        "purchases": purchases,
    }
    return render(request, "dashboard/dspurchaselist.html", context)

@login_required
def delete_dpurchase(request, pk):
    purchase = get_object_or_404(DsPurchase, pk=pk, created_by=request.user)
    purchase_name = purchase.product.name
    purchase.delete()
    Notification.objects.create(
                    user=request.user,
                    message=f"Purchase '{purchase_name}' was deleted successfully."
                )
    messages.success(request, "purchase has been deleted successfully")
    return redirect("dashboard:dpurchaselist")


@login_required 
def edit_dpurchase(request, pk):
    purchase = get_object_or_404(DsPurchase, pk=pk, created_by=request.user)
    form = DsPurchaseForm(instance=purchase)
    if request.method == 'POST':
        form = DsPurchaseForm(request.POST, instance=purchase)
        if form.is_valid():
            form.save()
            Notification.objects.create(
                    user=request.user,
                    message=f"New purchase edited for({purchase.unit_purchased} units at ₦{purchase.price})"
                )
            messages.success(request, "Purchase Updated Successfully.")
            return redirect('dashboard:dpurchaselist')
        else:
            messages.error(request, "Error updating purchase.")
    return render(request, 'dashboard/editdpurchase.html', {'form': form})

@login_required
def adddsale(request):
    form = DSSaleForm()
    
    if request.method == 'POST':
        form = DSSaleForm(request.POST)
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
                return redirect('dashboard:dsalelist')

            except ValidationError as ve:
                messages.error(request, ve.message)
            except Exception as e:
                messages.error(request, f"An unexpected error occurred: {str(e)}")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")

    return render(request, 'dashboard/adddsale.html', {'form': form})

def dsalelist(request):
    sales = DSSale.objects.all().order_by('-id')
    context = {
        "sales": sales,
    }
    return render(request, "dashboard/dsaleslist.html", context)

@login_required
def delete_dsale(request, pk):
    sale = get_object_or_404(DSSale, pk=pk, created_by=request.user)
    sale_name = sale.product.name
    sale.delete()
    Notification.objects.create(
                    user=request.user,
                    message=f"DS-9C '{sale_name}' was deleted successfully."
                )
    messages.success(request, "sale has been deleted successfully")
    return redirect("dashboard:dsalelist")


@login_required
def dedit_sale(request, pk):
    purchase = get_object_or_404(DSSale, pk=pk, created_by=request.user)
    form = DSSaleForm(instance=purchase)
    if request.method == 'POST':
        form = DSSaleForm(request.POST, instance=purchase)
        if form.is_valid():
            form.save()
            Notification.objects.create(
                    user=request.user,
                    message=f"New Sales edited for({purchase.unit_sold} units at ₦{purchase.price})"
                )
            messages.success(request, "Purchase Updated Successfully.")
            return redirect('dashboard:dsalelist')
        else:
            messages.error(request, "Error updating purchase.")
    return render(request, 'dashboard/deditsale.html', {'form': form})


### Np7

@login_required
def add_n7purchase(request):
    form = N7PurchaseForm()
    if request.method == 'POST':
        form = N7PurchaseForm(request.POST)
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
                return redirect('dashboard:np_purchaselist')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field.capitalize()}: {error}")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}")
    else:
        form = N7PurchaseForm()
    
    return render(request, 'dashboard/addnp_purchase.html', {'form': form})

@login_required
def n7purchaselist(request):
    purchases = N7Purchase.objects.all().order_by('-id')
    context = {
        "purchases": purchases,
    }
    return render(request, "dashboard/np_purchaselist.html", context)


@login_required
def delete_n7purchase(request, pk):
    purchase = get_object_or_404(N7Purchase, pk=pk, created_by=request.user)
    purchase_name = purchase.product.name
    purchase.delete()
    Notification.objects.create(
                    user=request.user,
                    message=f"Purchase '{purchase_name}' was deleted successfully."
                )
    messages.success(request, "purchase has been deleted successfully")
    return redirect("dashboard:np_purchaselist")


@login_required 
def edit_n7purchase(request, pk):
    purchase = get_object_or_404(N7Purchase, pk=pk, created_by=request.user)
    form = N7PurchaseForm(instance=purchase)
    if request.method == 'POST':
        form = N7PurchaseForm(request.POST, instance=purchase)
        if form.is_valid():
            form.save()
            Notification.objects.create(
                    user=request.user,
                    message=f"New purchase edited for({purchase.unit_purchased} units at ₦{purchase.price})"
                )
            messages.success(request, "Purchase Updated Successfully.")
            return redirect('dashboard:np_purchaselist')
        else:
            messages.error(request, "Error updating purchase.")
    return render(request, 'dashboard/editdpurchase.html', {'form': form})

@login_required
def ad_np7sale(request):
    form = N7SaleForm()
    
    if request.method == 'POST':
        form = N7SaleForm(request.POST)
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
                return redirect('dashboard:np_salelist')

            except ValidationError as ve:
                messages.error(request, ve.message)
            except Exception as e:
                messages.error(request, f"An unexpected error occurred: {str(e)}")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")

    return render(request, 'dashboard/ad_npsale.html', {'form': form})

def np_salelist(request):
    sales = N7Sale.objects.all().order_by('-id')
    context = {
        "sales": sales,
    }
    return render(request, "dashboard/np_sales.html", context)

@login_required
def delete_npsale(request, pk):
    sale = get_object_or_404(N7Sale, pk=pk, created_by=request.user)
    sale_name = sale.product.name
    sale.delete()
    Notification.objects.create(
                    user=request.user,
                    message=f"DS-9C '{sale_name}' was deleted successfully."
                )
    messages.success(request, "sale has been deleted successfully")
    return redirect("dashboard:np_salelist")


@login_required
def edit_npsale(request, pk):
    purchase = get_object_or_404(N7Sale, pk=pk, created_by=request.user)
    form = N7SaleForm(instance=purchase)
    if request.method == 'POST':
        form = N7SaleForm(request.POST, instance=purchase)
        if form.is_valid():
            form.save()
            Notification.objects.create(
                    user=request.user,
                    message=f"New Sales edited for({purchase.unit_sold} units at ₦{purchase.price})"
                )
            messages.success(request, "Purchase Updated Successfully.")
            return redirect('dashboard:np_salelist')
        else:
            messages.error(request, "Error updating purchase.")
    return render(request, 'dashboard/deditsale.html', {'form': form})


#### inventory for bch
@login_required
def bc_inventory(request):
    products = BC.objects.all()

    inventory_data = []
    for product in products:
        # Calculate total units bought for this product
        units_bought = BCPurchase.objects.filter(product=product).aggregate(
            total=Sum('unit_purchased')
        )['total'] or 0

        # Calculate total units sold for this product
        units_sold = BCSale.objects.filter(product=product).aggregate(
            total=Sum('unit_sold')
        )['total'] or 0

        # Calculate current stock / inventory
        current_inventory = units_bought - units_sold

        # Determine stock status
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

    return render(request, 'dashboard/bc_inventory.html', {'inventory_data': inventory_data})

#### 80800 inventory
@login_required
def nu_inventory(request):
    products = Number8.objects.all()

    inventory_data = []
    for product in products:
        # Calculate total units bought for this product
        units_bought = NPurchase.objects.filter(product=product).aggregate(
            total=Sum('unit_purchased')
        )['total'] or 0

        # Calculate total units sold for this product
        units_sold = NSale.objects.filter(product=product).aggregate(
            total=Sum('unit_sold')
        )['total'] or 0

        # Calculate current stock / inventory
        current_inventory = units_bought - units_sold

        # Determine stock status
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

    return render(request, 'dashboard/nu_inventory.html', {'inventory_data': inventory_data})

### ds-9c inventory
@login_required
def ds_inventory(request):
    products = Ds9c.objects.all()

    inventory_data = []
    for product in products:
        # Calculate total units bought for this product
        units_bought = DsPurchase.objects.filter(product=product).aggregate(
            total=Sum('unit_purchased')
        )['total'] or 0

        # Calculate total units sold for this product
        units_sold = DSSale.objects.filter(product=product).aggregate(
            total=Sum('unit_sold')
        )['total'] or 0

        # Calculate current stock / inventory
        current_inventory = units_bought - units_sold

        # Determine stock status
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

    return render(request, 'dashboard/ds_inventory.html', {'inventory_data': inventory_data})

#### NP7A

@login_required
def np_inventory(request):
    products = Np7a.objects.all()

    inventory_data = []
    for product in products:
        # Calculate total units bought for this product
        units_bought = N7Purchase.objects.filter(product=product).aggregate(
            total=Sum('unit_purchased')
        )['total'] or 0

        # Calculate total units sold for this product
        units_sold = N7Sale.objects.filter(product=product).aggregate(
            total=Sum('unit_sold')
        )['total'] or 0

        # Calculate current stock / inventory
        current_inventory = units_bought - units_sold

        # Determine stock status
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

    return render(request, 'dashboard/n7_inventory.html', {'inventory_data': inventory_data})