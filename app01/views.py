import re
from django.shortcuts import render,redirect,HttpResponse
from django.urls import reverse
from rbac import models
from rbac.service.init_permission import init_permission

def login(request):
    '''用户登录'''
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        current_user = models.User.objects.filter(username=username,password=password).first()
        if current_user:
            # 如果用户名登录正确，则需要获取当前用户的权限信息，并把这个权限信息写入到session.
            init_permission(user=current_user,request=request)
            return redirect(reverse('index'))
    return HttpResponse('LOGIN')

class Page_permission(object):
    '''用于在页面显示按钮，便签是否显示'''
    def __init__(self,code_list):
        self.code_list = code_list

    def has_add(self):
        if 'add' in self.code_list:
            return True

    def has_list(self):
        if 'list' in self.code_list:
            return True

    def has_edit(self):
        if 'edit' in self.code_list:
            return True

    def has_del(self):
        if 'del' in self.code_list:
            return True

# 在session中拿到的关于生成menu的数据，还需要结构化中需要的结构，用于在前端页面直接用for循环展开。
# menu_list_text = [
#     {'menu_id': 1, 'menu_title': '菜单一', 'permission__title': '用户列表', 'permission_url': '/userinfo/', 'permissions__is_menu': True,'active':False},
#     {'menu_id': 1, 'menu_title': '菜单一', 'permission__title': '订单列表', 'permission_url': '/order/', 'permissions__is_menu': True,'active':False},
#     {'menu_id': 2, 'menu_title': '菜单二', 'permission__title': '订单列表ss', 'permission_url': '/orderss/', 'permissions__is_menu': True,'active':False},
# ]
def userinfo(request):
    page_permission = Page_permission(request.permission_code_list)   # 传入在中间件写入request的code_list
    users = models.User.objects.all()

    return render(request, 'userinfo.html', {'users':users, 'page_permission':page_permission,})


def userinfo_add(request):
    return render(request,'userinfo_add.html')

def userinfo_edit(request,nid):
    return render(request,'userinfo_edit.html')

def order(request):
    # 模拟订单的数据
    order_info = {'banana': 5, 'apple': 10}
    return render(request,'order.html',{'order':order_info})

def index(request):

    return render(request,'index.html')
