from django.db import models

# Create your models here.

class Category(models.Model):

    tab_name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.tab_name}'

class Type(models.Model):

    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="type")

    def __str__(self):
        return f'{self.category.tab_name}: {self.name}'

class Fz223(models.Model):

    fz = models.ForeignKey(Type, on_delete=models.CASCADE, related_name="fz223")
    registration_number = models.CharField(max_length=100)
    create_date = models.DateField()
    url_EIS = models.TextField()
    ulr_VSRZ = models.TextField()
    name = models.CharField(max_length=300)
    full_name = models.CharField(max_length=300)
    legal_address = models.CharField(max_length=300)
    purchase_code_name = models.CharField(max_length=300)
    place = models.CharField(max_length=300)
    currency = models.CharField(max_length=100)
    initial_sum = models.CharField(max_length=100)
    submission_start_date = models.CharField(max_length=100)
    submission_close_date = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.fz.__str__()}:{self.name}'


class Fz44(models.Model):

    fz = models.ForeignKey(Type, on_delete=models.CASCADE, related_name="fz44")
    fz44id = models.CharField(max_length=100)
    link = models.TextField()
    purchase_number = models.CharField(max_length=100)
    purchase_object = models.CharField(max_length=300)
    org_name = models.CharField(max_length=100)
    placing_way = models.CharField(max_length=100)
    start_date = models.CharField(max_length=100)
    end_date = models.CharField(max_length=100)
    place = models.TextField()
    max_price = models.CharField(max_length=100)
    currency = models.CharField(max_length=100)
    finance_source = models.CharField(max_length=100)
    aplication_guarantee = models.CharField(max_length=100)
    contract_guarantee = models.CharField(max_length=100)
    delivery = models.CharField(max_length=300)
    delivery_place = models.CharField(max_length=300)

class Fcp(models.Model):

    gp_name = models.ForeignKey(Type, on_delete=models.CASCADE, related_name="fcp")
    time = models.DateField()
    card_name = models.CharField(max_length=300)
    title = models.CharField(max_length=300)
    lead = models.TextField()
    link = models.CharField(max_length=300)

class Grant(models.Model):
    grant_name = models.ForeignKey(Type, on_delete=models.CASCADE, related_name="grants")
    time = models.DateField(blank=True)
    label = models.CharField(max_length=100, blank=True)
    text = models.TextField(blank=True)
    link = models.CharField(max_length=300, blank=True, )
    org = models.CharField(max_length=300, blank=True)
    days = models.CharField(max_length=30, blank=True)
    rouble = models.CharField(max_length=30, blank=True)
    fond = models.CharField(max_length=300, blank=True)
    fond_link = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return f'{self.grant_name.__str__()}: {self.id}'


class Link(models.Model):

    link = models.CharField(max_length=300)
    grant_id = models.ForeignKey(Grant, on_delete=models.CASCADE, related_name="links")
