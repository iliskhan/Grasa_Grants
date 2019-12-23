from django.db import models

class Region(models.Model):

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Category(models.Model):

    tab_name = models.CharField(max_length=100)

    def __str__(self):
        return self.tab_name


class Type(models.Model):

    name = models.CharField(max_length=300)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="type")

    def __str__(self):
        return f'{self.category.tab_name}: {self.name}'

class Fz223(models.Model):

    fz = models.ForeignKey(Type, on_delete=models.CASCADE, related_name="fz223")
    registration_number = models.CharField(max_length=100)
    create_date = models.DateField()
    url_EIS = models.TextField(null=True)
    url_VSRZ = models.TextField(null=True)
    name = models.CharField(max_length=300)
    full_name = models.CharField(max_length=300)
    legal_address = models.CharField(max_length=300)
    purchase_code_name = models.CharField(max_length=300)
    place = models.CharField(max_length=300, null=True)
    currency = models.CharField(max_length=100)
    initial_sum = models.CharField(max_length=100, null=True)
    submission_start_date = models.CharField(max_length=100, null=True)
    submission_close_date = models.CharField(max_length=100, null=True)

    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.fz.__str__()}: {self.name}'

class Fz44(models.Model):

    fz = models.ForeignKey(Type, on_delete=models.CASCADE, related_name="fz44")
    fz44id = models.CharField(max_length=100)
    link = models.TextField()
    purchase_number = models.CharField(max_length=100)
    purchase_object = models.CharField(max_length=300)
    org_name = models.CharField(max_length=100)
    placing_way = models.CharField(max_length=100, null=True)
    start_date = models.CharField(max_length=100, null=True)
    end_date = models.CharField(max_length=100, null=True)
    place = models.TextField(null=True)
    max_price = models.CharField(max_length=100, null=True)
    currency = models.CharField(max_length=100, null=True)
    finance_source = models.CharField(max_length=100, null=True)
    aplication_guarantee = models.CharField(max_length=100, null=True)
    contract_guarantee = models.CharField(max_length=100, null=True)
    delivery = models.CharField(max_length=300, null=True)
    delivery_place = models.CharField(max_length=300, null=True)

    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.fz.__str__()}: {self.purchase_object}'

class Fcp(models.Model):

    gp_name = models.ForeignKey(Type, on_delete=models.CASCADE, related_name="fcp")
    time = models.DateField()
    card_name = models.CharField(max_length=300, null=True)
    title = models.CharField(max_length=300, null=True)
    lead = models.TextField(null=True)
    link = models.CharField(max_length=300, null=True)

    def __str__(self):
        return f'{self.gp_name.__str__()}: {self.title}'

class DigitalEconomy(models.Model):
    
    type_name = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='digital_economy')
    document_number = models.CharField(mas_length=50, null=True)
    label = models.CharField(max_length=150, null=True)
    date = models.DateField(null=True)
    text = models.TextField()
    link = models.CharField(max_length=300)

    def __str__(self):
        return f'{self.type_name.__str__()}: {self.text}'

class Grant(models.Model):
    grant_name = models.ForeignKey(Type, on_delete=models.CASCADE, related_name="grants")
    time = models.DateField()
    label = models.CharField(max_length=100, null=True)
    text = models.TextField()
    link = models.CharField(max_length=300, null=True)
    org = models.CharField(max_length=300, null=True)
    days = models.CharField(max_length=30, null=True)
    rouble = models.CharField(max_length=30, null=True)
    fond = models.CharField(max_length=300, null=True)
    fond_link = models.CharField(max_length=300, null=True)

    def __str__(self):
        return f'{self.grant_name.__str__()}: {self.text}'


class Link(models.Model):

    link = models.CharField(max_length=300)
    grant_id = models.ForeignKey(Grant, on_delete=models.CASCADE, related_name="links")

    def __str__(self):
        return self.grant_id.__str__()
