


from django.shortcuts import render, get_object_or_404, redirect
from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from django.apps import apps
Category = apps.get_model('labadmin', 'Category')
Test = apps.get_model('labadmin', 'Test')
User = apps.get_model('labadmin', 'User')
Patient=apps.get_model('labadmin', 'Patient')
Slot=apps.get_model('labadmin', 'Slot')



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

@login_required
def viewmember(request):
    uid = request.session['uid']
    member = Patient.objects.filter(customer_id=uid)
    context = {'member' : member }
    #print(uid)
    return render(request,'customer/viewmember.html', context)

@login_required
def addmember(request):
    uid = request.session['uid']
    print(uid)

    return render(request,'customer/patient.html')

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

    return redirect('viewmember', uid)

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
    uid = request.session['userid']
    member = Patient.objects.filter(customer_id=uid)
    context = {'member': member}


    return render(request,'customer/book1.html', context)

@login_required
def book2(request):
    #request.session['userid'] = uid
    pid = request.POST['patient2']
    print(pid)
    request.session['pid'] = pid
    catgry = Category.objects.order_by('name')[:]
    test = Test.objects.filter(status='true')
    context = {'catgry': catgry, 'test': test}
    #member = Patient.objects.filter(customer_id=uid)
    #context = {'member': member}


    return render(request,'customer/book2.html', context )


def select(request, tid):
    print(tid)
    request.session['tid'] = tid
    t = Test.objects.filter(id=tid).values('category_id')
    c=None
    for x in t:

        c=x.get('category_id')
    print(c)
    s = Slot.objects.filter(category_id=c) & Slot.objects.filter(status='true')
    print(s)
    context = {'s': s}

    return render(request,'customer/book3.html',context)

def book3(request):
    slt = request.POST['slot']
    print(slt)
    request.session['sltid'] = slt


    return render(request,'customer/booking4.html')

