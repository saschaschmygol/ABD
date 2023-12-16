from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('about/', views.about, name="about"),
    path('add_page/', views.addpage, name="add_page"),
    path('contact/', views.contact, name="contact"),
    path('login/', views.LoginUser.as_view(), name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('my_articles/', views.my_articles, name="my_articles"),
    path('post/<slug:post_slug>', views.post, name="post"),
    path('reviews/<int:post_id>', views.reviews, name="reviews"),
    path('cat/<slug:cat_slug>', views.cat, name="cat"),
    path('register/', views.RegisterUser.as_view(), name="register"),
    path('addcomment/<slug:post_slug>', views.addcomment, name="addcomment"),
]