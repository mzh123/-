"""py URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from .views import views,userviews,typesviews,goodsviews,authviews,orderviews

urlpatterns = [
    #后台首页
    url(r'^$', views.index,name='myadmin_index'),
    #会员管理
    url(r'^user/add/$',userviews.add,name='myadmin_user_add'),
    url(r'^user/list/$',userviews.list,name='myadmin_user_list'),
    url(r'^user/delete/$',userviews.delete,name='myadmin_user_delete'),
    url(r'^user/edit/$',userviews.edit,name='myadmin_user_edit'),



  


    # 后台权限管理

    # 后台用户添加
    url(r'^auth/user/add/$',authviews.useradd,name='auth_user_add'),
    # 后台用户列表
    url(r'^auth/user/list/$',authviews.userlist,name='auth_user_list'),
    url(r'^auth/user/del/(?P<uid>[0-9]+)/$',authviews.userdel,name='auth_user_del'),

    # 后台组添加
    url(r'^auth/group/add/$',authviews.groupadd,name='auth_group_add'),
    # 后台组列表
    url(r'^auth/group/list/$',authviews.grouplist,name='auth_group_list'),
    url(r'^auth/group/edit/(?P<gid>[0-9]+)/$',authviews.groupedit,name='auth_group_edit'),


    #商品分类管理
    url(r'^types/add/$',typesviews.add,name='myadmin_types_add'),
    url(r'^types/index/$',typesviews.index,name='myadmin_types_list'),
    url(r'^types/delete/$',typesviews.delete,name='myadmin_types_delete'),
    url(r'^types/edit/$',typesviews.edit,name='myadmin_types_edit'),



    #商品管理
    url(r'^goods/add/$',goodsviews.add,name='myadmin_goods_add'),
    url(r'^goods/index/$',goodsviews.index,name='myadmin_goods_list'),
    url(r'^goods/delete/$',goodsviews.delete,name='myadmin_goods_delete'),
    url(r'^goods/edit/$',goodsviews.edit,name='myadmin_goods_edit'),

    #订单列表
    url(r'^order/index/$',orderviews.index,name='myadmin_order_list'),



    # 后台登录和登录验证
    url(r'^login/$', authviews.mylogin,name='myadmin_login'),

    # 退出登录
    url(r'^loginout/$',authviews.mylogout,name='admin_loginout'),



]
