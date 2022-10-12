from django.shortcuts import render, get_object_or_404, redirect
from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from.models import Patient,Slot,Customer,User,Appointment,Category,Feedback,Home,Info,Order,Payment,Result,Test


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
    test = Test.objects.all()
    context = {'catgry': catgry, 'test':test}
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
def slot_management(request):
    catgry = Category.objects.order_by('name')[:]
    context = {'catgry': catgry}
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
    cat = Test.objects.filter(category_id=cat_id)
    qs_json = serialize('json', cat)
    print(qs_json)
    return JsonResponse({"testresult": qs_json})

@login_required
def list_by_cat2(request):
    cat_id = request.GET['cat_id']
    cat = Slot.objects.filter(category_id=cat_id)
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

    if(len(tavail)==0):

        ts="Not available"
    else:
        ts="Available"

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
       test =Test.objects.get(id=tid)
       p1=0
       p2=0
       if test.status=="Available":
           p1=1
       if test.hstatus=="Available":
           p2=1
       print(p1)
       print(p2)
       print(test.status)
       print(test.hstatus)
       context = {'test': test,'f1':p1,'f2':p2}
       return render(request, 'labadmin/update test.html',context)



@login_required
def getupdatedtestdata(request):
    tname = request.POST['test']
    des = request.POST['testdes']
    price = request.POST['price']
    cat = request.POST['category']
    tavail = request.POST.getlist('available')
    havail = request.POST.getlist('home')

    print(tname,des,price,cat,tavail,havail)

    catgry = Category.objects.order_by('name')[:]
    context = {'catgry': catgry}
    return render(request,'labadmin/test manage.html',context)


@login_required
def updateslot(request):


    return render(request, 'labadmin/update slot.html')


@login_required
def getupdatedslotdata(request):
    #slot_interval = request.POST['slot_interval']
    #strength = request.POST['strength']
    #status = request.POST.getlist('slot_status')


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

#
@login_required
def deleteslot(request, sid):
    print(sid)


    return redirect('slot_management')








