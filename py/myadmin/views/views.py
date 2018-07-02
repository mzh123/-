from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    

    return render(request,'myadmin/index.html')



# 后台登录
def login(request):
    
    if request.method == 'GET':

        return render(request,'myadmin/login.html')

    elif request.method == 'POST':

        # 执行登录

        return HttpResponse('执行登录')