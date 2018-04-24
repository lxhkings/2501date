from django.test import TestCase
from lists.models import Item, List

class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

class ListAndItemModelsTest(TestCase):

        # 测试保存和检索项目
    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()

        save_list = List.objects.first()
        self.assertEqual(save_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, list_)


    def test_displays_all_items(self):
        list_ = List.objects.create()
        Item.objects.create(text='itemey 1', list=list_)
        Item.objects.create(text='itemey 2', list=list_)

class NewListTest(TestCase):

    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')


    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')

class ListViewTest(TestCase):

        # 测试使用列表模板
    def test_uses_list_template(self):

        # 实例化List创建数据库。然后赋值给list
        list_ = List.objects.create()
        # response反应,客户端以get方式打开/lists/{list_.id}
        response = self.client.get(f'/lists/{list_.id}/')
        # 模版是否存在断定
        self.assertTemplateUsed(response, 'list.html')

        # 测试只显示项目列表
    def test_displays_only_items_for_that_list(self):

        # 实例化List创建数据库。然后赋值给correct_list(正确列表)
        correct_list = List.objects.create()
        # 数据库中插入
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)
        # # 实例化List创建数据库。然后赋值给other list(其它列表)
        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)

        # 客户端打开连接/lists/正确列表ID 获取 给(响应)pesponse
        response = self.client.get(f'/lists/{correct_list.id}/')

        # assertContains
        # 声明一个Response实例产生了给定的status_code(HTML状态码，默认200)并且text出现在响应的内容中。
        # 如果count提供，text必须count在响应中准确发生时间。
        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')

        # 断言Response实例产生了给定的内容status_code，text并且不会出现在响应的内容中。
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')

        # 测试通过正确的列表模板
    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')

        # response.context代表我们将要传递给渲染函数的上下文
        self.assertEqual(response.context['list'], correct_list)

        # print('\n')
        # print('---------开始------------')
        # print(response)
        # print(response.context['list'])
        # print('---------结束------------')

class NewItemTest(TestCase):

        # 测试可以保存一个POST请求到现有的列表
    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        # 客户端以POST方式打开连接
        self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': 'A new item for an existing list'}
        )

        # 判断是否相等
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': 'A new item for an existing list'}
        )
        # print('\n')
        # print('---------开始------------')
        # print(response)
        # print('---------结束------------')

        self.assertRedirects(response, f'/lists/{correct_list.id}/')

        # self.fail('通过')


