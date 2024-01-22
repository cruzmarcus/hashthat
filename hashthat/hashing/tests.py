import hashlib
import time

from django.core.exceptions import ValidationError
from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By

from .forms import HashForm
from .models import Hash


class FunctionalTestCase(TestCase):
    def setUp(self) -> None:
        self.browser = webdriver.Chrome()


    def tearDown(self) -> None:
        self.browser.quit()

    def test_there_is_homepage(self):
        self.browser.get("http://localhost:8000/")
        self.assertIn("Enter hash here:", self.browser.page_source)

    def test_hash_of_hello_text(self):
        self.browser.get("http://localhost:8000/")
        text = self.browser.find_element(By.ID, "id_text")
        text.send_keys("hello")
        self.browser.find_element(By.NAME, "submit").click()

        self.assertIn(
            "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824",
            self.browser.page_source
        )

    def test_hash_ajax(self):
        self.browser.get("http://localhost:8000/")
        text = self.browser.find_element(By. ID,"id_text")
        text.send_keys("hello")
        
        time.sleep(2) # Wait for AJAX
        
        self.assertIn(
            "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824",
            self.browser.page_source
        )



class UnitTestCase(TestCase):
    def test_home_homepage_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "hashing/home.html")

    def test_hash_form(self):
        form = HashForm(data={"text": "hello"})
        self.assertTrue(form.is_valid())

    def test_hash_text_successfully(self):
        text_hashed = hashlib.sha256("hello".encode("utf-8")).hexdigest()
        self.assertEqual(
            "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824",
            text_hashed,
        )

    def save_hash(self):
        hash = Hash()
        hash.text = "hello"
        hash.hash = "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
        hash.save()
        return hash

    def test_hash_object(self):
        hash = self.save_hash()
        pulled_hash = Hash.objects.get(
            hash="2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
        )

        self.assertEqual(hash.text, pulled_hash.text)
        self.assertEqual(hash.hash, pulled_hash.hash)

    def test_viewing_hash(self):
        _ = self.save_hash()
        response = self.client.get(
            "/hash/2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
        )
        self.assertContains(response, "hello")

    def test_bad_data(self):
        def bad_hash():
            hash = Hash()
            hash.hash = "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824xxxx"
            hash.full_clean()
        
        self.assertRaises(ValidationError, bad_hash)