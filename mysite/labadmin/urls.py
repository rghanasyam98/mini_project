from django.urls import path

from . import views

urlpatterns = [
     path('', views.index, name='index'),
     path('lablogout', views.lab_logout, name='lab_logout'),
     path('labhome', views.labhome, name='labhome'),
     path('test', views.test_management, name='test_management'),
     path('signin', views.signin, name='signin'),
     path('signup', views.signup, name='signup'),
     path('slot_management', views.slot_management, name='slot_management'),
     path('cat', views.cat_management, name='cat_management'),
     path('slot', views.addslot, name='slot'),
     path('login_user', views.login_user, name='login_user'),
     path('register', views.register, name='register'),
     path('getregisterdata', views.getregisterdata, name='getregisterdata'),
     path('addcat', views.addcat, name='addcat'),
     path('addtest', views.addtest, name='addtest'),
     path('gettestdata', views.gettestdata, name='gettestdata'),
     #path('updatetest', views.updatetest, name='updatetest'),
     path('getupdatedtestdata', views.getupdatedtestdata, name='getupdatedtestdata'),
     path('updateslot/<int:sid>/', views.updateslot, name='updateslot'),
     path('getupdatedslotdata', views.getupdatedslotdata, name='getupdatedslotdata'),
     path('addslotdata', views.addslotdata, name='addslotdata'),
     path('deleteslot/<int:sid>/', views.deleteslot, name='deleteslot'),
     path('listcat', views.list_by_cat, name='listcat'),
     path('listcat2', views.list_by_cat2, name='listcat2'),
     path('deletecat/<int:catid>/', views.deletecat, name='deletecat'),
     path('deletetest/<int:tid>/', views.deletetest, name='deletetest'),
     path('updatetest/<int:tid>/', views.updatetest, name='updatetest'),


]