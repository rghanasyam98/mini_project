
from django.shortcuts import render, get_object_or_404, redirect
from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
import json
import datetime
from django.conf import settings
import razorpay
from django.views.decorators.csrf import csrf_exempt

from django.apps import apps
Category = apps.get_model('labadmin', 'Category')
Test = apps.get_model('labadmin', 'Test')
User = apps.get_model('labadmin', 'User')
Patient=apps.get_model('labadmin', 'Patient')
Slot=apps.get_model('labadmin', 'Slot')
Customer=apps.get_model('labadmin', 'Customer')
Daytbl=apps.get_model('labadmin', 'Daytbl')
Working_days=apps.get_model('labadmin', 'Working_days')
Appointment=apps.get_model('labadmin', 'Appointment')
Order=apps.get_model('labadmin', 'Order')



# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

# Create your views here.
#
# from labadmin.models import Patient,Slot,Customer,User,Appointment,Category,Feedback,Home,Info,Order,Payment,Result,Test

def index(request):
    print("hai")
    return render(request, 'index3.html')



@login_required
def testview(request):
    catgry = Category.objects.order_by('name')[:]

    caty = Category.objects.all().first()
    test = Test.objects.filter(category_id=caty.id)
    # test = Test.objects.all()
    context = {'catgry': catgry, 'test': test,'caty':caty}

    return render(request,'customer/user view tests.html',context)

# @login_required
def viewmember(request):
    uid = request.session['uid']
    print(uid)
    member = Patient.objects.filter(customer_id=uid)
    context = {'member' : member }
    #print(uid)
    return render(request,'customer/viewmember.html', context)

@login_required
def addmember(request):
    uid = request.session['uid']
    print("hai")
    print(uid)

    return render(request,'customer/patient.html')

# @login_required
def editprofile(request):
    uid = request.session['uid']
    # print(uid)
    usr = Customer.objects.get(id=uid)
    print(usr.id)
    print(usr.user_id)
    p1 = 0

    if usr.gender == "male":
        p1 = 1

    useremail=User.objects.get(id=usr.user_id)


    context={'usr':usr,'useremail':useremail,'p1':p1}


    return render(request,'customer/update profile.html',context)


@login_required
def getupdatedprofile(request):
    uid = request.session['uid']
    # print(uid.id)
    name = request.POST['name']
    addr = request.POST['addr']
    gen = request.POST['gender']
    phone = request.POST['mob']
    email = request.POST['email']
    passwd = request.POST['pwd']
    print(name, addr, gen, phone, email, passwd)
    usr = Customer.objects.get(id=uid)
    usr.name=name
    usr.address=addr
    usr.gender=gen
    usr.phone=phone
    usr.save()
    p = make_password(passwd)
    usr1=User.objects.get(id=usr.user_id)
    # print(usr1)
    usr1.password=p
    usr1.username=email
    usr1.first_name=name
    usr1.last_name = name
    usr1.email = email
    usr1.save()
    url = 'editprofile'
    resp_body = '<script>alert("Profile updated successfully...");\
                            window.location="%s"</script>' % url
    return HttpResponse(resp_body)




    # return render(request,'index3.html')



@login_required
def getmemberdata(request):
    name=request.POST['pname']
    age=request.POST['pAge']
    gen=request.POST['gender']
    place=request.POST['place']
    phone=request.POST['phone']
    #current_user = request.user
    #print(current_user.id)
    uid = request.session['uid']
    print(uid)

    print(uid,name,age,gen,place,phone)
    p=Patient()
    p.pname=name
    p.age=age
    p.gender=gen
    p.phone=phone
    p.place=place
    p.customer_id=uid
    p.save()

    url = 'viewmember'
    resp_body = '<script>alert("Member added successfully...");\
                                window.location="%s"</script>' % url
    return HttpResponse(resp_body)

    # return redirect('viewmember')

def deletemember(request, pid):
    uid = request.session['uid']
    entry = Patient.objects.get(id=pid)
    #print(entry)
    entry.delete()
    return redirect('viewmember')




@login_required
def listcat3(request):
    cat_id = request.GET['cat_id']
    cat = Test.objects.filter(category_id=cat_id)
    qs_json = serialize('json', cat)
    print(qs_json)
    return JsonResponse({"testresult": qs_json})

   # return render(request, '/labadmin/templates/login.html')



@login_required
def book1(request):
    uid = request.session['uid']
    member = Patient.objects.filter(customer_id=uid)
    ddate = datetime.date.today()
    print(ddate)
    # bdays=Daytbl.objects.all()
    # today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    # print(today_min);
    # bdays = Daytbl.objects.get(date__range = (today_min))
    # bdays=Daytbl.objects.filter(date__startswith=datetime.date.today())
    bdays=Daytbl.objects.filter(date__gte=datetime.date.today())
    # bdays=Daytbl.objects.filter(date__range=[ddate])
    catgry = Category.objects.order_by('name')[:]
    context = {'member': member,'catgry':catgry,'bdays':bdays}


    return render(request,'customer/book1.html', context)

@login_required
def book2(request):
    #request.session['userid'] = uid
    pid = request.POST.get('patient2', False);
    # is_private = request.POST.get('is_private', False);
    # bookdateid = request.POST['bdate']
    cat = request.POST.get('cat',False);
    bday = request.POST.get('bdate', False);
    # print(pid)
    # print(cat)
    print(bday)
    # bdate=Daytbl.objects.get(id=bday)
    # print(bdate.date)
    request.session['pid'] = pid

    request.session['cat'] = cat
    request.session['bday'] = bday
    catgry = Category.objects.order_by('name')[:]
    # arr = [pid,cat,bday]
    # arr = json.dumps(arr)
    # apmt=Appointment()
    # apmt.patient_id=pid
    # apmt.bdate_id=bday
    # apmt.mode="lab"
    # apmt.token=0
    # apmt.status="pending"
    # apmt.compstatus="pending"
    # apmt.bookslot_id=0
    # apmt.save()
    # appid = (Appointment.objects.last()).id
    # request.session['appid'] = appid


    test = Test.objects.filter(status='Available') & Test.objects.filter(category_id=cat)
    print(test)
    context = { 'test': test}
    #member = Patient.objects.filter(customer_id=uid)
    #context = {'member': member}


    return render(request,'customer/book2.html', context )

def gotoslotpage(request):
    cat=request.session['cat']
    bday=request.session['bday']
    # appid = request.session['appid']

    some_var = request.POST.getlist('type1')
    request.session['orders'] = some_var
    # some_var = json.dumps(some_var)
    # arr = json.loads(arr)

    # print('iiiii');
    #
    # ordr=Order()
    # for x in some_var:
    #     ordr.

    slt = Working_days.objects.filter(dayonly=bday) & Working_days.objects.filter(category=cat)
    context = {'slt': slt}
    return render(request, 'customer/book3.html', context)
    # print(some_var);
    # if  len(some_var)==0:
    #     print("empty")
    #     url = 'book1'
    #     resp_body = '<script>alert("Must choose any test to proceed..");\
    #                                    window.location="%s"</script>' % url
    #     return HttpResponse(resp_body)




def bookingsummary(request, bksid):
    print(bksid)
    orders= request.session['orders']
    cat = request.session['cat']
    bday = request.session['bday']
    pid= request.session['pid']
    # some_var = json.loads(some_var)
    print("hai")
    print(orders)
    bkslot = Working_days.objects.get(id=bksid)
    # print("token:",(bkslot.strength - bkslot.astrength) + 1)
    apmt=Appointment()
    apmt.patient_id=pid
    apmt.bdate_id=bday
    apmt.mode="lab"
    apmt.token=0
    apmt.status="pending"
    apmt.compstatus="pending"
    apmt.bookslot_id=bksid
    apmt.save()
    appid = (Appointment.objects.last()).id

    for x in orders:
        ordr = Order()
        ordr.appointment_id=appid
        ordr.tests_id=x
        ordr.save()
    pat = Patient.objects.get(id=pid)
    print(pat.pname)
    bkdate=Daytbl.objects.get(id=bday)
    appo=Appointment.objects.get(id=appid)
    listoftests=Order.objects.filter(appointment_id= appid)
    testdata=Test.objects.all()
    sum=0
    print(testdata)

    for k in listoftests:
        # print(k.tests_id)
        var=Test.objects.get(id=k.tests_id)
        sum=sum+(var.price)
    print(sum)
    # for i in testdata:
    #     for j in listoftests:
    #         if j.tests_id == i.id:
    #             sum=sum+x.price
    #
    context={'listoftests':listoftests,'testdata':testdata,'pat':pat,'bkdate':bkdate,'bkslot':bkslot,'appo':appo,'sum':sum}


    return render(request, 'customer/booking4.html',context)

def bookingcompleted(request):

    return render(request,'index3.html')


def select(request, tid):
    print(tid)

    # request.session['tid'] = tid
    # t = Test.objects.filter(id=tid).values('category_id')
    # c=None
    # for x in t:
    #
    #     c=x.get('category_id')
    # print(c)
    # # s = Slot.objects.filter(category_id=c)
    # print(s)
    # context = {'s': s}
    cat = request.session['cat']
    test = Test.objects.filter(status='Available') & Test.objects.filter(category_id=cat)
    context = {'test': test}

    # return redirect('book2')
    return render(request, 'customer/book2.html', context)
    # return render(request,'customer/book3.html',context)

def backtotestapge(request):

    cat=request.session['cat']
    test = Test.objects.filter(status='Available') & Test.objects.filter(category_id=cat)
    context = {'test': test}

    return render(request,'customer/book2.html', context )

def book3(request):
    slt = request.POST['slot']
    print(slt)
    request.session['sltid'] = slt


    return render(request,'customer/booking4.html')



#payment portion
def home(request):
    currency = 'INR'
    amount = 20000  # Rs. 200

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))

    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler'

    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url

    return render(request, 'payment.html', context=context)


# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):
    # only accept POST request.
    print('fff');
    if request.method == "POST":
        try:

            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            print(payment_id)
            if result is not None:
                amount = 20000  # Rs. 200
                try:

                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)

                    # render success page on successful caputre of payment

                    return HttpResponse('success')
                except:

                    # if there is an error while capturing payment.
                    resp_body = '<script>alert("payment failed...");\
                                                                     </script>'
                    return HttpResponse(resp_body)
            else:

                # if signature verification fails.
                resp_body = '<script>alert("payment failed...");\
                                                    </script>'
                return HttpResponse(resp_body)
        except:

            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
        # if other than POST request is made.
        return HttpResponseBadRequest()


























