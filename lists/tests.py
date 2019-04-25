from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item


from lists.views import home_page
# Create your tests here.


class HomePageTest(TestCase):

    # def test_root_url_resolves_to_home_page_view(self):
    #     found=resolve('/')
    #     self.assertEqual(found.func,home_page)

    # def test_home_page_returns_correct_htmL(self):
    #     # request=HttpRequest()
    #     # response=home_page(request)
    #     response=self.client.get('/')           #检测的原生方式
    #     html=response.content.decode('utf-8')
    #
    #     expected_html=render_to_string('home.html') #测试是否正确渲染模板，然后与视图返回的结果做对比 自定义检测，万能模式
    #     self.assertEqual(html,expected_html)
    #
    #     self.assertTrue(html.startswith('<html>'))
    #     self.assertIn('<title>To-Do lists</title>',html)
    #     self.assertTrue(html.strip().endswith('</html>'))
    #
    #     self.assertTemplateUsed(response,'home.html') #测试是否正确渲染模板，然后与视图返回的结果做对比   检测的原生方式
    #
    #     self.assertEqual(response,'wrong.html')
    #
    def test_users_home_template(self):
        response=self.client.get('/')
        self.assertTemplateUsed(response,'home.html')
    def test_can_save_a_POST_request(self):
        response=self.client.post('/',data={'item_text':'A new list item'})

        self.assertEqual(Item.objects.count(),1)#检查是否把一个新的item对象存入数据库，
        # object.count（）是object.all（）.count（）的简写模式
        new_item=Item.objects.first()#object.first（）等价于object.all()[0]
        self.assertEqual(new_item,'A new list item')#检查待办事项的文本是否正确

        self.assertIn('A new list item',response.content.decode())
        self.assertTemplateUsed(response,'home.html')

    def test_only_saves_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(),0)



class  ItemModelTest(TestCase):
    def test_saving_and_retrieving_item(self):
        first_item=Item()
        first_item.text='The first (ever) list item'
        first_item.save()

        second_item=Item()
        second_item.text='Item the second'
        second_item.save()

        saved_items=Item.objects.all()
        self.assertEqual(saved_items.count(),2)

        first_saved_item=saved_items[0]
        second_saved_item=saved_items[1]
        self.assertEqual(first_saved_item.text,'The first (ever) list item')
        self.assertEqual(second_item.text,'Item the second')

