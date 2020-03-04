from django.db import models

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
    name = models.CharField(max_length=700)
    full_name = models.CharField(max_length=250)
    legal_address = models.CharField(max_length=250)
    purchase_code_name = models.CharField(max_length=250)
    place = models.CharField(max_length=500, null=True)
    currency = models.CharField(max_length=50)
    initial_sum = models.CharField(max_length=50, null=True)
    submission_start_date = models.CharField(max_length=50, null=True)
    submission_close_date = models.CharField(max_length=50, null=True)

    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.fz223_name.__str__()}: {self.name}'

class Fz44(models.Model):

    fz44_name = models.ForeignKey(Type, on_delete=models.CASCADE, related_name="fz44")
    fz44id = models.CharField(max_length=100)
    create_date = models.DateField()
    link = models.TextField()
    purchase_number = models.CharField(max_length=350)
    purchase_object = models.CharField(max_length=900)
    org_name = models.CharField(max_length=350)
    placing_way = models.CharField(max_length=400, null=True)
    start_date = models.CharField(max_length=350, null=True)
    end_date = models.CharField(max_length=350, null=True)
    place = models.TextField(null=True)
    max_price = models.CharField(max_length=350, null=True)
    currency = models.CharField(max_length=350, null=True)
    finance_source = models.CharField(max_length=300, null=True)
    aplication_guarantee = models.CharField(max_length=350, null=True)
    contract_guarantee = models.CharField(max_length=350, null=True)
    delivery = models.CharField(max_length=350, null=True)
    delivery_place = models.CharField(max_length=2000, null=True)

    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.fz44_name.__str__()}: {self.purchase_object}'

class Fcp(models.Model):

    fcp_name = models.ForeignKey(Type, on_delete=models.CASCADE, related_name="fcp")
    time = models.DateField()
    card_name = models.CharField(max_length=350, null=True)
    title = models.CharField(max_length=350, null=True)
    lead = models.TextField(null=True)
    link = models.CharField(max_length=350, null=True)

    def __str__(self):
        return f'{self.fcp_name.__str__()}: {self.title}'

class DigitalEconomy(models.Model):
    
    digitaleconomy_name = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='digital_economy')
    document_number = models.CharField(max_length=100, null=True)
    date = models.DateField(null=True)
    text = models.TextField()
    link = models.CharField(max_length=300)

    def __str__(self):
        return f'{self.digitaleconomy_name.__str__()}: {self.text}'

class Grant(models.Model):
    grant_name = models.ForeignKey(Type, on_delete=models.CASCADE, related_name="grant")
    time = models.DateField()
    label = models.CharField(max_length=300, null=True)
    text = models.TextField()
    link = models.CharField(max_length=300, null=True)
    org = models.CharField(max_length=300, null=True)
    days = models.CharField(max_length=30, null=True)
    rouble = models.CharField(max_length=30, null=True)
    fond = models.CharField(max_length=300, null=True)
    fond_link = models.CharField(max_length=300, null=True)

    def __str__(self):
        return f'{self.grant_name.__str__()}: {self.text}'
    
    @staticmethod 
    def clean_correct_days_4science(grant):

        if grant.days:
            day = int(grant.days.split()[0])

            if day - 1 < 0:
                grant.delete()
            else:
                grant.days = day - 1
                grant.save()

class Link(models.Model):

    link = models.CharField(max_length=250)
    grant_id = models.ForeignKey(Grant, on_delete=models.CASCADE, related_name="links")

    def __str__(self):
        return self.grant_id.__str__()
