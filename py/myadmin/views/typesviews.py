from django.shortcuts import render,reverse
from django.http import HttpResponse

from .. models import Types
# Create your views here.

def add(request):
    if request.method == 'GET':
        #返回一个添加的页面
        #获取当前数据库中的所有分类
    

        # context = {'tlist'}
        return render(request,'myadmin/types/add.html')
    elif request.method == 'POST':

        # 执行分类添加
        ob = Types()
        ob.name = request.POST['name']
        ob.pid = request.POST['pid']
        ob.path = '0,'
        ob.save()

        return HttpResponse('<script>alert("添加成功");location.href="'+reverse('myadmin_types_list')+'"</script>')

        



def index(request):
    pass



def delete(request):
    pass



def edit(request):
    pass