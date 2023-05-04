from django.test import LiveServerTestCase
from selenium.webdriver.common.by import By
from selenium import webdriver
from time import sleep

class ep27_tests(LiveServerTestCase):
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

        # validação do teste - Verificar se o produto pesquisado, irá aparecer na pesquisa
        try:
            tabela = self.driver.find_element(By.XPATH, "//table[@class='content-table']")
            tabela.find_element(By.XPATH, f"//td[contains(text(), 'Parafuso Sextavado')]")
            assert True
            print(" Validação 1 - Produto encontrado na tabela, validação realizada com sucesso.")
        except:
            assert False, "Validação 1 - Produto não encontrado na tabela."

        #teste para verificar se irá aparecer um produto que não existe
        product_error = self.driver.find_element(By.XPATH, "//input[@name='search-area']")
        product_error.send_keys("Iphone 14")

        search_button = self.driver.find_element(By.CLASS_NAME, "search-btn")
        search_button.click()   

        #resultado da segunda validação
        try:
            tabela2 = self.driver.find_element(By.XPATH, "//table[@class='content-table']")
            tabela2.find_element(By.XPATH, f"//td[contains(text(), 'Iphone 14')]")
            assert False, "Validação 2 - O este encontrou um erro, o HTML retorna um produto que não existe"
        except:
            assert True
            print("Validação 2 - O produto não foi encontrado, o teste foi validado com sucesso.")







class ep5_tests(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def estoqueMinimo(self):
        ...








class ep3_tests(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def estoqueMinimo(self):
        self.driver.get(self.live_server_url + "/register/")

        username = self.driver.find_element(By.XPATH, "//input[@name='username']")
        username.send_keys("kauan123@")

        password = self.driver.find_element(By.XPATH, "//input[@name='password1']")
        password.send_keys("Graciebarra592@")

        password2 = self.driver.find_element(By.XPATH, "//input[@name='password2']")
        password2.send_keys("Graciebarra592@")

        botao = self.driver.find_element(By.CLASS_NAME, "button")
        botao.click()

        sleep(2)

        #cadastrar produto com a quantidade minima igual a quantidade
        product_register = self.driver.find_element(By.ID, "product-register")
        product_register.click()

        name = self.driver.find_element(By.XPATH, "//input[@name='name']")
        name.send_keys("Parafuso Sextavado")

        price = self.driver.find_element(By.XPATH, "//input[@name='price']")
        price.send_keys("5")

        name = self.driver.find_element(By.XPATH, "//input[@name='quantity']")
        name.send_keys("10")

        name = self.driver.find_element(By.XPATH, "//input[@name='min_quantity']")
        name.send_keys("10")

        search_button = self.driver.find_element(By.CLASS_NAME, "button")
        search_button.click()

        sleep(2)

        #cadastrar produto com a quantidade superior a quantidade mínima
        product_register = self.driver.find_element(By.ID, "product-register")
        product_register.click()

        name = self.driver.find_element(By.XPATH, "//input[@name='name']")
        name.send_keys("Iphone 14")

        price = self.driver.find_element(By.XPATH, "//input[@name='price']")
        price.send_keys("1000")

        name = self.driver.find_element(By.XPATH, "//input[@name='quantity']")
        name.send_keys("10")

        name = self.driver.find_element(By.XPATH, "//input[@name='min_quantity']")
        name.send_keys("1")

        search_button = self.driver.find_element(By.CLASS_NAME, "button")
        search_button.click()

        sleep(2)

        #clicar em estoque minimo
        search_button = self.driver.find_element(By.ID, "toggle-low-stock-btn")
        search_button.click()
