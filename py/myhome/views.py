from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from myadmin.models import Users,Types,Goods,Address,Orders,OrderInfo

from django.contrib.auth.hashers import make_password, check_password
#首页
def index(request):
    
    #先获取所有顶级分类
    data = Types.objects.filter(pid=0)
    erdata = []
    for x in data:
        # print(x.name)
        #获取当前类下的子类
        x.sub = Types.objects.filter(pid=x.id)

        # print(x.sub)

        for v in x.sub:
            v.goodssub = Goods.objects.filter(typeid=v.id)

            erdata.append(v)


    context = {'typegoodslist':data,'erdata':erdata}

    return render(request,'myhome/index.html',context)

#列表
def list(request,tid):

    #根据分类id获取分类信息和商品信息
    data = Goods.objects.filter(typeid = tid)

    #分配
    context = {'goodslist':data}

    # print(data.count())
    #加载模板
    return render(request,'myhome/list.html',context)

#搜索
def search(request):


    #获取搜索参数
    keywords  = request.GET.get('keywords',None)

    if not keywords:
        return HttpResponse('<script>history.back(-1)</script>')
    
    data = Goods.objects.filter(title__contains=keywords)

    context = {'goodslist': data}

    return render(request,'myhome/search.html',context)

#详情
def info(request,sid):
    try:

        #根据商品id 获取商品信息
        data = Goods.objects.get(id=sid)

        #修改当前商品的点击量
        data.clicknum = data.clicknum + 1
        data.save()

        context = {'ginfo':data}

        return render(request,'myhome/info.html',context)
    except:
        pass

#登录
def login(request):
    nexturl = request.GET.get('next','/')
    if request.method == 'GET':

        return render(request,'myhome/login.html')

    elif request.method == 'POST':
        #执行登录
        #根据用户先获取用户对象,再检测密码是否正确

        #先判断验证码是否正确
        if request.POST['vcode'].upper() != request.session['verifycode'].upper():
            return HttpResponse('<script>alert("验证码错误");history.back(-1)</script>')



        try:
            ob = Users.objects.get(username = request.POST['username'])

            #检测密码是否正确
            res = check_password(request.POST['password'],ob.password)

            if res:
                #密码正确
                request.session['VipUser'] = {'uid':ob.id,'username':ob.username}
            
                return HttpResponse('<script>alert("登录成功");location.href="'+nexturl+'"</script>')

        except:
            # #用户名错误
            # # 接收表单提交的数据,
            # data = request.POST.copy().dict()
            # #删除掉csrf验证的字段数据
            # del data['csrfmiddlewaretoken']
            # del data['vcode']
            pass


        return HttpResponse('<script>alert("用户名或密码错误,请重新登录");history.back(-1)</script>')

#注册
def register(request):

    if request.method == 'GET':

        return render(request,'myhome/register.html')

    elif request.method == 'POST':

        #先判断验证码是否正确
        if request.POST['vcode'].upper() != request.session['verifycode'].upper():
            return HttpResponse('<script>alert("验证码错误");history.back(-1)</script>')

        #用户数据的创建

        
        # 接收表单提交的数据,
        data = request.POST.copy().dict()
        #删除掉csrf验证的字段数据
        del data['csrfmiddlewaretoken']
        del data['vcode']


        #进行密码加密
           
        data['password'] = make_password(data['password'], None, 'pbkdf2_sha256')


        #执行用户的添加
        try:
            ob = Users.objects.create(**data)

            #记录用户登录的状态  session

            request.session['VipUser'] = {'uid':ob.id,'username':ob.username}

            return HttpResponse('<script>alert("注册成功");location.href="/"</script>')
        # except pymysql.err.Integrityerror:
        #     return HttpResponse('<script>alert("用户名已存在");history.back(-1)="/"</script>')
        except:
            pass
            
        return HttpResponse('<script>alert("注册失败");history.back(-1)</script>')


        # #接收请求参数,执行用户添加
        # return HttpResponse('post')
        
#退出登录
def logout(request):
    

    request.session['VipUser'] = {}
    

    return HttpResponse('<script>alert("退出成功");location.href="/"</script>')

#验证码
def vcode(request):
   
    #引入绘图模块
    from PIL import Image, ImageDraw, ImageFont
    #引入随机函数模块
    import random
    #定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100), 255)
    width = 100
    height = 25
    #创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    #创建画笔对象
    draw = ImageDraw.Draw(im)
    #调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    #定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    #随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    #构造字体对象
    font = ImageFont.truetype('FreeMono.ttf', 23)
    #构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    #绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    #释放画笔
    del draw
    #存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    #内存文件操作
    import io
    buf = io.BytesIO()
    #将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    #将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')   

#加入购物车
def addcart(request):
    #获取商品id和商品购买数量
    sid = request.GET['sid']
    num = int(request.GET['num'])

    #先获取购物车的商品数据
    data = request.session.get('cart',{})


    #判断要购买的商品是否已存在购物车
    if sid in data.keys():
        #如果存在  修改数量
        data[sid]['num'] += num
    else:
        #定义加入购物车的商品数据
        
        #如果不存在  再进行添加
        
        ob = Goods.objects.get(id=sid)
        
        goods = {'id':ob.id,'title':ob.title,'price':float(ob.price),'pics':ob.pics,'num':num}
        
        #把购物车存入session中
        data[sid] = goods

        #将商品加入购物车
    request.session['cart'] = data

    return HttpResponse('1')
   
#购物车列表
def shopcartlist(request):

    # data = request.session.get('cart',{})


    # for v in data.values():
    #     print(v)
    # 获取session的购物车
    data = request.session.get('cart',None)

    if data:

        data = data.values()


    return render(request,'myhome/cart.html',{'data':data})

#清空购物车
def emptyshopcart(request):

    request.session['cart'] = {}

    return HttpResponse('<script>location.href="/shopcartlist/"</script>')

#删除购物车的一个商品
def delcart(request):

    #接受一下商品id  ajax传过来的
    sid = request.GET['sid']

    #先把购物车的数据给读出来        获取session中的购物车数据
    data = request.session['cart']  
    #在这个变量中删除
    del data[sid]

    #把购物车重新写入session  
    request.session['cart'] = data

    return HttpResponse('0')

#修改购物车商品数量
def editcart(request):
    #告诉我商品id
    sid = request.GET['sid']
    num = int(request.GET['num'])

    # 在session 中获取购物车数据
    data = request.session['cart']

    #修改
    data[sid]['num'] = num 

    #把购物车重新写入session
    request.session['cart'] = data

    return HttpResponse('0')


# 订单确认
def ordercheck(request):
    # 获取购物车提交的数据
    items = eval(request.GET['items'])

    data = {}
    totalprice = 0
    totalnum = 0

    for x in items:
        ob = Goods.objects.get(id=x['goodsid'])
        x['title'] = ob.title
        x['price'] = float(ob.price)
        x['pics'] = ob.pics
        # 计算总价和总数
        totalprice += x['num']*x['price']
        totalnum += x['num']

    data['totalprice'] = round(totalprice,2)
    data['totalnum'] = totalnum
    data['items'] = items

    # 把确认的商品信息.,存入session
    request.session['order'] = data

    # 需要获取当前用户的收货地址
    addlist = Address.objects.filter(uid=request.session['VipUser']['uid'])


    context = {'data':data,'addlist':addlist}

    return render(request,'myhome/ordercheck.html',context)


# 地址修改
def addressedit(request):
    
    aid = int(request.GET['aid'])
    uid = request.session['VipUser']['uid']
    # 获取当前用户的所有收货地址
    obs = Address.objects.filter(uid=uid)
    for x in obs:
        if x.id == aid:
            x.status = 1
        else:
            x.status = 0
        x.save()

    return HttpResponse(0)



# 地址添加
def addressadd(request):
    data = eval(request.GET['data'])



    data['address'] = ",".join(data['address'])
    data['uid'] = Users.objects.get(id=request.session['VipUser']['uid'])

    # 添加地址信息
    res =  Address.objects.create(**data)

    # print(res)
    
    return HttpResponse(0)


# 生成订单
def ordercreate(request):

    # 接受用户id
    uid = request.session['VipUser']['uid']
    # 收货地址id
    addressid = request.POST['addressid']
    # 商品信息
    data = request.session['order']

    # 获取购物车中的数据
    cart = request.session['cart']

    print(cart)


    # 生成订单
    ob = Orders()
    ob.uid = Users.objects.get(id=uid)
    ob.addressid = Address.objects.get(id=addressid)
    ob.totalprice = data['totalprice']
    ob.totalnum = data['totalnum']
    ob.save()


    # .订单详情
    for v in data['items']:
     
        oinfo = OrderInfo()
        oinfo.orderid = ob
        oinfo.gid = Goods.objects.get(id=v['goodsid'])
        oinfo.num = v['num']
        oinfo.save()
        # 在购物车中删除当前购买的商品
        del cart[v['goodsid']]


    # 清除购物车中已经下单的商品,清除order数据
    request.session['cart'] = cart
    request.session['order'] = ''

    # 把生成订单id get请求到一个新的付款页面

    return HttpResponse('<script>location.href="/buy/?orderid='+str(ob.id)+'"</script>')

# 支付
def buy(request):

    orderid = request.GET['orderid']

    data = Orders.objects.get(id=orderid)
    print(data)

    context = {'orderlist':data}


    return render(request,'myhome/buy.html',context)

# 我的个人中心
def mycenter(request):
    
    return render(request,'myhome/word/mycenter.html')

# 我的订单
def myorders(request):
    # 获取当前用户的所有订单
    data = Orders.objects.filter(uid=request.session['VipUser']['uid'])

    context = {'orderlist':data}
    
    return render(request,'myhome/word/myorders.html',context)

#个人中心
def information(request):


    return render(request,'myhome/word/information.html')