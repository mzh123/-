from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
#显示添加页面
def add(request):
    
    return render(request,'myadmin/user/add.html')

#执行用户数据添加
def insert(request):

    return HttpResponse('执行用户数据添加')