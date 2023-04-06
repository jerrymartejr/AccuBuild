from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    role = models.CharField(max_length=20, blank=True)


class Client(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    image = models.ImageField(upload_to="client_logos/", null=True, blank=True)

    def __str__(self):
        return self.name
    

class Project(models.Model):
    name = models.CharField(max_length=100)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='scopes')
    address = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    status = models.CharField(max_length=100)
    area = models.DecimalField(max_digits=8, decimal_places=2)
    bid_deadline = models.DateField()
    estimator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="estimator_projects")
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name="manager_projects")
    timestamp = models.DateTimeField(auto_now_add=True)
    material = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=True, null=True)
    labor = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=True, null=True)
    equipment = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=True, null=True)
    ocm = models.DecimalField(max_digits=20, decimal_places=2, default=10 , blank=True, null=True)
    profit = models.DecimalField(max_digits=20, decimal_places=2, default=12, blank=True, null=True)
    vat = models.DecimalField(max_digits=20, decimal_places=2, default=12 , blank=True, null=True)
    progress = models.CharField(max_length=20, default='on-going', blank=True, null=True)
    reject_msg = models.CharField(max_length=200, default='', blank=True, null=True)

    @property
    def direct_cost(self):
        return self.material + self.labor + self.equipment
    
    @property
    def markup(self):
        return self.ocm + self.profit
    
    @property
    def material_no_vat(self):
        return round(self.material * (1 + (self.markup / 100)), 2)
    
    @property
    def material_w_vat(self):
        return round(self.material_no_vat * (1 + (self.vat / 100)), 2)
    
    @property
    def labor_no_vat(self):
        return round(self.labor * (1 + (self.markup / 100)), 2)
    
    @property
    def labor_w_vat(self):
        return round(self.labor_no_vat * (1 + (self.vat / 100)), 2)
    
    @property
    def equipment_no_vat(self):
        return round(self.equipment * (1 + (self.markup / 100)), 2)
    
    @property
    def equipment_w_vat(self):
        return round(self.equipment_no_vat * (1 + (self.vat / 100)), 2)
    
    def __str__(self):
        return f"Project name: {self.name}, Client: {self.client}"


class Division(models.Model):
    name = models.CharField(max_length=100)
    project = models.ManyToManyField(Project, blank=True, related_name="divisions")

    def __str__(self):
        return self.name
    

class DivisionCost(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='division_costs')
    division = models.ForeignKey(Division, on_delete=models.CASCADE, related_name='division_costs')
    material = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    labor = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    equipment = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    @property
    def direct_cost(self):
        return self.material + self.labor + self.equipment


class Scope(models.Model):
    name = models.CharField(max_length=100)
    division = models.ForeignKey(Division, on_delete=models.CASCADE, related_name='scopes')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='scopes', null=True, blank=True)
    qty = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    unit = models.CharField(max_length=20, default="lot")
    material = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    labor = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    equipment = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    @property
    def direct_cost(self):
        return self.material + self.labor + self.equipment

    def __str__(self):
        return self.name


class ItemType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=100)
    scope = models.ForeignKey(Scope, on_delete=models.CASCADE, related_name="items")
    qty = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    unit = models.CharField(max_length=20, default="lot")
    unit_price = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    amount = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    type = models.ForeignKey(ItemType, on_delete=models.CASCADE, related_name="items", blank=True, null=True)

    def __str__(self):
        return self.name