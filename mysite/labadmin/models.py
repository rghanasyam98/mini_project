from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
#from current_user import get_current_user

class User(AbstractUser):
    user_type = models.CharField(max_length=20)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    address = models.CharField(max_length=60)
    gender = models.CharField(max_length=6)
    phone = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Test(models.Model):
    name = models.CharField(max_length=30)
    price = models.IntegerField()
    des = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    status = models.CharField(max_length=15)
    hstatus = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return '%s %s' %(self.category, self.name)


# class Slot(models.Model):
#     time = models.CharField(max_length=10)
#     status = models.CharField(max_length=15)
#     strength = models.PositiveIntegerField(default=0)
#     astrength = models.PositiveIntegerField(default=0)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return '%s %s' %(self.category, self.time)

class Slot(models.Model):
    start = models.PositiveIntegerField(default=0)
    end = models.PositiveIntegerField(default=0)
    t1 = models.CharField(max_length=5,default='AM')
    t2 = models.CharField(max_length=5,default='AM')
    # status = models.CharField(max_length=15)
    strength = models.PositiveIntegerField(default=0)
    # astrength = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s %s' %(self.category, self.category)






class Patient(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    pname = models.CharField(max_length=25)
    age = models.PositiveIntegerField(default=0)
    gender = models.CharField(max_length=6)
    phone = models.BigIntegerField()

    place = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.pname


# class Appointment(models.Model):
#      patient=models.ForeignKey(Patient, on_delete=models.CASCADE)
#      bdate = models.DateField()
#      mode = models.CharField(max_length=15)
#      token = models.PositiveIntegerField(default=0)
#      status = models.CharField(max_length=20)
#      testpres = models.FileField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#      def __str__(self):
#         return self.patient

class Daytbl(models.Model):
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Working_days(models.Model):
    dayonly = models.ForeignKey(Daytbl, on_delete=models.CASCADE)
    start = models.PositiveIntegerField()
    end = models.PositiveIntegerField()
    t1 = models.CharField(max_length=5)
    t2 = models.CharField(max_length=5)
    strength = models.PositiveIntegerField()
    astrength = models.PositiveIntegerField()
    status = models.CharField(max_length=15)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='categories')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # def __str__(self):
    #     return self.start

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    bookslot=models.ForeignKey(Working_days,on_delete=models.CASCADE)
    bdate = models.ForeignKey(Daytbl, on_delete=models.CASCADE)
    mode = models.CharField(max_length=15)
    token = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20)
    compstatus=models.CharField(max_length=20,default='begin')
    # testpres = models.FileField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.patient


class Order(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    tests = models.ForeignKey(Test,  on_delete=models.CASCADE)
    # slot=models.ForeignKey(Slot, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s %s' %(self.appointment, self.tests)

# class Feedback(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     message = models.CharField(max_length=60)
#     reply = models.CharField(max_length=60)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.customer

class Feedback(models.Model):
    name=models.CharField(max_length=25,default='shyam')
    email=models.EmailField(max_length=254,default='rghanasyam9@gmail.com')
    subject = models.CharField(max_length=25,default='general')
    message = models.CharField(max_length=100)
    reply = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.customer


class Home(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    lat = models.DecimalField(max_digits=22,decimal_places=16)
    lon = models.DecimalField(max_digits=22, decimal_places=16)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.appointment

class Info(models.Model):
    title = models.CharField(max_length=20)
    content = models.CharField(max_length=60)
    image = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Payment(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    amount = models.FloatField(default=0.0)
    transaction = models.CharField(max_length=200)
    status = models.CharField(max_length=45, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.appointment


class Result(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    file = models.FileField()
    status = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.appointment








