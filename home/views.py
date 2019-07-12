from django.shortcuts import render, redirect,HttpResponse
from django.contrib import messages
# from datetime import datetime
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from home.models import user_register,savings,transactions,payment_details
import requests,random,time,datetime
uname = ""
amount_to_be_paid = ""
def home_view(request):
    return render(request, 'home.html')


def user_logout(request):
    logout(request)
    return redirect('/home/')


def register(request):
    global uname    
    if request.method == "POST":     
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        contact = request.POST.get('contact')
        uname = username
        check = None
        try:
            check = user_register.objects.get(username=username)
        except:
            check = None
        if check:
            messages.error(request,'Username already exists')
            return HttpResponseRedirect("/home/registers/")
        else:
            k = False
            user = user_register.objects.create(username=username,firstname=firstname,lastname=lastname,email=email,password=password,contact=contact)
            user.save()
            messages.success(request,'Your are registered successfully!!')
           # return redirect('/home/login1/You have successfully signed up')
            return redirect('/home/login1/')
    else:
        return render(request,'auth/signup.html',{'msg':''})


def thankyou(request):
    return render(request,'thankyou.html')


def user_login(request):
    global uname
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        uname = username
        user1=None
        try:
            user1 = user_register.objects.get(username=username,password=password)
        except:
            user1=None        
        if user1 :
            return redirect('/home/login2/')                   
        else:
            messages.error(request,"Invalid Login Details given")
            return render(request,'auth/loginuser.html')
    else:
        return render(request,'auth/loginuser.html',{})       


def login1(request):
    global uname 
    if request.method == "POST":        
        MoneytobeSaved =request.POST.get('money_to_be_saved')
        deadline = request.POST.get('deadline')
        uname= request.POST.get('username')
        
        #return redirect('/home/login2/')
        date_format = "%Y-%m-%d"
        date = str(datetime.datetime.now())
        date = date.split(' ')
        a = datetime.datetime.strptime(date[0], date_format)
        b = datetime.datetime.strptime(deadline, date_format)
        delta = b-a
        remaining_days=delta.days
        paid_sum=0
            # print(delta.days)
        if delta.days > 0:
            log = savings.objects.create(username=uname,money_to_be_saved=MoneytobeSaved,deadline=deadline,paid_sum=paid_sum,remaining_days=remaining_days)
            log.save()

                # return render(request, "auth/login1.html", {'value1': MoneytobeSaved, 'value2': deadline, 'choice': choice, 'key': 'True', 'name': uname})
            return redirect('/home/login2/')
        else:
            messages.error(request,"Invalid deadline")
            return HttpResponseRedirect('/home/login1/')
        #return redirect('/home/login2')

    else:
        # return HttpResponse("Invalid Login Details given")
        return render(request, 'auth/login1.html', {'name': uname,'msg':' '})
        # else:
        #     return render(request,'auth/login1.html')
        #return HttpResponse("Hello")
    # else:
    #      return HttpResponse("Invalid Login Details given")
    #     return render(request,'auth/login1.html',{'name':uname})
        # user = savings.objects.create(username=username,MoneytobeSaved=MoneytobeSaved,deadline=deadline)
        # user.save()
        

def payment(request):
    if request.method == "POST" :          
        global uname,amount_to_be_paid
        nameoncard = request.POST.get('nameoncard')
        cardnumber = request.POST.get('cardnumber')
        expirymonth = request.POST.get('expirymonth')
        expiryyear = request.POST.get('expiryyear')
        cvv = request.POST.get('cvv')
        date=str(datetime.datetime.now())
        k = date.split(' ')
        p = str(k[0])
        p=p.split('-')
        if (expiryyear == p[0] and expirymonth > p[1]) or (expiryyear > p[0]) :
            log = payment_details.objects.create(username=uname,cardnumber=cardnumber,nameoncard=nameoncard,expirymonth=expirymonth,expiryyear=expiryyear,cvv=cvv)
            log.save()
            # pay = payment.objects.create(Username=uname,nameoncard=nameoncard,cardnumber=cardnumber)
            # pay.save()
            return redirect('/home/otp/')
        else:
            messages.error(request,"Your card is expired")
            return HttpResponseRedirect('/home/payment/')
            # return HttpResponseRedirect('/home/payment/{'msg':'Your card is expired','obj':'.'}')
    else:
        users1 = None
        try:
            # print("try")
            users1 = payment_details.objects.filter(username=uname)
        except:
            # print("except")
            users1 = None
        if users1:
            # print(users1)
            # print(type(users1))
            value1=int(users1[0].cardnumber)
            value2=str(users1[0].nameoncard)
            # print(value1,value2)
            # print(users1[0].username)
            return render(request,'auth/payment.html',{'val1':value1,'val2':value2,'msg':'True'})
        else:
            print("else")
            return render(request,'auth/payment.html')
        # if objec['obj']=='.':
        #     return render(request,'auth/payment.html',{'msg':objec['msg']})
        # else:
        #      return render(request,'auth/payment.html',{'msg':objec['msg'],'value':objec['obj']})


def login2(request):
    global uname,amount_to_be_paid 
    # amount = request.POST.get('amount_to_be_paid')
    # uname = request.POST.get('username')
    # print(uname)
    # amount_to_be_paid = amount
    user1 = savings.objects.get(username=uname)
    if int(user1.remaining_days)<=0:
        return redirect('/home/remaining/')
    # print(user1)
    paid_sum = int(user1.paid_sum)
    money_to_be_saved = user1.money_to_be_saved
    money_to_be_saved = int(money_to_be_saved)
    value1 = int(user1.paid_sum)
    value2 = int(user1.remaining_days)
    value3 = int((money_to_be_saved-value1)/value2)

    if request.method == "POST":
        amount = int(request.POST.get('amount_to_be_paid'))
        uname= request.POST.get('username')
        amount_to_be_paid = amount
        # names = None
        # try:
        #     names = payment.objects.get(username=username)
        # except:
        #     names = None
        # if names :
        #     return redirect('/home/payment/{'msg':'.','obj':names}')  
        # else:
        #     return redirect('/home/payment/{'msg':'.','obj':'.'}')
        # log = transactions.objects.create(username=uname, amountpaid=amount_to_be_paid)
        # log.save()
        # return redirect('/home/payment/Card Details Please')
        print(money_to_be_saved)
        print(paid_sum)
        print(amount)
        if amount<=(money_to_be_saved-paid_sum):
            return redirect('/home/payment/')
        else:
            messages.success(request,"Please enter valid amount")
            return render(request, 'auth/login2.html', {'value1': value1, 'value2': value2, 'value3': value3,'name':uname})
    else:
        return render(request, 'auth/login2.html',{'value1': value1, 'value2': value2, 'value3': value3,'name':uname})


def remaining(request):
    global uname
    if request.method=="POST":
        extended=extended_deadline.POST.get('extended_deadline')
        date_format = "%Y-%m-%d"
        date = str(datetime.datetime.now())
        date = date.split(' ')
        a = datetime.datetime.strptime(date[0], date_format)
        b = datetime.datetime.strptime(extended_deadline, date_format)
        delta = b-a
        remaining_days=delta.days
        if remaining_days>0:
            savings.objects.filter(username=uname).update(remaining_days=remaining_days,deadline=extended)
            return redirect('/home/login2')
    else:
        return render(request,'remaining.html')        







def otp(request):
    global uname,amount_to_be_paid
    if request.method=="POST":
        # me = "Welcome to OTP portal"
        otp = request.POST.get('otp')
        with open("test.txt",'r') as f: 
            rn=f.readline()
            ts=f.readline()
        now=datetime.datetime.now()
        ki = str(now)
        ko = ki.split('.')
        date_time_obj1 = datetime.datetime.strptime(ko[0], '%Y-%m-%d %H:%M:%S')
        date_time_obj2 = datetime.datetime.strptime(ts, '%Y-%m-%d %H:%M:%S')
        print(date_time_obj1)
        rn=int(rn)
        sec = (date_time_obj1-date_time_obj2).total_seconds()
        otp=int(otp)
        print(rn,otp)
        print(type(rn),type(otp))
        # print(len(rn),len(otp))
        if (sec > 40) :
            messages.error(request,"OTP has been expired")
            return HttpResponseRedirect('/home/otp/')
        elif rn!=otp :
            messages.error(request,"Please enter valid OTP")
            return HttpResponseRedirect('/home/otp/')
        else:
            log = transactions.objects.create(username=uname, amountpaid=amount_to_be_paid)
            log.save()    
            user1 = savings.objects.get(username=uname)
            paid_sum = int(user1.paid_sum)+int(amount_to_be_paid)      
            deadline = user1.deadline
            date_format = "%Y-%m-%d"
            date = str(datetime.datetime.now())
            date = date.split(' ')
            a = datetime.datetime.strptime(date[0], date_format)
            b = datetime.datetime.strptime(deadline, date_format)
            delta = b-a
            remaining_days = delta.days
            savings.objects.filter(username=uname).update(
            paid_sum=paid_sum, remaining_days=remaining_days)
            use = savings.objects.get(username=uname)
            if int(use.money_to_be_saved)==int(use.paid_sum):
                money = (int((use.paid_sum))*12)/100
                savings.objects.filter(username=uname).delete()
                payment_details.objects.filter(username=uname).delete()
                transactions.objects.filter(username=uname).delete()
                user_register.objects.filter(username=uname).delete()
                messages.success(request,"You have reached the target and bonus of "+str(money)+" is awarded")
            return HttpResponseRedirect('/home/thankyou/')

    else:
        return render(request,'auth/otp.html',{'msg':' '})
 

def output(request):
    global uname
    user = user_register.objects.get(username=uname)
    print(uname)
    url = "https://www.fast2sms.com/dev/bulk"
    print(url)
    a = random.randint(100000,1000000)
    t = datetime.datetime.now()
    print(a)
    payload = "sender_id=FSTSMS&message=OTP for Daily-savings accont is "+str(a)+"&language=english&route=p&numbers="+str(user.contact)
    headers = {
    'authorization': "CYvJy9ick6V7p8oFtjmuZTMSQ0UdDz51bAI2BR4ewPl3nhXgrsGKBYurmTvqPc0aAeFENQogyI2sUCpW",
    'Content-Type': "application/x-www-form-urlencoded",
    'Cache-Control': "no-cache",
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)
    rn=str(a)
    ts=str(t)
    k = ts.split('.')
    # print(k[0])
    date_time_obj = datetime.datetime.strptime(k[0], '%Y-%m-%d %H:%M:%S')
    print(date_time_obj)
    # print(k[0])
    with open("test.txt",'w+') as f:  
        f.write(str(a)+'\n')
        f.write(str(k[0]))
    print("DONE")
    #message = "OTP has been sent to your registered mobile number"
    #return render(request, 'otp.html', {'msg':message})
    messages.success(request,"OTP has been sent to your registered mobile number")
    return HttpResponseRedirect('/home/otp/')


def dashboard(request):
    global uname
    user = transactions.objects.filter(username=uname)
    return render(request, 'dashboard.html', {'user': user})

def adminlogin(request):
    adminname = request.POST.get('adminname')
    password = request.POST.get('password')
    if request.method=="POST":
        adminname = request.POST.get('adminname')
        password = request.POST.get('password')
        print(adminname)
        print(password)
        if adminname=="admin" and password=="admin123":
            print(adminname)
            print(password)
            return redirect('/home/admins/')
        else:
            messages.error(request,"Invalid username or password")
            return render(request,'adminlogin.html')
    else:
        return render(request,'adminlogin.html')
        

def admins(request):
    user = savings.objects.all()
    return render(request,'admins.html',{'user':user})


def debit(request):
    global uname
    user=savings.objects.get(username=uname)
    if request.method=="POST":
        deb = request.POST.get('money')
        if (int(deb) > 0):
            if int(deb) == int(user.paid_sum):
                var = str(user.paid_sum)
                messages.success(request,var+" will be credited to your account within 24hours and your account will be deleted")
                savings.objects.filter(username=uname).delete()
                transactions.objects.filter(username=uname).delete()
                user_register.objects.filter(username=uname).delete()
                payment_details.objects.filter(username=uname).delete()
                return redirect('/home/')
            elif int(deb) < int(user.paid_sum) :
                k = int(user.paid_sum)-int(deb)
                messages.success(request,deb+" will be credited to your account within 24hours")
                savings.objects.filter(username=uname).update(paid_sum=str(k))
                sav = transactions.objects.create(username=uname, amountpaid=str(-int(deb)))
                sav.save()
                return redirect('/home/login2/')
            else:
                messages.error(request,'You dont have enough money')
                return redirect('/home/login2/')         
    else:
        return render(request,'debit.html')


def contactus(request):
    return render(request,'contactus.html')
