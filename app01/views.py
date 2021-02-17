from django.shortcuts import render,redirect
from django.views import View
from django.forms import Form
from django.forms import fields

class MyForm(Form):
    username = fields.CharField(
        max_length=16,
        min_length=6,
        required=True,
        error_messages={
            'max_length':'用户名长度应小于16位',
            'min_length':'用户名长度应大于6位',
            'required':'用户名不能为空',
        })
    password = fields.CharField(
        max_length=16,
        min_length=6,
        required=True,
        error_messages={
            'max_length':'密码长度应小于16位',
            'min_length':'密码长度应大于6位',
            'required':'密码不能为空',
        })

# Create your views here.
class Login(View):
    def get(self,request):
        return render(request,'login.html')
    def post(self,request):
        v = MyForm(request.POST)
        print(v.is_valid())
        if v.is_valid() and v.cleaned_data['username'] == '754914142' and v.cleaned_data['password']=='754914142':
            #对比账号密码
            request.session['userinfo'] = {'username':v.cleaned_data['username'],'password':v.cleaned_data['password']}
            return redirect('/index/')
        else:
            return render(request,'login.html',{'erro':v.errors})

def login(func):
    def wrap(request, *args, **kwargs):
        if request.session.get('userinfo'):
            return func(request, *args, **kwargs)
        else:
            return redirect('/login/')
    return wrap

@login
def index(request):
    v = request.session.get('userinfo')
    return render(request, 'index.html',{'v':v})

@login
def logout(request):
    request.session.delete()
    return redirect('/login/')