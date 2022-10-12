from django.shortcuts import render, get_object_or_404, redirect
from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib import messages
import datetime
from.models import Patient,Slot,Customer,User,Appointment,Category,Feedback,Home,Info,Order,Payment,Result,Test,Day,Dayonly


User = get_user_model()

# Create your views here.

def index(request):
   return render(request, 'index.html')

@login_required
def labhome(request):
   return render(request, 'index2.html')

def signin(request):
   return render(request, 'login.html')

def signup(request):
   return render(request, 'register.html')

# def index(request):
#     return render(request, 'login.html')

@login_required
def test_management(request):
    catgry = Category.objects.order_by('name')[:]
    # test = Test.objects.all()

    caty = Category.objects.all().first()
    # print(cat.id)
    # print(cat.name)
    test = Test.objects.filter(category_id=caty.id)
    context = {'catgry': catgry, 'test':test,'caty':caty}
    return render(request, 'labadmin/test manage.html',context)


def lab_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return render(request, 'index.html')


@login_required
def deletetest(request,tid):
    entry = Test.objects.get(id=tid)
    print(entry)
    entry.delete()

    return redirect('test_management')

@login_required
def date_management(request):
    dd=Day.objects.all().values()
    # dd=Day.objects.select_related('category')
    current_date = datetime.date.today()
    # print(current_date)
    # d=Day.objects.all(date_gte = current_date).distinct()
    d = Day.objects.all().distinct()
    # context={'dd':dd,'disday':d}


    return render(request,'labadmin/datemanage.html',)

@login_required
def listbydate(request):
    did = request.GET['ddate']
    # print(cat_id)
    cat = Day.objects.filter(id=did)
    qs_json = serialize('json', cat)
    print(qs_json)
    return JsonResponse({"testresult": qs_json})

@login_required
def deletedayslot(request, dsid):
    entry = Day.objects.get(id=dsid)
    print(entry)
    entry.delete()


    return redirect('date_management')



@login_required
def add_date(request):
    d=request.POST['tdate']
    # print(d)
    slt=Slot.objects.all().values()
    # print(slt)
    d_date = Dayonly()
    d_date.date = d
    d_date.save()
    # entry = Dayonly.objects.get()
    # did=Dayonly.objects.latest('id')
    LastInsertId = int((Dayonly.objects.last()).id)
    print(LastInsertId)

    for s in slt:
        dd=Day()
        dd.date=d
        dd.start=s.get('start')
        dd.end=s.get('end')
        dd.t1=s.get('t1')
        dd.t2=s.get('t2')
        dd.strength=s.get('strength')
        dd.astrength=s.get('strength')
        dd.status = "Available"
        dd.category_id=s.get('category_id')
        # dd.did=LastInsertId

        dd.save()

    return redirect('date_management')



@login_required
def slot_management(request):
    catgry = Category.objects.order_by('name')[:]
    caty = Category.objects.all().first()
    # print(cat.id)
    # print(cat.name)
    slt = Slot.objects.filter(category_id=caty.id)

    context = {'catgry': catgry,'slt':slt,'caty':caty}
    return render(request, 'labadmin/slot manage.html', context)

@login_required
def cat_management(request):
    #catgry = Category.objects.all().values()
   # context = {
    #    'catgry ': catgry,
    #}
    #catgry = get_object_or_404(Category)
    #context = {' catgry':  catgry}
    catgry = Category.objects.order_by('name')[:]
    context = {'catgry': catgry}
    return render(request, 'labadmin/category.html', context)

   # return render(request, 'category.html')

@login_required
def list_by_cat(request):
    cat_id = request.GET['cat_id']
    print(cat_id)
    cat = Test.objects.filter(category_id=cat_id)
    qs_json = serialize('json', cat)
    print(qs_json)
    return JsonResponse({"testresult": qs_json})

@login_required
def list_by_cat2(request):
    cat_id = request.GET['cat_id']
    cat = Slot.objects.filter(category_id=cat_id)
    print(cat)
    qs_json = serialize('json', cat)
    print(qs_json)
    return JsonResponse({"slotresult": qs_json})

@login_required
def register(request):


    return render(request, 'register.html')

def getregisterdata (request):
    name = request.POST['name']
    addr = request.POST['addr']
    gen = request.POST['gender']
    phone = request.POST['mob']
    email = request.POST['email']
    passwd = request.POST['pwd']
    print(name,addr,gen,phone,email,passwd)
    p=make_password(passwd)
    u=User()
    u.email=email
    u.password=p
    u.username=email
    u.first_name=name
    u.last_name=name
    u.user_type="customer"
    u.save()
    uid = User.objects.filter(email=email).values('id')
    print(uid)
    # x = User.objects.filter(email=email)
    # print(x)
    # print(x['id'])
    z = None
    for i in uid:
        z = i.get('id')
    print(z)
    c=Customer()
    c.user_id=z
    c.name=name
    c.address=addr
    c.gender=gen
    c.phone=phone
    c.save()



    return redirect('register')



def login_user(request):
    email = request.POST['username']
    password = request.POST['password']

    username = User.objects.get(email=email).username
    user = authenticate(username=username, password=password)

   # print(uid)

    if user is not None:
        usertype = user.user_type

        if usertype == "labadmin":
            # return render(request, 'labadmin/admindash.html')
          login(request, user)
          return redirect('labhome')

        # elif usertype == 'resp':
        #     return render(request, '')
        elif usertype == 'customer':

            login(request, user)
            customer = Customer.objects.get(user=user)
            request.session['uid'] = customer.id
            request.session['uname'] = customer.name

            # return render(request, 'customer/user dash.html', context)
            return render(request, 'index3.html')
           #return render(request, 'mysite/customer/templates/user dash.html')
        else:
            return HttpResponse('Invalid user!')

    else:
        return HttpResponse('login error!')


@login_required
def addcat(request):
    if request.POST:

       cat = request.POST['category']
       print(cat)
       p = Category(name=cat)
       p.save()
    #catgry = Category.objects.all().values()
    #print(catgry)
    catgry = Category.objects.order_by('name')[:]
    context = {'catgry': catgry}
    return render(request, 'labadmin/category.html', context)


@login_required
def deletecat(request, catid):
    entry = Category.objects.get(id=catid)
    print(entry)
    entry.delete()


    return redirect('addcat')


@login_required
def addtest(request):

    #catgry = Category.objects.all().values()
    #print(catgry)
   # catgry = Category.objects.order_by('name')[:]
    #context = {'catgry': catgry}
    catgry = Category.objects.order_by('name')[:]
    context = {'catgry': catgry}


    return render(request, 'labadmin/addtest.html', context)

@login_required
def gettestdata(request):

    tname = request.POST['test']
    des = request.POST['testdes']
    price = request.POST['price']
    cat = request.POST['category']
    tavail = request.POST.getlist('available')
    havail = request.POST.getlist('home')
    print(cat)
    if (len(tavail) == 0):

        ts = "Not available"
    else:
        ts = "Available"

    if (len(havail) == 0):

        hs = "Not available"
    else:
        hs = "Available"



    c = Test()
    c.name = tname
    c.price=price
    c.des=des
    c.status=ts
    c.hstatus=hs
    c.category_id=cat
    c.save()
    return redirect('test_management')





@login_required
def updatetest(request, tid):
   # catgry = Category.objects.order_by('name')[:]
   # context = {'catgry': catgry}
       request.session['testid'] = tid
       test =Test.objects.get(id=tid)
       p1=0
       p2=0
       if test.status=="Available":
           p1=1
       if test.hstatus=="Available":
           p2=1
       print(test.category_id)
       catgry = Category.objects.all().values()
       print(p1)
       print(p2)
       print(test.status)
       print(test.hstatus)
       context = {'test': test,'f1':p1,'f2':p2,'catgry':catgry}
       return render(request, 'labadmin/update test.html',context)



@login_required
def getupdatedtestdata(request):
    tid = request.session['testid']
    c = Test.objects.get(id=tid)
    tname = request.POST['test']
    des = request.POST['testdes']
    price = request.POST['price']
    cat = request.POST['category']
    tavail = request.POST.getlist('available')
    havail = request.POST.getlist('home')
    print(cat)
    if (len(tavail) == 0):

        ts = "Not available"
    else:
        ts = "Available"

    if (len(havail) == 0):

        hs = "Not available"
    else:
        hs = "Available"

    c.name = tname
    c.price = price
    c.des = des
    c.status =ts
    c.hstatus = hs
    c.category_id = cat
    c.save()
    # print(tname,des,price,cat,tavail,havail)

    # catgry = Category.objects.order_by('name')[:]
    # context = {'catgry': catgry}
    # return render(request,'labadmin/test manage.html',context)
    return redirect('test_management')


# @login_required
# def updateslot(request):
#
#
#     return render(request, 'labadmin/update slot.html')


@login_required
def getupdatedslotdata(request):
    #slot_interval = request.POST['slot_interval']
    #strength = request.POST['strength']
    #status = request.POST.getlist('slot_status')

    start = request.POST['start']
    t1 = request.POST['t1']
    end = request.POST['end']
    t2 = request.POST['t2']
    strength = request.POST['strength']
    # status = request.POST.getlist('slot_status')
    cat = request.POST['category']


    return render(request, 'labadmin/slot manage.html')


@login_required
def addslot(request):
    catgry = Category.objects.order_by('name')[:]
    context = {'catgry': catgry}
    return render(request, 'labadmin/add slot.html', context)

    #return render(request, 'labadmin/add slot.html')


@login_required
def addslotdata(request):
    start = request.POST['start']
    t1=request.POST['t1']
    end = request.POST['end']
    t2=request.POST['t2']
    strength = request.POST['strength']
    # status = request.POST.getlist('slot_status')
    cat = request.POST['category']
    # if (len(status) == 0):
    #
    #     ts = "false"
    # else:
    #     ts = "true"
    # #print(cat,slot_interval,strength,ts)
    s = Slot()
    s.category_id = cat
    s.start=start
    s.end=end
    s.t1=t1
    s.t2=t2
    # s.status = ts
    s.strength = strength
    # s.astrength = strength
    s.save()

    return redirect('slot_management')
    #return render(request, 'labadmin/slot manage.html')


@login_required
def deleteslot(request, sid):
    print(sid)
    entry = Slot.objects.get(id=sid)
    print(entry)
    entry.delete()
    return redirect('slot_management')

@login_required
def updateslot(request, sid):
    request.session['sltid'] = sid
    #slt = Slot.objects.get(id=sid)
    slt = Slot.objects.get(id=sid)
    print(slt.category_id)
    catgry = Category.objects.order_by('name')[:]
    print(slt)
    p1=0
    p2=0

    if slt.t1=="AM":
        p1=1
    if slt.t2 == "AM":
        p2 = 1
    print(slt.t1)
    print(p1)
    print(slt.t2)
    print(p2)
    context = {'slt': slt,'catgry':catgry,'p1':p1,'p2':p2}


    return render(request,'labadmin/update slot.html', context)


@login_required
def getupdatedslotdata(request):
    #slot_interval = request.POST['slot_interval']
    #strength = request.POST['strength']
    #status = request.POST.getlist('slot_status')
    sid=request.session['sltid']
    print(sid)
    slt=Slot.objects.get(id=sid)
    start = request.POST['start']
    t1 = request.POST['t1']
    end = request.POST['end']
    t2 = request.POST['t2']
    strength = request.POST['strength']
    # status = request.POST.getlist('slot_status')
    # cat = request.POST['category']
    slt.start=start
    slt.end=end
    slt.t1=t1
    slt.t2=t2
    slt.strength=strength
    slt.save()
    return redirect('slot_management')

@login_required
def listbydate(request):
    did = request.GET['ddate']
    # print(cat_id)
    cat = Day.objects.filter(id=did)
    qs_json = serialize('json', cat)
    print(qs_json)
    return JsonResponse({"testresult": qs_json})










