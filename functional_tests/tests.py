from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from django.test import LiveServerTestCase
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10




class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        # 自动测试工具
        self.browser = webdriver.Firefox()

    def tearDown(self):
        # 调用wedbriver.Firefox()方法退出浏览器
        self.browser.quit()

    # 等待列表中的行
    def wait_for_row_in_list_table(self, row_text):
        # 获取当前时间
        start_time = time.time()
        # 死循环
        while True:
            try:
                # 通过id定位元素 id_list_table
                table = self.browser.find_element_by_id('id_list_table')
                # 通过标签定位tr获取里面内容保存为rows列表
                rows = table.find_elements_by_tag_name('tr')
                # 函数传入的row_text在rows列表里面。用循环判断
                self.assertIn(row_text, [row.text for row in rows])
                return
            # 断言语句（assert）失败
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

        # 测试可以为一个用户启动一个列表
    def test_can_start_a_list_for_one_user(self):
        # Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage
        # get方法打开django测试页面
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention to-do lists
        # 判断'To-Do'在主页标签里面
        self.assertIn('To-Do', self.browser.title)
        # 获取标签h1里面的text内容传给header_text
        header_text = self.browser.find_element_by_tag_name('h1').text
        # 判断To-Do在header_text里面
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away
        # 获取id为id_new_item的内容传给inputbox
        inputbox = self.browser.find_element_by_id('id_new_item')
        # get_attribute获取属性,即input的默认输入内容是否相等
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # She types "Buy peacock feathers" into a text box (Edith's hobby
        # is tying fly-fishing lures)
        inputbox.send_keys('Buy peacock feathers')

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list table
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly" (Edith is very
        # methodical)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on her list
        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # Satisfied, she goes back to sleep

        # 测试多个用户可以在不同的网址上开始列表
    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Edith starts a new to-do list
        # get方式打开当前主页
        self.browser.get(self.live_server_url)
        # 获取id为id_new_item的内容传给inputbox
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # She notices that her list has a unique URL
        # 获取当前网址
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        # Now a new user, Francis, comes along to the site.

        ## We use a new browser session to make sure that no information
        ## of Edith's is coming through from cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Francis visits the home page.  There is no sign of Edith's

        # get方法打开django测试页面
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # Francis starts a new list by entering a new item. He
        # is less interesting than Edith...
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Again, there is no trace of Edith's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        # Satisfied, they both go back to sleep
