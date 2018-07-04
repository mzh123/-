from django.shortcuts import render
from django.http import HttpResponse
from myadmin.models import Users,Types,Goods,Address,Orders,OrderInfo
# Create your views here.

from django.contrib.auth.decorators import permission_required


@permission_required('myadmin.show_order',raise_exception = True)
def index(request):
    
    # 获取当前用户的所有订单
    data = Orders.objects.all()

    context = {'orderlist':data}
    
    return render(request,'myadmin/order/list.html',context)


