from django.shortcuts import render,reverse
from django.http import HttpResponse

from . typesviews import gettypesorder
from . userviews import uploads

from .. models import Goods,Types

# Create your views here.


def add(request):
    if request.method == 'GET':
        tlist = gettypesorder()
        context = {'tlist':tlist}
        return render(request,'myadmin/goods/add.html',context)
    elif request.method == 'POST':

        #先判断是否有图片上传
        if not request.FILES.get('pic',None):

            return HttpResponse('<script>alert("必须选择商品图片");location.href="'+reverse('myadmin_goods_add')+'"</script>')

        pic = uploads(request)
        if pic == 1: 
            return HttpResponse('<script>alert("图片类型错误");location.href="'+reverse('myadmin_goods_add')+'"</script>')
        #执行商品的添加
        #接受表但提交的数据
        data = request.POST.copy().dict()
        #删除掉  csrt验证的字段数据
        del data['csrfmiddlewaretoken']
        data['pics'] = pic

        data['typeid'] = Types.objects.get(id=data['typeid'])

        #执行用户的创建
        ob = Goods.objects.create(**data)

        # print(data)
        print(ob)
        return HttpResponse('post')

def index(request):
    glist = Goods.objects.all()

    context = {'glist':glist}

    return render(request,'myadmin/goods/list.html',context)



def delete(request):
    pass



def edit(request):
    pass