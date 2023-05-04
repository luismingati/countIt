from django.test import LiveServerTestCase
from selenium.webdriver.common.by import By
from selenium import webdriver
from time import sleep

class MySeleniumTests(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_search_product(self):
        self.driver.get(self.live_server_url + "/register/")

        #cadastrar usuario
        username = self.driver.find_element(By.XPATH, "//input[@name='username']")
        username.send_keys("kauan123@")

        password = self.driver.find_element(By.XPATH, "//input[@name='password1']")
        password.send_keys("Graciebarra592@")

        password2 = self.driver.find_element(By.XPATH, "//input[@name='password2']")
        password2.send_keys("Graciebarra592@")

        botao = self.driver.find_element(By.CLASS_NAME, "button")
        botao.click()

        sleep(2)

        #cadastrar produto
        product_register = self.driver.find_element(By.ID, "product-register")
        product_register.click()

        name = self.driver.find_element(By.XPATH, "//input[@name='name']")
        name.send_keys("Parafuso Sextavado")

        price = self.driver.find_element(By.XPATH, "//input[@name='price']")
        price.send_keys("5")

        name = self.driver.find_element(By.XPATH, "//input[@name='quantity']")
        name.send_keys("100")

        name = self.driver.find_element(By.XPATH, "//input[@name='min_quantity']")
        name.send_keys("10")

        search_button = self.driver.find_element(By.CLASS_NAME, "button")
        search_button.click()

        sleep(2)

        #pesquisar produto
        name = self.driver.find_element(By.XPATH, "//input[@name='search-area']")
        name.send_keys("Parafuso Sextavado")

        search_button = self.driver.find_element(By.CLASS_NAME, "search-btn")
        search_button.click()   

        sleep(2)

        # validação do teste
        try:
            tabela = self.driver.find_element(By.XPATH, "//table[@class='content-table']")
            tabela.find_element(By.XPATH, f"//td[contains(text(), 'Parafuso Sextavado')]")
            assert True
            print("Produto encontrado na tabela, validação realizada com sucesso.")
        except:
            assert False, "Produto não encontrado na tabela."

