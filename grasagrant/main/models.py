from django.db import models
from django.shortcuts import reverse
from accounts.models import User

class Region(models.Model):

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Category(models.Model):

    tab_name = models.CharField(max_length=99)

    def __str__(self):
        return self.tab_name


class Type(models.Model):

    name = models.CharField(max_length=250)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="type")

    def __str__(self):
        return f'{self.category.tab_name}: {self.name}'

class Fz223(models.Model):

    fz223_name = models.ForeignKey(Type, on_delete=models.CASCADE, related_name="fz223")
    registration_number = models.CharField(max_length=50)
    create_date = models.DateField()
    url_EIS = models.TextField(null=True)
    url_VSRZ = models.TextField(null=True)
    name = models.TextField()
    full_name = models.TextField()
    legal_address = models.TextField()
    purchase_code_name = models.TextField()
    place = models.TextField(null=True)
    currency = models.CharField(max_length=50)
    initial_sum = models.CharField(max_length=50, null=True)
    submission_start_date = models.CharField(max_length=50, null=True)
    submission_close_date = models.CharField(max_length=50, null=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    favorite = models.ManyToManyField(User)

    def __str__(self):
        return f'{self.fz223_name.__str__()}: {self.name}'

    def get_absolute_url(self):
        return reverse('detailed', kwargs={'tab_name': 'Fz223','pk': self.id})

    class Meta:
        ordering = ('-create_date', )

class Fz44(models.Model):

    fz44_name = models.ForeignKey(Type, on_delete=models.CASCADE, related_name="fz44")
    fz44id = models.CharField(max_length=100)
    create_date = models.DateField()
    link = models.TextField()
    purchase_number = models.CharField(max_length=350)
    purchase_object = models.TextField()
    org_name = models.TextField()
    placing_way = models.TextField(null=True)
    start_date = models.CharField(max_length=350, null=True)
    end_date = models.CharField(max_length=350, null=True)
    place = models.TextField(null=True)
    max_price = models.CharField(max_length=350, null=True)
    currency = models.CharField(max_length=350, null=True)
    finance_source = models.CharField(max_length=300, null=True)
    aplication_guarantee = models.CharField(max_length=350, null=True)
    contract_guarantee = models.CharField(max_length=350, null=True)
    delivery = models.TextField(null=True)
    delivery_place = models.TextField(null=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    favorite = models.ManyToManyField(User)

    def __str__(self):
        return f'{self.fz44_name.__str__()}: {self.purchase_object}'

    def get_absolute_url(self):
        return reverse('detailed', kwargs={'tab_name': 'Fz44','pk': self.id})  

    class Meta:
        ordering = ('-create_date', )   


class DigitalEconomy(models.Model):
    
    digitaleconomy_name = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='digital_economy')
    document_number = models.CharField(max_length=100, null=True)
    date = models.DateField(null=True)
    text = models.TextField()
    link = models.TextField()

    favorite = models.ManyToManyField(User)

    def __str__(self):
        return f'{self.digitaleconomy_name.__str__()}: {self.text}'

    def get_absolute_url(self):
        return reverse('detailed', kwargs={'tab_name': 'DigitalEconomy','pk': self.id})

    class Meta:
        ordering = ('-date', ) 

class Grant(models.Model):
    grant_name = models.ForeignKey(Type, on_delete=models.CASCADE, related_name="grant")
    time = models.DateField()
    label = models.CharField(max_length=300, null=True)
    text = models.TextField()
    link = models.TextField(null=True)
    org = models.TextField(null=True)
    days = models.CharField(max_length=30, null=True)
    rouble = models.CharField(max_length=30, null=True)
    fond = models.TextField(null=True)
    fond_link = models.TextField(null=True)
    favorite = models.ManyToManyField(User)

    def __str__(self):
        return f'{self.grant_name.__str__()}: {self.text}'

    def get_absolute_url(self):
        return reverse('detailed', kwargs={'tab_name': 'Grant','pk': self.id})

    class Meta:
        ordering = ('-time', ) 

class Link(models.Model):

    link = models.TextField()
    grant_id = models.ForeignKey(Grant, on_delete=models.CASCADE, related_name="links")

    def __str__(self):
        return self.grant_id.__str__()
