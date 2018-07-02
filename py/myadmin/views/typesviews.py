from django.shortcuts import render,reverse
from django.http import HttpResponse,JsonResponse

from .. models import Types
# Create your views here.

def gettypesorder():
    

    tlist=Types.objects.extra(select = {'paths':'concat(path,id)'}).order_by('paths')

    for x in tlist:
        if x.pid == 0:
            x.pname = '顶级分类'
        else:
            t = Types.objects.get(id=x.pid)
            x.pname = t.name
        num = x.path.count(',')-1
        x.name = (num*'|---')+x.name

    return tlist
            



def add(request):
    if request.method == 'GET':
        #返回一个添加的页面
        #获取当前数据库中的所有分类
        # tlist = Types.objects.all()

        tlist = gettypesorder()

        context = {'tlist':tlist}
    

        # context = {'tlist'}
        return render(request,'myadmin/types/add.html',context)
    elif request.method == 'POST':

        # 执行分类添加
        ob = Types()
        ob.name = request.POST['name']
        ob.pid = request.POST['pid']
        if ob.pid == '0':
            ob.path = '0,'
        else:
            #根据当前父级id获取path,再添加当前父级id
            t = Types.objects.get(id=ob.pid)
            ob.path = t.path+(ob.pid)+','
        ob.save()

        return HttpResponse('<script>alert("添加成功");location.href="'+reverse('myadmin_types_list')+'"</script>')

        



def index(request):
    #获取所有的分类信息

    # tlist = Types.objects.all()

    tlist = gettypesorder()

    context = {'tlist':tlist}

    return render(request,'myadmin/types/list.html',context)



def delete(request):
    # try:
    tid = request.GET.get('uid',None)

        #判断当前类下是否为子类

    num = Types.objects.filter(pid=tid).count()
    #如果num 不等于　0
    if num != 0:
        data = {'msg':'当前类下有子类，不能删除','code':1}
    else:
        ob = Types.objects.get(id=tid)
        #判断当前累下是否商品
        ob.delete()
        data={'msg':'删除成功','code':0}
    # except:
    #     data={'msg':'删除失败','code':1}

    return JsonResponse(data)

def edit(request):
    #接受参数
    uid = request.GET.get('uid',None)
    #获取对象
    ob = Goods.objects.get(id=uid)

    if request.method == 'GET':
        
        #分配数据
        context = {'uinfo':ob}
        #显示编辑页面
        return render(request,'myadmin/goods/edit.html',context)