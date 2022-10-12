


from django.shortcuts import render, get_object_or_404, redirect
from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password

from django.apps import apps
Category = apps.get_model('labadmin', 'Category')
Test = apps.get_model('labadmin', 'Test')
User = apps.get_model('labadmin', 'User')
Patient=apps.get_model('labadmin', 'Patient')
Slot=apps.get_model('labadmin', 'Slot')
Customer=apps.get_model('labadmin', 'Customer')



# Create your views here.
#
# from labadmin.models import Patient,Slot,Customer,User,Appointment,Category,Feedback,Home,Info,Order,Payment,Result,Test

def index(request):
    print("hai")
    return render(request, '/labadmin/templates/login.html')



@login_required
def testview(request):
    catgry = Category.objects.order_by('name')[:]
    test = Test.objects.all()
    context = {'catgry': catgry, 'test': test}

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




    return render(request,'index3.html')



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

    return redirect('viewmember')

def deletemember(request, pid):
    uid = request.session['uid']
    entry = Patient.objects.get(id=pid)
    #print(entry)
    entry.delete()
    return redirect('viewmember', uid)




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
    catgry = Category.objects.order_by('name')[:]
    context = {'member': member,'catgry':catgry}


    return render(request,'customer/book1.html', context)

@login_required
def book2(request):
    #request.session['userid'] = uid
    pid = request.POST.get('patient2', False);
    # is_private = request.POST.get('is_private', False);
    # bookdateid = request.POST['bdate']
    cat = request.POST.get('cat',False);
    # print(pid)
    # print(cat)

    request.session['pid'] = pid
    # request.session['bookdateid'] = bookdateid
    request.session['cat'] = cat
    # catgry = Category.objects.order_by('name')[:]

    test = Test.objects.filter(status='Available') & Test.objects.filter(category_id=cat)
    print(test)
    context = { 'test': test}
    #member = Patient.objects.filter(customer_id=uid)
    #context = {'member': member}


    return render(request,'customer/book2.html', context )


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

