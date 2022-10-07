from django.urls import path

from . import views

urlpatterns = [
     path('', views.index, name='index'),
     path('listcat3', views.listcat3, name='listcat3'),
     path('testview', views.testview, name='testview'),
     path('viewmember', views.viewmember, name='viewmember'),
     path('addmember', views.addmember, name='addmember'),
     path('getmemberdata', views.getmemberdata, name="getmemberdata"),
     path('deletemember/<int:pid>/', views.deletemember, name="deletemember"),
     path('book1', views.book1, name="book1"),
     path('book2', views.book2, name="book2"),
     path('select/<int:tid>/', views.select, name="select"),
     path('book3', views.book3, name="book3"),
     path('editprofile', views.editprofile, name="editprofile"),
     path('getupdatedprofile', views.getupdatedprofile, name="getupdatedprofile"),




]