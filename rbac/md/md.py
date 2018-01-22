# !/usr/bin/env python
# coding:utf-8
# author bai
import re
from django.shortcuts import render,redirect,HttpResponse
from django.conf import settings

class MiddlewareMixin(object):
    def __init__(self, get_response=None):
        self.get_response = get_response
        super(MiddlewareMixin, self).__init__()

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response

class M1(MiddlewareMixin):
    '''
    判断用户有无此url的权限的中间件
    '''
    def process_request(self,request):
        current_url = request.path_info

        # 1.白名单验证
        valid_url = settings.VALID_URL
        for each in valid_url:
            if re.match(each, current_url):
                return None

        # 2.验证是否已经写入session，即：是否已经登录
        permission_dic = request.session.get('permission_url_list')
        if not permission_dic:
            return redirect('/login/')
        print('在中间件这里写入了permission_code_list')
        # 3.与当前访问的url与权限url进行匹配验证,并在request中写入code信息，
        flag = False
        for group_id,code_urls in permission_dic.items():
            for url in code_urls['per_url']:
                regax = '^{0}$'.format(url)
                if re.match(regax,current_url):
                    flag = True

                    request.permission_code_list = code_urls['code']  # 在session中增加code的信息，用于在页面判断在当前页面的权限，
                    break
            if flag:
                break

        if not flag:
            return HttpResponse('无权访问')


    def process_response(self,request,response):
        return response

