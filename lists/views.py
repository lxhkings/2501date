from django.shortcuts import redirect, render
from lists.models import Item, List


def home_page(request):
    return render(request, 'home.html')


def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    # redirect传递的参数返回适当的URL
    return redirect(f'/lists/{list_.id}/')


def view_list(request, list_id):
    '''
    上一版本的修改
    # 从数据库里获取id=list_id 赋值给list_
    list_ = List.objects.get(id=list_id)
    # 从数据库里获取list=list_第一条数据 赋值给items
    items = Item.objects.filter(list=list_)
    # 将给定的模板与给定的上下文字典组合起来，并返回HttpResponse带有该呈现文本的对象。
    return render(request, 'list.html', {'items': items})
    '''

    list_ = List.objects.get(id=list_id)
    return render(request, 'list.html', {'list': list_})


def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect(f'/lists/{list_.id}/')
