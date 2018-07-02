from django.shortcuts import render
from django.http import HttpResponse
import re

class AdminLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):

        # 当前用户请求的url路径
        u = request.path


        # # 定义后台请求的登录验证  /myadmin/user/add/
        # if re.match('/myadmin/',u) and u not in ['/myadmin/login/']:
        #     # 判断是否登录
        #     if not request.session.get('AdminLogin',None):
        #         # 没有登录
        #         return HttpResponse('<script>alert("请先登录");location.href="/myadmin/login/?next='+u+'"</script>')




        # 定义需要登录url请求
        urllist = ['/ordercheck/','/addressedit/','/addressadd/','/ordercreate/','/buy/','/mycenter/','/myorders/',]

        # 判断当前的请求是否需要登录
        if u in urllist:

            # 验证是否登录
            if not request.session.get('VipUser',None):
                # 没有登录
                return HttpResponse('<script>alert("请先登录");location.href="/login/?next='+u+'"</script>')



        # #验证是否登录
        # res = request.session.get('VipUser',None)
        # # 如果为假的时候   
        # if not res:  
        #     print('没有登录')

        response = self.get_response(request)
        return response