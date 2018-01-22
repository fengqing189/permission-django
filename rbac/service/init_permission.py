# !/usr/bin/env python
# coding:utf-8
# author bai

def init_permission(user, request):
    '''
    前端页面调用，把当前登录用户的权限放到session中，request参数指前端传入的当前当前login请求时的request
    :param user: 当前登录用户
    :param request: 当前请求
    :return: None
    '''
    # 拿到当前用户的权限信息
    print('--------------')
    permission_url_list = user.roles.values('permissions__group_id',
                                            'permissions__code',
                                            # 'permissions__url',
                                            'permissions__group__menu__id',     # 菜单需要
                                            'permissions__group__menu__title',    # 菜单需要
                                            'permissions__title',   # 菜单需要
                                            'permissions__url',     # 菜单需要
                                            'permissions__menu_gp',  # 菜单需要
                                            ).distinct()
    # 页面显示权限相关，用到了权限的分组,
    print('+++++',permission_url_list)
    dest_dic = {}
    for each in permission_url_list:
        if each['permissions__group_id'] in dest_dic:
            dest_dic[each['permissions__group_id']]['code'].append(each['permissions__code'])
            dest_dic[each['permissions__group_id']]['per_url'].append(each['permissions__url'])
        else:
            # 刚循环，先创建需要的结构,并把第一次的值放进去。
            dest_dic[each['permissions__group_id']] = {'code': [each['permissions__code'], ],
                                                       'per_url': [each['permissions__url'], ]}
    request.session['permission_url_list'] = dest_dic
    print('dest_dic',dest_dic)

    # 页面菜单相关
    # 1.去掉不做菜单的url,拿到的结果是menu_list,列表中的元素是字典
    menu_list = []
    for item_dic in permission_url_list:
        if not item_dic['permissions__menu_gp']:
            temp = {'menu_id':item_dic['permissions__group__menu__id'],
                    'menu_title':item_dic['permissions__group__menu__title'],
                    'permission__title': item_dic['permissions__title'],
                    'permission_url':item_dic['permissions__url'],
                    'permissions__menu_gp':item_dic['permissions__menu_gp'],
                    'active':False,   # 用于页面是否被选中，
                    }
            menu_list.append(temp)   # temp 其实只是给key重新起名字，之前的名字太长了。。。。
    request.session['permission_menu_list'] = menu_list
    print(menu_list)

    # 执行完成之后是如下的数据，用来做菜单。
    # menu_list = [
    #     {'menu_id': 1, 'menu_title': '菜单一', 'permission__title': '用户列表', 'permission_url': '/userinfo/', 'permissions__is_menu': True,'active':False},
    #     {'menu_id': 1, 'menu_title': '菜单一', 'permission__title': '订单列表', 'permission_url': '/order/', 'permissions__is_menu': True,'active':False}
    # ]