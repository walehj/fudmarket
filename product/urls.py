from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create', views.post_create, name='create'),

    path('detail/<slug:product_slug>', views.singleView, name='single_listview'),
    path('howitworks', views.howitworksView, name='howitworks'),
    path('base', views.base, name='base'),
    path('contact', views.Contact, name='contact'),
    path('help', views.help, name='help'),
    path('signin', views.user_login, name='signin'),
    path('signout', views.user_logout, name='signout'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('register', views.register, name='register'),
    path('privacy', views.privacy, name='privacy'),
    path('terms', views.terms, name='terms'),
    path('classified', views.classifiedView, name='classified'),
    path('<slug:category_slug>', views.classifiedView,
         name='product_list_category')

]
