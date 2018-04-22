#-*-coding:utf-8-*-
from django.shortcuts import render,render_to_response,Http404, HttpResponse,HttpResponseRedirect
from django.db.models import Q
from .forms import LoginForm
from django.views.generic import View
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from ConnectMysql import execute_sql_str
from django.core.paginator import Paginator
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

class IndexView(View):
    def get(self,request):
        if request.user.is_authenticated():
            return render(request, 'profile.html')
        else:
            return HttpResponseRedirect('/login')

class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/index')
        else:
            return render(request, 'login.html')

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get('username', "")
            password = request.POST.get('password', "")
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/index')
                else:
                    return render(request, 'login.html', {'msg':u'用户未激活'})
            else:
                return render(request, 'login.html', {'msg':u'用户名或密码错误'})
        else:
            return render(request, 'login.html', {"login_form":login_form})





@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login')


@login_required
def search(request):
    if  request.method == 'GET':
        search_value = request.GET.get('q',"")
        return render(request, 'profile.html')



class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html', )

class UnitTestDataListView(View):
    def get(self, request):
        if request.user.is_authenticated():
            data = execute_sql_str('SELECT id ,methodName, description, createdtime, createdby FROM sg_pms')
            test_list = []
            for i in range(len(data)) :
                test_data = {}
                test_data['id'] = data[i][0]
                test_data['methodName'] = data[i][1]
                test_data['description'] = data[i][2]
                test_data['createdtime'] = data[i][3]
                test_data['createdby'] = data[i][4]
                test_list.append(test_data)
            try:
                page = request.GET.get('page',1)
            except PageNotAnInteger:
                page = 1
            #2表示当页面数据少于2个时合并到上一页
            print page
            p = Paginator(test_list, 16, 2)
            page_contacts = p.page(page)
            return render(request, 'unittest.html', {"page_data":page_contacts})
        else:
            return render(request, 'login.html',{})

class DeleteTestDataView(View):
    def post(self, request, pk):
        if request.user.is_authenticated():
            request.POST.get('id')





class UnitTestView(View):
    def get(self, request):
        return render(request, 'unittest.html')