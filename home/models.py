from django.db import models

# Create your models here.


class savings(models.Model):
    username = models.CharField('username', max_length=30)
    money_to_be_saved = models.CharField(
        'MoneytobeSaved', max_length=10, null=False)
    deadline = models.CharField('deadline', max_length=30, null=False)
    paid_sum = models.CharField('paid_sum',max_length=9,null=False,default='000000000')
    remaining_days = models.CharField('remaining_days',max_length=30,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class user_register(models.Model):
    username = models.CharField('username', max_length=30,null=True)
    firstname = models.CharField('firstname', max_length=20,null=True)
    lastname = models.CharField('lastname', max_length=20,null=True)
    email = models.CharField('email', max_length=40,null=True)
    password = models.CharField('password', max_length=20, null=True)
    contact = models.CharField('Contact', max_length=15,null=True)

class transactions(models.Model):
    username = models.CharField('username', max_length=30, null = True)
    amountpaid = models.CharField("amountpaid", max_length=10, null = True)
    timestamp = models.DateTimeField(auto_now_add=True)

class payment_details(models.Model):
    username = models.CharField('username', max_length=30, null=True)
    cardnumber = models.CharField('cardnumber', max_length=16, null=True)
    nameoncard = models.CharField('nameoncard', max_length=30, null=True)
    expirymonth = models.CharField('expirymonth', max_length=5, null=True)
    expiryyear = models.CharField('expiryyear', max_length=5, null=True)
    cvv = models.CharField('cvv', max_length=5, null=True)