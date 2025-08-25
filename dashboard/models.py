from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Sum, F
from decimal import Decimal
# Create your models here.

class Type(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    item_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, null=True, blank=True)
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    current_stock = models.IntegerField(default=0, null=True, blank=True)
    total_sold = models.IntegerField(default=0, null=True, blank=True)
    total_cost_value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    created_by = models.ForeignKey(User,related_name='product', null=True, blank=True, on_delete=models.CASCADE)
    

    def __str__(self):
        return f"{self.name} ({self.item_id})"
    
    def average_cost(self):
        purchases = self.purchase_set.aggregate(
            total_cost=Sum(F('price') * F('unit_purchased')),
            total_units=Sum('unit_purchased')
        )
        total_cost = purchases['total_cost'] or Decimal('0.00')
        total_units = purchases['total_units'] or 0
        return round(total_cost / total_units, 2) if total_units else Decimal('0.00')
    
# BC MODELS
class BC(models.Model):
    item_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, null=True, blank=True)
    unit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    current_stock = models.IntegerField(default=0, null=True, blank=True)
    total_sold = models.IntegerField(default=0, null=True, blank=True)
    total_cost_value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    created_by = models.ForeignKey(User,related_name='bc211', null=True, blank=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.name} ({self.item_id})"
    
    def average_cost(self):
        purchases = self.bcpurchase_set.aggregate(
            total_cost=Sum(F('price') * F('unit_purchased')),
            total_units=Sum('unit_purchased')
        )
        total_cost = purchases['total_cost'] or Decimal('0.00')
        total_units = purchases['total_units'] or 0
        return round(total_cost / total_units, 2) if total_units else Decimal('0.00')


class BCPurchase(models.Model):
    product = models.ForeignKey(BC, on_delete=models.CASCADE)
    purchase_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, null=True, blank=True)
    unit_purchased = models.PositiveIntegerField()
    point_of_contact = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, related_name='bcpurchase', null=True, blank=True, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.product.current_stock = (self.product.current_stock or 0) + self.unit_purchased
        self.product.save()

    def delete(self, *args, **kwargs):
        self.product.current_stock = (self.product.current_stock or 0) - self.unit_purchased
        self.product.save()

        super().delete(*args, **kwargs)


class BCSale(models.Model):
    product = models.ForeignKey(BC, on_delete=models.CASCADE)
    sales_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, null=True, blank=True)
    unit_sold = models.PositiveIntegerField()
    point_of_contact = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, related_name='bcsales', null=True, blank=True, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.pk:
            # Update case
            previous = BCSale.objects.get(pk=self.pk)
            delta = self.unit_sold - previous.unit_sold
        else:
            # New sale
            delta = self.unit_sold

        # Ensure enough stock
        if delta > 0 and delta > (self.product.current_stock or 0):
            raise ValidationError(
                f"Not enough stock! Available: {self.product.current_stock or 0}, Tried to sell additional: {delta}"
            )

        # Adjust stock & total_sold
        self.product.current_stock = (self.product.current_stock or 0) - delta
        self.product.total_sold = (self.product.total_sold or 0) + delta
        self.product.save()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Restore stock & total_sold
        self.product.current_stock = (self.product.current_stock or 0) + self.unit_sold
        self.product.total_sold = (self.product.total_sold or 0) - self.unit_sold
        self.product.save()
        super().delete(*args, **kwargs)



class Number8(models.Model):
    item_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, null=True, blank=True)
    unit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    current_stock = models.IntegerField(default=0, null=True, blank=True)
    total_sold = models.IntegerField(default=0, null=True, blank=True)
    total_cost_value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    created_by = models.ForeignKey(User,related_name='number8', null=True, blank=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.name} ({self.item_id})"
    
    def average_cost(self):
        purchases = self.npurchase_set.aggregate(
            total_cost=Sum(F('price') * F('unit_purchased')),
            total_units=Sum('unit_purchased')
        )
        total_cost = purchases['total_cost'] or Decimal('0.00')
        total_units = purchases['total_units'] or 0
        return round(total_cost / total_units, 2) if total_units else Decimal('0.00')



class NPurchase(models.Model):
    product = models.ForeignKey(Number8, on_delete=models.CASCADE)
    purchase_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, null=True, blank=True)
    unit_purchased = models.PositiveIntegerField()
    point_of_contact = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, related_name='Npurchase', null=True, blank=True, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.product.current_stock = (self.product.current_stock or 0) + self.unit_purchased
        self.product.save()

    def delete(self, *args, **kwargs):
        self.product.current_stock = (self.product.current_stock or 0) - self.unit_purchased
        self.product.save()

        super().delete(*args, **kwargs)
        

class NSale(models.Model):
    product = models.ForeignKey(Number8, on_delete=models.CASCADE)
    sales_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, null=True, blank=True)
    unit_sold = models.PositiveIntegerField()
    point_of_contact = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, related_name='Nsales', null=True, blank=True, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.pk:
            # Update case
            previous = NSale.objects.get(pk=self.pk)
            delta = self.unit_sold - previous.unit_sold
        else:
            # New sale
            delta = self.unit_sold

        # Ensure enough stock
        if delta > 0 and delta > (self.product.current_stock or 0):
            raise ValidationError(
                f"Not enough stock! Available: {self.product.current_stock or 0}, Tried to sell additional: {delta}"
            )

        # Adjust stock & total_sold
        self.product.current_stock = (self.product.current_stock or 0) - delta
        self.product.total_sold = (self.product.total_sold or 0) + delta
        self.product.save()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Restore stock & total_sold
        self.product.current_stock = (self.product.current_stock or 0) + self.unit_sold
        self.product.total_sold = (self.product.total_sold or 0) - self.unit_sold
        self.product.save()
        super().delete(*args, **kwargs)

class Ds9c(models.Model):
    item_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, null=True, blank=True)
    unit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    current_stock = models.IntegerField(default=0, null=True, blank=True)
    total_sold = models.IntegerField(default=0, null=True, blank=True)
    total_cost_value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    created_by = models.ForeignKey(User,related_name='ds', null=True, blank=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.name} ({self.item_id})"
    
    def average_cost(self):
        purchases = self.dspurchase_set.aggregate(
            total_cost=Sum(F('price') * F('unit_purchased')),
            total_units=Sum('unit_purchased')
        )
        total_cost = purchases['total_cost'] or Decimal('0.00')
        total_units = purchases['total_units'] or 0
        return round(total_cost / total_units, 2) if total_units else Decimal('0.00')

class DsPurchase(models.Model):
    product = models.ForeignKey(Ds9c, on_delete=models.CASCADE)
    purchase_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, null=True, blank=True)
    unit_purchased = models.PositiveIntegerField()
    point_of_contact = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, related_name='dspurchase', null=True, blank=True, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.product.current_stock = (self.product.current_stock or 0) + self.unit_purchased
        self.product.save()

    def delete(self, *args, **kwargs):
        self.product.current_stock = (self.product.current_stock or 0) - self.unit_purchased
        self.product.save()

        super().delete(*args, **kwargs)
        
class DSSale(models.Model):
    product = models.ForeignKey(Ds9c, on_delete=models.CASCADE)
    sales_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, null=True, blank=True)
    unit_sold = models.PositiveIntegerField()
    point_of_contact = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, related_name='dssales', null=True, blank=True, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.pk:
            # Update case
            previous = DSSale.objects.get(pk=self.pk)
            delta = self.unit_sold - previous.unit_sold
        else:
            # New sale
            delta = self.unit_sold

        # Ensure enough stock
        if delta > 0 and delta > (self.product.current_stock or 0):
            raise ValidationError(
                f"Not enough stock! Available: {self.product.current_stock or 0}, Tried to sell additional: {delta}"
            )

        # Adjust stock & total_sold
        self.product.current_stock = (self.product.current_stock or 0) - delta
        self.product.total_sold = (self.product.total_sold or 0) + delta
        self.product.save()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Restore stock & total_sold
        self.product.current_stock = (self.product.current_stock or 0) + self.unit_sold
        self.product.total_sold = (self.product.total_sold or 0) - self.unit_sold
        self.product.save()
        super().delete(*args, **kwargs)
    
class Np7a(models.Model):
    item_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, null=True, blank=True)
    unit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    current_stock = models.IntegerField(default=0, null=True, blank=True)
    total_sold = models.IntegerField(default=0, null=True, blank=True)
    total_cost_value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    created_by = models.ForeignKey(User,related_name='np', null=True, blank=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.name} ({self.item_id})"
    
    def average_cost(self):
        purchases = self.n7purchase_set.aggregate(
            total_cost=Sum(F('price') * F('unit_purchased')),
            total_units=Sum('unit_purchased')
        )
        total_cost = purchases['total_cost'] or Decimal('0.00')
        total_units = purchases['total_units'] or 0
        return round(total_cost / total_units, 2) if total_units else Decimal('0.00')
    
class N7Purchase(models.Model):
    product = models.ForeignKey(Np7a, on_delete=models.CASCADE)
    purchase_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, null=True, blank=True)
    unit_purchased = models.PositiveIntegerField()
    point_of_contact = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, related_name='n7purchase', null=True, blank=True, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.product.current_stock = (self.product.current_stock or 0) + self.unit_purchased
        self.product.save()

    def delete(self, *args, **kwargs):
        self.product.current_stock = (self.product.current_stock or 0) - self.unit_purchased
        self.product.save()

        super().delete(*args, **kwargs)
        
class N7Sale(models.Model):
    product = models.ForeignKey(Np7a, on_delete=models.CASCADE)
    sales_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, null=True, blank=True)
    unit_sold = models.PositiveIntegerField()
    point_of_contact = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, related_name='n7sales', null=True, blank=True, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.pk:
            # Update case
            previous = N7Sale.objects.get(pk=self.pk)
            delta = self.unit_sold - previous.unit_sold
        else:
            # New sale
            delta = self.unit_sold

        # Ensure enough stock
        if delta > 0 and delta > (self.product.current_stock or 0):
            raise ValidationError(
                f"Not enough stock! Available: {self.product.current_stock or 0}, Tried to sell additional: {delta}"
            )

        # Adjust stock & total_sold
        self.product.current_stock = (self.product.current_stock or 0) - delta
        self.product.total_sold = (self.product.total_sold or 0) + delta
        self.product.save()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Restore stock & total_sold
        self.product.current_stock = (self.product.current_stock or 0) + self.unit_sold
        self.product.total_sold = (self.product.total_sold or 0) - self.unit_sold
        self.product.save()
        super().delete(*args, **kwargs)
    



class Purchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    purchase_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, null=True, blank=True)
    unit_purchased = models.PositiveIntegerField()
    point_of_contact = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, related_name='purchase', null=True, blank=True, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.pk:  # Editing existing purchase
            previous = Purchase.objects.get(pk=self.pk)
            delta = self.unit_purchased - previous.unit_purchased
        else:
            delta = self.unit_purchased  # New purchase

        self.product.current_stock = (self.product.current_stock or 0) + delta
        self.product.save()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Reverse the stock
        self.product.current_stock = (self.product.current_stock or 0) - self.unit_purchased
        self.product.save()
        super().delete(*args, **kwargs)




class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    sales_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, null=True, blank=True)
    unit_sold = models.PositiveIntegerField()
    point_of_contact = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, related_name='sales', null=True, blank=True, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.pk:
            # Update case
            previous = Sale.objects.get(pk=self.pk)
            delta = self.unit_sold - previous.unit_sold
        else:
            # New sale
            delta = self.unit_sold

        # Ensure enough stock
        if delta > 0 and delta > (self.product.current_stock or 0):
            raise ValidationError(
                f"Not enough stock! Available: {self.product.current_stock or 0}, Tried to sell additional: {delta}"
            )

        # Adjust stock & total_sold
        self.product.current_stock = (self.product.current_stock or 0) - delta
        self.product.total_sold = (self.product.total_sold or 0) + delta
        self.product.save()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Restore stock & total_sold
        self.product.current_stock = (self.product.current_stock or 0) + self.unit_sold
        self.product.total_sold = (self.product.total_sold or 0) - self.unit_sold
        self.product.save()
        super().delete(*args, **kwargs)




class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:50]}"  # Display first 50 characters of the message
    
    
class Customer(models.Model):
    name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    
    