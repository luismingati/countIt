from django.test import LiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from collections import Counter
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

def registerProduct(self,iterator):
    self.driver.get(self.live_server_url + "/estoque/cadastro/")

    name = self.driver.find_element(By.XPATH, "//input[@name='name']")
    name.send_keys(f"Iphone 14 {iterator}")

    price = self.driver.find_element(By.XPATH, "//input[@name='price']")
    price.send_keys("14000")

    quantity = self.driver.find_element(By.XPATH, "//input[@name='quantity']")
    quantity.send_keys("10")

    min_quantity = self.driver.find_element(By.XPATH, "//input[@name='min_quantity']")
    min_quantity.send_keys("1")

    select_element = self.driver.find_element(By.XPATH, "//select[@id='id_category']")
    select = Select(select_element)
    select.select_by_visible_text("Telefones")

    button = self.driver.find_element(By.CLASS_NAME, "button")
    button.click()

def createCategory(self,name):
    self.driver.get(self.live_server_url + "/createCategory/")

    category_name = self.driver.find_element(By.XPATH, "//input[@name='name']")
    category_name.send_keys(f"{name}")
    
    category_button = self.driver.find_element(By.CLASS_NAME, "create-category")
    category_button.click()

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

    def test_27_vd1(self):
        # Verifica se um produto que existe no estoque aparece no HTML
        self.driver.get(self.live_server_url + "/register/")

        #cadastrar usuario
        userRegister(self)

        #criar categoria
        createCategory(self, "Telefones")

        #cadastrar produto
        for i in range(1,6):
            registerProduct(self, i)

        sleep(1)

        #pesquisar produto
        name = self.driver.find_element(By.XPATH, "//input[@name='search-area']")
        name.send_keys("Iphone 14 1")

        search_button = self.driver.find_element(By.CLASS_NAME, "search-btn")
        search_button.click()   

        sleep(1)

        # validação do teste - Verificar se o produto pesquisado, irá aparecer na pesquisa
        try:
            element = self.driver.find_element(By.XPATH, "//p[contains(text(), 'Iphone 14 1')]")
            assert True, element
            print(" Validação 1 - Produto encontrado na tabela, validação realizada com sucesso.")
        except:
            assert False, "Validação 1 - Produto não encontrado na tabela."

    def test_27_vd2(self):
        # Teste para verificar o HTML Retorna um produto que já existe
        self.driver.get(self.live_server_url + "/register/")

        #cadastrar usuario
        userRegister(self)

        #cadastra categoria
        createCategory(self, "Telefones")

        #cadastrar produto
        for i in range(1,6):
            registerProduct(self, i)

        sleep(1)

        #pesquisar produto
        name = self.driver.find_element(By.XPATH, "//input[@name='search-area']")
        name.send_keys("Iphone 14 1")

        search_button = self.driver.find_element(By.CLASS_NAME, "search-btn")
        search_button.click()   

        sleep(1)
        
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

    def test_5(self):
        # Verifica se produtos com estoque mínimo irão ser retornados quando forem solicitados
        self.driver.get(self.live_server_url + "/register/")

        #cadastrar usuario
        userRegister(self)

        #cadastrar categoria
        createCategory(self, "Telefones")

        #cadastrar produto com a quantidade minima igual a quantidade
        self.driver.get(self.live_server_url + "/estoque/cadastro/")

        name = self.driver.find_element(By.XPATH, "//input[@name='name']")
        name.send_keys("Iphone 14")

        price = self.driver.find_element(By.XPATH, "//input[@name='price']")
        price.send_keys("14000")

        quantity = self.driver.find_element(By.XPATH, "//input[@name='quantity']")
        quantity.send_keys("1")

        min_quantity = self.driver.find_element(By.XPATH, "//input[@name='min_quantity']")
        min_quantity.send_keys("10")

        sleep(5)

        select_element = self.driver.find_element(By.XPATH, "//select[@id='id_category']")
        select = Select(select_element)
        select.select_by_visible_text("Telefones")

        button = self.driver.find_element(By.CLASS_NAME, "button")
        button.click()


        sleep(2)

        #cadastrar produto com a quantidade superior a quantidade mínima
        registerProduct(self, 1)

        #clicar em estoque minimo
        search_button = self.driver.find_element(By.ID, "toggle-low-stock-btn")
        search_button.click()

        sleep(2)

        # validação do teste - Verificar se o produto pesquisado, irá aparecer na pesquisa
        try:
            element = self.driver.find_element(By.XPATH, "//p[contains(text(), 'Iphone 14')]")
            assert True, element
            print(" Validação 1 - Produto aparece como estoque mínimo, teste validado")
        except:
            assert False, "Validação 1 - Produto não encontrado na tabela de estoque mínimo, há um erro."

    def test_3_vd1(self):
        # Verifica se consegue vender uma quantidade de produtos maior que a do estoque
        self.driver.get(self.live_server_url + "/register/")

        #cadastrar usuario
        userRegister(self)

        #cadastrar categoria
        createCategory(self, "Telefones")

        #cadastrar 5 produtos
        for i in range(1,6):
            registerProduct(self, i)

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
        quantity.send_keys("11")

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
            
    def test_3_vd2(self):
        self.driver.get(self.live_server_url + "/register/")

        #cadastrar usuario
        userRegister(self)

        createCategory(self, "Telefones")

        #cadastrar 5 produtos
        for i in range(1,6):
            registerProduct(self, i)

        sleep(1)

        #entrar na pagina de vendas
        self.driver.get(self.live_server_url + "/vendas/")

        sleep(1)

        #Pesquisar 5 produtos
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

    #Entrega 4#

    def test_14_vd1(self):

        self.driver.get(self.live_server_url + "/register/")

        self.driver.refresh()

        userRegister(self)

        createCategory(self,"Telefones")

        registerProduct(self,1)

        self.driver.get(self.live_server_url + "/vendas/")

        add_product_cart = self.driver.find_element(By.CLASS_NAME, "add-to-cart-btn")
        add_product_cart.click()

        discount = self.driver.find_element(By.XPATH, "//input[@name='discount']")
        discount.send_keys("101")

        finish_sale =  self.driver.find_element(By.CLASS_NAME, "finish-btn")
        finish_sale.click()

        try:
            current_url = self.driver.current_url
            expected_url = 'http://127.0.0.1:8000/vendas/concluir/'
            assert True, current_url != expected_url
            print("O produto não foi vendido, teste validado.")
        except:
            assert False, "A venda foi realizada, há um erro."

    def test_14_vd2(self):
        self.driver.get(self.live_server_url + "/register/")

        self.driver.refresh()

        userRegister(self)

        createCategory(self,"Telefones")

        registerProduct(self,1)

        self.driver.get(self.live_server_url + "/vendas/")

        add_product_cart = self.driver.find_element(By.CLASS_NAME, "add-to-cart-btn")
        add_product_cart.click()

        discount = self.driver.find_element(By.XPATH, "//input[@name='discount']")
        discount.send_keys("-10")

        finish_sale =  self.driver.find_element(By.CLASS_NAME, "finish-btn")
        finish_sale.click()

        try:
            current_url = self.driver.current_url
            expected_url = 'http://127.0.0.1:8000/vendas/concluir/'
            assert True, current_url != expected_url
            print("O produto não foi vendido, teste validado.")
        except:
            assert False, "A venda foi realizada, há um erro."
    
    def test_14_vd3(self):
        self.driver.get(self.live_server_url + "/register/")

        self.driver.refresh()

        userRegister(self)

        createCategory(self,"Telefones")

        registerProduct(self,1)

        self.driver.get(self.live_server_url + "/vendas/")

        add_product_cart = self.driver.find_element(By.CLASS_NAME, "add-to-cart-btn")
        add_product_cart.click()

        discount = self.driver.find_element(By.XPATH, "//input[@name='discount']")
        discount.send_keys("10")

        finish_sale =  self.driver.find_element(By.CLASS_NAME, "finish-btn")
        finish_sale.click()

        try:
            current_url = self.driver.current_url
            expected_url = 'http://127.0.0.1:8000/vendas/concluir/'
            price_element = self.driver.find_element(By.XPATH, "//td[@class='final-price' and contains(text(), '12600')]")
            assert True, current_url == expected_url and price_element
            print("O produto foi vendido e o desconto está correto, teste validado.")
        except:
            assert False, "Há um erro."

    def test_29_vd1(self):
        self.driver.get(self.live_server_url + "/register/")

        self.driver.refresh()

        userRegister(self)

        createCategory(self,"Telefones")

        select_element = self.driver.find_element(By.XPATH, "//select[@id='id_category']")
        select = Select(select_element)
        select.select_by_visible_text("Telefones")

        sleep(10)

        try:
            select_element = self.driver.find_element(By.ID, "id_category")
            selected_option = select_element.find_element(By.XPATH, f"./option[text()='Telefones']")
            assert selected_option
            print("In select tag exists the option 'Telefones'. Test validated.")
        except AssertionError:
            print("There is an error.")
    
    def test_29_vd2(self):
        self.driver.get(self.live_server_url + "/register/")

        self.driver.refresh()

        userRegister(self)

        createCategory(self,"Telefones")

        for i in range(0,2):
            registerProduct(self, i)

        try:
            category_elements = self.driver.find_elements(By.CSS_SELECTOR, "p.category")
            
            for category_element in category_elements:
                if category_element.text != "Telefones":
                    raise AssertionError("Not all categories have the text 'Telefones'")
            
            print("All categories have the text 'Telefones'. Test validated.")
        except AssertionError as e:
            print(str(e))
    ##refatorar
    def test_29_vd3(self):
        self.driver.get(self.live_server_url + "/register/")
        self.driver.refresh()

        userRegister(self)

        for i in range(0,2):
            createCategory(self,"Telefones")
        
        try:
            select_element = self.driver.find_element(By.XPATH, "//select[@id='id_category']")
            options = select_element.find_elements(By.TAG_NAME, "option")
            option_names = [option.text for option in options]

            duplicate_options = [name for name, count in Counter(option_names).items() if count > 1]

            if len(duplicate_options) == 0:
                print("No duplicate options found in the select element. Test validated")
            else:
                print(f"Duplicate options found: {', '.join(duplicate_options)}, There is an error.")
        except NoSuchElementException:
            print("Select element not found.")

    #FALTA FAZER
    # def Test_2_vd1(self):
    #     ...

    # def Test_2_vd2(self):
    #     ...

    # def Test_2_vd3(self):
        ...