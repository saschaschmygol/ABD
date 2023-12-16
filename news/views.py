from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .utils import *
from newsapi import NewsApiClient
from time import sleep
from googletrans import Translator

from .forms import AddPostForm, RegisterUserForm, LoginUserForm, AddComment
from .models import News, Category

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Старт", 'url_name': 'contact'},
        {'title': "Мои статьи", 'url_name': 'my_articles'},]

def index(request):
    posts = News.objects.filter(is_published=True)
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': posts,
        'cat_selected': 0
    }
    return render(request, 'news/index.html', context=data)

# def base(request):
#     data = {
#         "menu": menu,
#     }
#     return render(request, 'news/base.html', context= data)

def my_articles(request):
    prof = Profiles.objects.get(user=request.user.id)
    posts = News.objects.filter(profiles=prof.id)

    data = {
        'title': f'Мои новости',
        'menu': menu,
        'posts': posts,
    }
    return render(request, 'news/index.html', context=data)

def about(request):
   return HttpResponse('о сайте')

def add_page(request):
    return HttpResponse('Добавить статью')

def contact(request):
    q = ['ai', 'computer', 'microsoft', 'apple', 'it', 'samsung', 'huawei', 'artificial', 'people', 'mause', 'keyboard',
         'monitor', 'ai', 'ai', 'ai', 'ai', 'ai']
    newsapi = NewsApiClient(api_key='897663bb45274ed6bab7579bc4b81679')

    for i in q:
        categor = Category.objects.get(slug=i)
        #print(cat.slug)
        maxResult = 100
        page = 0
        totalResult = 0

        while (maxResult * page <= totalResult):
            print(i)
            try:
                page += 1
                all_articles = newsapi.get_everything(q=str(i),
                                                      from_param='2023-11-08',
                                                      to='2023-12-08',
                                                      language='en',
                                                      page=page)
                if all_articles["status"] != "ok":
                    break

                articles = all_articles['articles']
                totalResult = all_articles["totalResults"]
                # print(totalResult)

                for i in articles:
                    title = i['title']
                    content = i['content']
                    new = News(title=title, content=content, cat=categor)
                    new.save()

            except Exception as z:
                # print(str(z))
                break
    return redirect('home')

def login(request):
    return HttpResponse('Статьи')
def register(request):
    return HttpResponse('red')


def reviews(request, post_id):
    return HttpResponse(f"Отзывы на пост с id={post_id}")

def cat(request, cat_slug):
    cats = Category.objects.filter(slug=cat_slug)
    posts = News.objects.filter(cat__slug=cat_slug)

    data = {
        'title': f'Новости категории',
        'menu': menu,
        'posts': posts,
    }
    return render(request, 'news/index.html', context=data)
def addpage(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            us_id = request.user.id
            sl = request.POST.get("slug")
            nws = News.objects.filter(slug=sl)
            nws.update(profiles_id=us_id)
            return redirect('home')

    else:
        form = AddPostForm()

    return render(request, 'news/addpage.html', {'form': form, 'menu': menu, 'title': 'Добавление статьи'})

def addcomment(request, post_slug):
    if request.method == 'POST':
        form = AddComment(request.POST)
        if form.is_valid():
            new = News.objects.get(slug=post_slug)
            prof = Profiles.objects.get(user=request.user.id)
            posts = form.save(commit=False)
            # posts.news = new.id
            posts.user = prof
            posts.news = new
            posts.save()
            # id = request.POST.get("id")

            # form.fields['user'].choices = prof.id
            # form.fields['news'].choices = new.id

            # com = Comment.objects.get(id=id)
            # com = Comment.objects.get(news__slug=post_slug)
            # com.update(news=new.id)
            # com.update(user=prof.id)
            return redirect(reverse('post', kwargs={'post_slug': post_slug}))
    else:
        form = AddComment()
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'cat_selected': 0,
        'form': form,
        'post_slug': post_slug,
    }
    return render(request, 'news/addcomment.html', context=data)


def post(request, post_slug):
    posts = News.objects.get(slug=post_slug)
    comment = Comment.objects.filter(news__id=posts.id)

    data = {
        'title': f'Пост {post_slug}',
        'menu': menu,
        'posts': posts,
        'comment': comment,
    }
    return render(request, 'news/post.html', context=data)

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'news/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'news/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('home')


