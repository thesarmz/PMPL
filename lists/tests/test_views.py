from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.models import Item, List
from lists.views import home_page


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)


    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html', {'comment': 'yey, waktunya berlibur'})
        self.assertEqual(response.content.decode(), expected_html)

    def test_home_page_displays_comment_if_todolist_is_empty(self):
        #list_ = List.objects.create()
        request = HttpRequest()
        response = home_page(request)
        #response = self.client.get('/lists/%d/' % (list_.id,))

        self.assertEqual(Item.objects.count(),0)
        self.assertIn('yey, waktunya berlibur', response.content.decode())
        #self.assertContains(response, 'yey, waktunya berlibur')

    def test_home_page_displays_comment_if_todolist_is_less_than_5(self):
        list_ = List.objects.create()
        Item.objects.create(text='Itemey 1', list=list_)
        
        #request = HttpRequest()
        #response = home_page(request)
        response = self.client.get('/lists/%d/' % (list_.id,))

        self.assertLess(Item.objects.filter(list_id=list_.id).count(),5)
        #self.assertIn('sibuk tapi santai', response.content.decode())
        self.assertContains(response, 'sibuk tapi santai')

    def test_home_page_displays_comment_if_todolist_is_greater_equal_than_5(self):
        list_ = List.objects.create()
        Item.objects.create(text='Itemey 1', list=list_)
        Item.objects.create(text='Itemey 2', list=list_)
        Item.objects.create(text='Itemey 3', list=list_)
        Item.objects.create(text='Itemey 4', list=list_)
        Item.objects.create(text='Itemey 5', list=list_)

        #request = HttpRequest()
        #response = home_page(request)

        response = self.client.get('/lists/%d/' % (list_.id,))
        self.assertGreaterEqual(Item.objects.filter(list_id=list_.id).count(), 5)
        #self.assertIn('oh tidak', response.content.decode())
        self.assertContains(response, 'oh tidak')

    #def test_home_page_displays_all_list_items(self):
     #   Item.objects.create(text='itemey 1')
      #  Item.objects.create(text='itemey 2')

       # request = HttpRequest()
        #response = home_page(request)

        #self.assertIn('itemey 1', response.content.decode())
        #self.assertIn('itemey 2', response.content.decode())

#class ListViewTest(TestCase):
#         self.assertNotContains(response, 'other list item 1')
#         self.assertNotContains(response, 'other list item 2')


class NewListTest(TestCase):

    def test_saving_a_POST_request(self):
        self.client.post(
            '/lists/new',
            data={'item_text': 'A new list item'}
        )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')


    def test_redirects_after_POST(self):
        response = self.client.post(
            '/lists/new',
            data={'item_text': 'A new list item'}
        )
        new_list = List.objects.first()
        self.assertRedirects(response, '/lists/%d/' % (new_list.id,))

class NewItemTest(TestCase):

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            '/lists/%d/add_item' % (correct_list.id,),
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)


    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            '/lists/%d/add_item' % (correct_list.id,),
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))
