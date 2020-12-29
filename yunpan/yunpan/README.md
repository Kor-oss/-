###一、创建主程序包
####1创建主文件  yunpan
django-admin startproject yunpan
在vscode输入python manage.py runserver 运行
测试正常
`py manage.py startapp polls`创建登录应用
在`settings.py`文件中添加`polls`应用
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'polls',
]
```


####2配置数据库
建立一个应用起名为news，在项目包的settings.py中加入news应用
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'polls',
    'news',
]
```
配置models数据模型
```python
from django.db import models

class Reporter(models.Model):
    full_name = models.CharField(max_length=70)

    def __str__(self):
        return self.full_name

class Article(models.Model):
    pub_date = models.DateField()
    headline = models.CharField(max_length=200)
    content = models.TextField()
    reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)

    def __str__(self):
        return self.headline
```        
数据库迁移
```python
    python manage.py makemigrations
    python manage.py migrate
```
配置`admin`页面
```python
from django.contrib import admin

from . import models

admin.site.register(models.Article)
```
创建超级用户
```
python manage.py createsuperuser
```
创建`Repoter`模型并在`news`文档中建立`urls.py`配置跟路由
```python
from django.urls import path

from . import views

urlpatterns = [
    path('articles/<int:year>/', views.year_archive),
    path('articles/<int:year>/<int:month>/', views.month_archive),
    path('articles/<int:year>/<int:month>/<int:pk>/', views.article_detail),
]
```
配置`news/views.py`中的view函数
```python
from django.shortcuts import render

from .models import Article

def year_archive(request, year):
    a_list = Article.objects.filter(pub_date__year=year)
    context = {'year': year, 'article_list': a_list}
    return render(request, 'news/year_archive.html', context)
```
创建`news/templates/news/year_achive.heml`编写html页面样式
```html
{% extends "base.html" %}

{% block title %}Articles for {{ year }}{% endblock %}

{% block content %}
<h1>Articles for {{ year }}</h1>

{% for article in article_list %}
    <p>{{ article.headline }}</p>
    <p>By {{ article.reporter.full_name }}</p>
    <p>Published {{ article.pub_date|date:"F j, Y" }}</p>
{% endfor %}
{% endblock %}
```
创建`news/templates/base.heml`编写html页面样式
```html
{% load static %}
<html>
<head>
    <title>{% block title %}{% endblock %}</title>
</head>
<body>
    <img src="http://www.cuc.edu.cn/_upload/site/00/05/5/logo.png" alt="Logo">
    {% block content %}{% endblock %}
</body>
</html>
```
在`yunpan/urls.py`添加对`news`应用地址进行配置的命令
```python
    path('news/', include('news.urls')),
```
在`news/templates/news/year_achive.heml`添加div样式改变标题颜色
```html
<h1><div style="color:red">Articles for {{ year }}</div></h1>
```
提交到`git`仓库
####3建立HOMEWORK提交表单
将`nwes/models.py`中的`Report`和`Article`改为`Student`和`Homework`
```python
from django.db import models

class Student(models.Model):
    full_name = models.CharField(max_length=70)
    class Sex(models.IntegerChoices):
        MALE = 1, ('MALE')
        FEMALE = 2, ('FEMALE')
        OTHER = 3, ('OTHER')
    sex = models.IntegerField(choices=Sex.choices)
    def __str__(self):
        return self.full_name

class Homework(models.Model):
    commit_date = models.DateField(auto_now=True)
    headline = models.CharField(max_length=200)
    attach = models.FileField()
    remark = models.TextField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
```
建立`news/templates/homework_form.html`提交html显示文件，加入代码
```html
<html>
<body>
<form method="post">{% csrf_token %}
    {{ form.as_p }}
    <input type="submit" value="Save">
</form>
</body>
</html>
```
修改`news/view.py`，添加表格形式
```python
from.models import Student, Homework

from django.views.generic.edit import CreateView

class HomeworkCreate(CreateView):
    model = Homework
    template_name = 'homework_form.html'
    fields = ['headline','attach','remark','student']
```
更改`news/urls.py`的访问
```python
urlpatterns = [
    path('hw/create/', views.HomeworkCreate.as_view()),
```
为`news/admin.py`添加用户组
```python
admin.site.register(models.Student)
```
**数据库迁移`python .\manage.py makemigrations` , `python .\manage.py migrate`**
修改form表单中的bug
```html
<html>
<body>
<form method="post" enctype="multipart/form-data" >{% csrf_token %}
    {{ form.as_p }}
    <input type="submit" value="Save">
</form>
</body>
</html>
```
创建根路径
```python
    path('',include('news.urls')),
```
```python
    path('', views.HomeworkCreate.as_view()),
```
运行服务器
