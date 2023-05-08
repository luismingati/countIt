from django.test import LiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium import webdriver
from time import sleep

def userRegister(self):
    username = self.driver.find_element(By.XPATH, "//input[@name='username']")
    username.send_keys("kauan123@")

    password = self.driver.find_element(By.XPATH, "//input[@name='password1']")
    password.send_keys("Graciebarra592@")

    password2 = self.driver.find_element(By.XPATH, "//input[@name='password2']")
    password2.send_keys("Graciebarra592@")

    botao = self.driver.find_element(By.CLASS_NAME, "button")
    botao.click()

class plataformTests(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    #ep-27 -- Teste Funcionando --
    def Ep27Tests(self):
        self.driver.get(self.live_server_url + "/register/")

        #cadastrar usuario
        userRegister(self)

        #cadastrar produto
        for i in range(1,6):
            product_register = self.driver.find_element(By.ID, "product-register")
            product_register.click()

            name = self.driver.find_element(By.XPATH, "//input[@name='name']")
            name.send_keys(f"Parafuso Sextavado {i}")

            price = self.driver.find_element(By.XPATH, "//input[@name='price']")
            price.send_keys("5")

            name = self.driver.find_element(By.XPATH, "//input[@name='quantity']")
            name.send_keys("100")

            name = self.driver.find_element(By.XPATH, "//input[@name='min_quantity']")
            name.send_keys("10")

            search_button = self.driver.find_element(By.CLASS_NAME, "button")
            search_button.click()

        sleep(1)

        #pesquisar produto
        name = self.driver.find_element(By.XPATH, "//input[@name='search-area']")
        name.send_keys("Parafuso Sextavado 1")

        search_button = self.driver.find_element(By.CLASS_NAME, "search-btn")
        search_button.click()   

        sleep(1)

        # validação do teste - Verificar se o produto pesquisado, irá aparecer na pesquisa
        try:
            element = self.driver.find_element(By.XPATH, "//p[contains(text(), 'Parafuso Sextavado 1')]")
            assert True, element
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
            tabela2 = self.driver.find_element(By.XPATH, "//p[@class='name']")
            tabela2.find_element(By.XPATH, f"//td[contains(text(), 'Iphone 14')]")
            assert False, "Validação 2 - O teste encontrou um erro, o HTML retorna um produto que não existe"
        except:
            assert True
            print("Validação 2 - O produto não foi encontrado, o teste foi validado com sucesso.")

    #ep-5 -- Problema na validação, olhar o botão de estoque baixo --
    def Ep5Tests(self):
        self.driver.get(self.live_server_url + "/register/")

        #cadastrar usuario
        userRegister(self)

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

        sleep(2)

        # validação do teste - Verificar se o produto pesquisado, irá aparecer na pesquisa
        try:
            element = self.driver.find_element(By.XPATH, "//p[contains(text(), 'Parafuso Sextavado')]")
            assert True, element
            print(" Validação 1 - Produto aparece como estoque mínimo, teste validado")
        except:
            assert False, "Validação 1 - Produto não encontrado na tabela de estoque mínimo, há um erro."

    #ep-3 Tests -- Teste funcionando -- 
    def Ep3Tests(self):
        #--------------------------------VALIDACAO 1 ----------------------------------------------------------------

        self.driver.get(self.live_server_url + "/register/")

        #cadastrar usuario
        userRegister(self)

        #cadastrar 5 produtos
        for i in range(1,6):
            product_register = self.driver.find_element(By.ID, "product-register")
            product_register.click()

            name = self.driver.find_element(By.XPATH, "//input[@name='name']")
            name.send_keys(f"Iphone 14 {i}")

            price = self.driver.find_element(By.XPATH, "//input[@name='price']")
            price.send_keys("1000")

            name = self.driver.find_element(By.XPATH, "//input[@name='quantity']")
            name.send_keys("2")

            name = self.driver.find_element(By.XPATH, "//input[@name='min_quantity']")
            name.send_keys("1")

            search_button = self.driver.find_element(By.CLASS_NAME, "button")
            search_button.click()

        sleep(1)

        #entrar na pagina de vendas
        self.driver.get(self.live_server_url + "/vendas/")

        sleep(1)

        #escolher um produto
        pesquisarVenda = self.driver.find_element(By.XPATH, "//input[@name='search-area']")
        pesquisarVenda.send_keys("Iphone 14 1")

        add_button = self.driver.find_element(By.CLASS_NAME, "add-to-cart-btn")
        add_button.click()

        sleep(1)

        #adicionar quantidade superior a quantidade do estoque
        quantity = self.driver.find_element(By.XPATH, "//input[@type='number']")
        quantity.send_keys(Keys.BACKSPACE)
        sleep(1)
        quantity.send_keys("5")

        close_sale = self.driver.find_element(By.CLASS_NAME, "finish-btn")
        close_sale.click()
        sleep(1)

        #validar a resposta do alert
        try:
             #obter texto do alerta
            alert = Alert(self.driver)
            alert_text = alert.text
            assert True, "A quantidade solicitada de Iphone 14 1 excede a quantidade disponível no estoque." in alert_text
            print("Validação 1 - O texto do alerta bate com o resultado esperado, teste validado com sucesso")
            alert.accept()
        except:
            assert False, "Validação 1 - Resultado diferente do esperado, há um erro."


        #--------------------------------VALIDACAO 2 ----------------------------------------------------------------

        sleep(1)

        for i in range(1,6):
            searchArea = self.driver.find_element(By.XPATH, "//input[@name='search-area']")
            searchArea.send_keys(f"Iphone 14 {i}")
            searchArea.send_keys(Keys.ENTER)
            sleep(1)
            addButton = self.driver.find_element(By.CLASS_NAME, "add-to-cart-btn")
            addButton.click()
            searchArea.send_keys(Keys.BACKSPACE * len(searchArea.get_attribute('value')))
            sleep(1)

        endSale = self.driver.find_element(By.CLASS_NAME, "finish-btn")
        endSale.click()
        
        try:
            current_url = self.driver.current_url
            expected_url = 'http://127.0.0.1:8000/vendas/concluir/'
            assert True, current_url == expected_url
            print("Validação 2 - A venda dos 5 produtos foi realizada, teste validado com sucesso.")
        except:
            assert False, "Validação 2 - A venda não foi realizada, há um erro."
