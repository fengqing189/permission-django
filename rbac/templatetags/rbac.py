# !/usr/bin/env python
# coding:utf-8
# author bai
import re

from django.template import Library
from rbac import models

register = Library()

# inclusion_tag的结果是：把menu_html函数的返回值，放到menu_html中做渲染，生成一个渲染之后的大字符串，
# 在前端需要显示这个字符串的地方，只要调用menu_html就可以，如果有菜单需要传参数，这里是request,前端模板本来就有request,
@register.inclusion_tag('menu.html')
def menu_html(request):
    current_url = request.path_info

    # 结构化在页面显示的menu数据
    menu_list = request.session.get('permission_menu_list')

    # for item in menu_list:    # item是每一个做菜单的url
    #     # 先跟当前url进行匹配，如果当前的url在权限URl中，则需要修改当前的active，用于在前端页面的显示。
    #     url = item['permission_url']   # url分为两种，1.是菜单的url,2.组内不是做菜单的url
    #     reg = '^{0}$'.format(url)
    #     if re.match(reg, current_url):
    #         item['active'] = True
    print(menu_list)
    # 思路：直接拿到当前url，拿到他的组内菜单，然后再menu_list中，修改他的item['active'] = True,用于在前端页面展示
    all_url = models.Permission.objects.all()
    for url_reg in all_url:
        reg = '^{0}$'.format(url_reg.url)
        if re.match(reg,current_url):  # 匹配上那么url_reg就是当前访问的url,只需要找到他的组内菜单url即可，
            if not url_reg.menu_gp:  # 访问url就是组内做菜单的url
                for item in menu_list:
                    url = item['permission_url']
                    new_reg = '^{0}$'.format(url)
                    if re.match(new_reg, url_reg.url):
                        item['active'] = True
            else:
                for item in menu_list:
                    url = item['permission_url']
                    new_reg = '^{0}$'.format(url)
                    if re.match(new_reg, url_reg.menu_gp.url):
                        item['active'] = True

    menu_show_dic = {}   # 这个字典中储存格式化的菜单，在前端直接两层for循环出来展示就可以了，
    for item in menu_list:
        if item['menu_id'] in menu_show_dic:
            menu_show_dic[item['menu_id']]['children'].append(
                {'permission__title': item['permission__title'], 'permission_url': item['permission_url'],
                 'active': item['active']})
            if item['active']:
                menu_show_dic[item['menu_id']]['active'] = True
        else:
            menu_show_dic[item['menu_id']] = {'menu_id': item['menu_id'],
                                              'menu_title': item['menu_title'],
                                              'active': False,
                                              'children': [{'permission__title': item['permission__title'],
                                                            'permission_url': item['permission_url'],
                                                            'active': item['active']}, ]
                                              }
            if item['active']:
                menu_show_dic[item['menu_id']]['active'] = True


    return {'menu_dic':menu_show_dic}