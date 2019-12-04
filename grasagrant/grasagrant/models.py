from django.db import models

class Category(models.Model):

    tab_name = models.CharField(max_length=100)


class Type(models.Model):

    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="type")

class Fz223(models.Model):

    fz = models.ForeignKey(Type, on_delete=models.CASCADE, related_name="fz223")
    registration_number = models.CharField(max_length=100)
    create_date = models.DateTimeField()
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
    

class Fz44(models.Model):

    fz = models.ForeignKey(Type, on_delete=models.CASCADE, related_name="fz44")
    fz_id = models.CharField(max_length=100)
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
    time = models.DateTimeField()
    card_name = models.CharField(max_length=300)
    title = models.CharField(max_length=300)
    lead = models.TextField()
    link = models.CharField(max_length=300)

class Grants(models.Model):
    grant_name = models.ForeignKey(Type, on_delete=models.CASCADE, related_name="grants")
    time = models.DateTimeField()
    label = models.CharField(max_length=100)
    text = models.TextField()
    link = models.CharField(max_length=300)
    org = models.CharField(max_length=300)
    days = models.CharField(max_length=30)
    rouble = models.CharField(max_length=30)
    fond = models.CharField(max_length=300)
    fond_link = models.CharField(max_length=300)


class Links(models.Model):

    link = models.CharField(max_length=300)
    grant_id = model.ForeignKey(Grants, on_delete=models.CASCADE, related_name="links")
