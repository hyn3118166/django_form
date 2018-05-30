from django.shortcuts import render, redirect
from apps.blog.models import Article, Category, Tag, user, reply
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404, HttpResponse, JsonResponse
from django.conf import settings
from django.views import View
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
import datetime
categories = Category.objects.all()  # 获取全部的分类对象
tags = Tag.objects.all()  # 获取全部的标签对象
months = Article.objects.datetimes('pub_time', 'month', order='DESC')


# Create your views here.
def home(request):  # 主页
    # if request.session.get("is_login", None):
    #
    # # if request.GET.get("Cancellation"):
    # #     del request.session["is_login", "is_user"]
    # #     return redirect("/login")
    # return redirect("/login")
    name = request.session.get("is_user")
    posts = Article.objects.filter(status='p',
                                   pub_time__lt=datetime.datetime.now().strftime("%Y-%m-%d %H:%I:%S")
                                   ).order_by("-views")  # 获取全部(状态为已发布，发布时间不为空)Article对象filter(status='p', pub_time__isnull=False)
    paginator = Paginator(posts, settings.PAGE_NUM)  # 每页显示数量
    page = request.GET.get('page')  # 获取URL中page参数的值
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'home.html', {'post_list': post_list,
                                         'category_list': categories,
                                         'months': months,
                                         'name': name,
                                         'tags': tags,
                                         })


# 阅读全文
def detail(request, id):
    # if request.session.get("is_login", None):
        name = request.session.get("is_user")
        try:
            page = request.GET.get("id")
            post = Article.objects.get(id=str(id))
            post.viewed()  # 更新浏览次数
            bbs_names = post.use_id
            tags = post.tags.all()
            next_post = post.next_article()  # 上一篇文章对象
            prev_post = post.prev_article()  # 下一篇文章对象
            rel = reply.objects.filter(bbs_id=str(id))
        except Article.DoesNotExist:
            raise Http404
        return render(
                request, 'post.html',
                {
                    'post': post,
                    'tags': tags,
                    'category_list': categories,
                    'next_post': next_post,
                    'prev_post': prev_post,
                    'months': months,
                    'name': name,
                    'replay': rel,
                }
            )
    # return redirect("/login")


#   分类内
def search_category(request, id):
    # if request.session.get("is_login", None):
        name = request.session.get("is_user")
        posts = Article.objects.filter(category_id=str(id), status='p',
                                       pub_time__lt=datetime.datetime.now().strftime("%Y-%m-%d %H:%I:%S")
                                       ).order_by("-created_time")
        category = categories.get(id=str(id))
        paginator = Paginator(posts, settings.PAGE_NUM)  # 每页显示数量
        try:
            page = request.GET.get('page')  # 获取URL中page参数的值
            post_list = paginator.page(page)
        except PageNotAnInteger:
            post_list = paginator.page(1)
        except EmptyPage:
            post_list = paginator.page(paginator.num_pages)
        return render(request, 'category.html',
                      {'post_list': post_list,
                       'category_list': categories,
                       'category': category,
                       'months': months,
                       'name': name,
                      }
        )
    # return redirect("/login")


# 遍历标签
def search_tag(request, tag):
    # if request.session.get("is_login", None):
        name = request.session.get("is_user")
        posts = Article.objects.filter(tags__name__contains=tag)
        paginator = Paginator(posts, settings.PAGE_NUM)  # 每页显示数量
        try:
            page = request.GET.get('page')  # 获取URL中page参数的值
            post_list = paginator.page(page)
        except PageNotAnInteger:
            post_list = paginator.page(1)
        except EmptyPage:
            post_list = paginator.page(paginator.num_pages)
        return render(request, 'tag.html', {
            'post_list': post_list,
            'category_list': categories,
            'tags': tags,
            'months': months,
            'name': name,
            }
        )
    # return redirect("login")


# 标签内
def archives(request, year, month):
    # if request.session.get("is_login", None):
        name = request.session.get("is_user")
        posts = Article.objects.filter(pub_time__year=year, status='p',
                                       pub_time__month=month,
                                       ).order_by("-pub_time")
        paginator = Paginator(posts, settings.PAGE_NUM)  # 每页显示数量
        try:
            page = request.GET.get('page')  # 获取URL中page参数的值
            post_list = paginator.page(page)
            print(page)
        except PageNotAnInteger:
            post_list = paginator.page(1)
        except EmptyPage:
            post_list = paginator.page(paginator.num_pages)
        return render(request, 'archive.html', {
            'post_list': post_list,
            'category_list': categories,
            'months': months,
            'year_month': year+'年'+month+'月',
            'name': name,
            }
        )
    # if request.GET.get("Cancellation"):
    #     del request.session["is_login", "is_user"]
    # return redirect("/login")


# 登录
def login(request):
    if request.method == "POST":
        name = request.POST.get("user")
        pwd = request.POST.get("pwd")
        if name == '' or pwd == '':
            return JsonResponse({"tip": "不能为空"})
        users = user.objects.filter(user_name=name)
        # print(users[0].user_name, pwd, users[0].user_paw)
        if check_password(pwd, users[0].user_paw):
            if users[0].user_leg == -1:
                return JsonResponse({"tip": "该账号已被禁用"})
            request.session["is_login"] = True
            request.session["is_user"] = name
            # request.session["is_id"] = i.id
            return JsonResponse({"tip": "跳至主页面"})
        return JsonResponse({"tip": "账号或密码错误"})
    return render(request, "login.html",)


# 注册
def register(request):
    if request.method == "POST":
        name = request.POST.get("user")
        pwd = request.POST.get("pwd")
        pwd2 = request.POST.get("pwd2")
        if pwd == pwd2:
            pwd = make_password(pwd)
            email = request.POST.get("email")
            if name == "":
                return JsonResponse({"tip": "用户名为空"})
            elif user.objects.filter(user_name=name):
                return JsonResponse({"tip": "用户名重复"})
            user.objects.create(user_name=name, user_paw=pwd, user_email=email)
            request.session["is_login"] = True
            request.session["is_user"] = name
            return JsonResponse({"tip": "注册成功"})
        else:
            return JsonResponse({"tip": "两次密码输入不一致"})
    return render(request, "register.html",)


# 注销
def bye(request):
    try:
        del request.session['is_login']
        del request.session['is_user']
    except KeyError:
        pass
    return render(request, "demo.html")


# 评论
def comment(request):
    if request.session.get("is_login", None):
        if request.method == "POST":
            namer = request.session.get("is_user")
            print(namer)
            uid = user.objects.get(user_name=namer)
            re = request.POST.get("replay")
            id = int(request.POST.get('id'))
            print(id)
            bbs = Article.objects.get(id=str(id))
            print(bbs)
            reply.objects.create(bbs_id=bbs, user_id=uid, content=re,
                                 time=datetime.datetime.now().strftime("%Y-%m-%d %H:%I:%S"))
            try:
                # page = request.GET.get("id")
                post = Article.objects.get(id=str(id))
                post.viewed()  # 更新浏览次数
                tags = post.tags.all()
                next_post = post.next_article()  # 上一篇文章对象
                prev_post = post.prev_article()  # 下一篇文章对象
                rel = reply.objects.filter(bbs_id=str(id))
            except Article.DoesNotExist:
                raise Http404
            return render(
                request, 'post.html',
                {
                    'post': post,
                    'tags': tags,
                    'category_list': categories,
                    'next_post': next_post,
                    'prev_post': prev_post,
                    'months': months,
                    'name': namer,
                    'replay': rel,
                }
            )

            # return redirect("/home")
    return redirect("/login")


def publish(request):
    if request.session.get("is_login", None):
        if request.method == 'GET':
            name = request.session.get("is_user")
            return render(
                request, "publish.html",
                {
                 'category_list': categories,
                 'months': months,
                 'name': name,
                 'tags': tags,
                 }
            )
        if request.method == 'POST':
            name = request.session.get("is_user")
            title = request.POST.get("title")
            content = request.POST.get("content")
            status = request.POST.get("status")
            category = request.POST.get("category")
            tag = request.POST.get("tag")
            pub_time = request.POST.get("pub_time")
            # time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # pub_time = time.strptime(pub_time, "%Y-%m-%d %H:%M:%S")
            print(name, title, content, status, category, tag, pub_time)
            a = Article.objects.create(title=title, content=content,
                                       status=status, category_id=category,
                                       pub_time=pub_time,
                                       use=user.objects.filter(user_name=name).first()
                                       )
            a.tags.add(tag)
            # return redirect("/home")
            return JsonResponse({"tip": "发表成功"})
            # return  HttpResponse("123")
    return redirect('/login')


def search_title(request):
    if request.method == "POST":
        pass
        return JsonResponse({"tip": "跳至查询页"})
    title = request.GET.get("title")
    print(title)
    name = request.session.get("is_user")
    posts = Article.objects.filter(status='p',
                                   pub_time__lt=datetime.datetime.now().strftime("%Y-%m-%d %H:%I:%S"),
                                   title__icontains=title).order_by("-created_time")
    paginator = Paginator(posts, settings.PAGE_NUM)  # 每页显示数量
    page = request.GET.get('page')  # 获取URL中page参数的值
    print(posts)
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'search_title.html',
                  {
                   'post_list': post_list,
                   'category_list': categories,
                   'months': months,
                   'name': name,
                   'tags': tags,
                  })


def user_Post(request):
    if request.session.get("is_login", None):
        action = request.GET.get("action")
        name = request.session.get("is_user")
        if action == "modify":
            pid = request.GET.get("id")
            request.session["modify_id"] = str(pid)
            print(request.session["modify_id"], pid, str(pid))
            return redirect("/modify_publish")
        elif action == "delete":
            pid = request.GET.get("id")
            Article.objects.filter(id=pid).delete()
        posts = Article.objects.filter(use__user_name=name).order_by("-created_time")
        paginator = Paginator(posts, 6)  # 每页显示数量
        page = request.GET.get('page')  # 获取URL中page参数的值
        try:
            post_list = paginator.page(page)
        except PageNotAnInteger:
            post_list = paginator.page(1)
        except EmptyPage:
            post_list = paginator.page(paginator.num_pages)
        return render(request, 'user_Post.html',
                      {
                       'post_list': post_list,
                       'category_list': categories,
                       'months': months,
                       'name': name,
                       'tags': tags,
                      })
    return redirect("/login")


def modify_publish(request):
    if request.session.get("is_login", None):
        if request.method == 'GET':
            name = request.session.get("is_user")
            pid = request.session.get("modify_id")
            post = Article.objects.filter(id=pid)
            return render(
                request, "modify_publish.html",
                {
                 'post': post,
                 'category_list': categories,
                 'months': months,
                 'name': name,
                 'tags': tags,
                 }
            )
        if request.method == 'POST':
            pid = request.session.get("modify_id")
            name = request.session.get("is_user")
            title = request.POST.get("title")
            content = request.POST.get("content")
            status = request.POST.get("status")
            category = request.POST.get("category")
            tag = request.POST.get("tag")
            pub_time = request.POST.get("pub_time")
            # time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # pub_time = time.strptime(pub_time, "%Y-%m-%d %H:%M:%S")
            print(name, title, content, status, category, tag, pub_time)
            Article.objects.filter(id=pid).update(title=title, content=content,
                                                  status=status, category_id=category,
                                                  pub_time=pub_time, use=user.objects.filter(user_name=name).first())
            # a.tags.set(tag)
            # a.update(title=title)
            # a.update(content=content)
            # a.update(status=status)
            # a.update(pub_time=pub_time)
            # a.update(use_id=pid)
            # a.save()
            return JsonResponse({"tip": "发表成功"})
    return redirect('/login')


def imglook(request):
    return render(request, "imglook.html")


def game_2048(request):
    return render(request, "2048.html")


def retrieve(request):
    if request.method == "POST":
        print(1)
        name = request.POST.get("user")
        pwd = request.POST.get("pwd")
        pwd2 = request.POST.get("pwd2")
        print(pwd, pwd2)
        if pwd == pwd2:
            pwd = make_password(pwd)
            email = request.POST.get("email")
            if name == "":
                return JsonResponse({"tip": "用户名为空"})
            ue = user.objects.filter(user_name=name)
            print(ue)
            if ue != None:
                if ue[0].user_email == email:
                    ue.update(user_name=name, user_paw=pwd)
                    request.session["is_login"] = True
                    request.session["is_user"] = name
                    return JsonResponse({"tip": "修改成功"})
                else:
                    return JsonResponse({"tip": "邮箱错误"})
            else:
                return JsonResponse({"tip": "账号不存在"})
        else:
            return JsonResponse({"tip": "两次密码输入不一致"})
    return render(request, "retrieve.html")



class CBV(View):
    def dispatch(self, request, *args, **kwargs):
        print("进行验证")
        # 'get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace'
        result = super(CBV.self).dispatch(request, *args, **kwargs)
        return result

    def post(self, request):
        pass

    def get(self, request):
        pass