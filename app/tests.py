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
        self.driver.get(self.live_server_url + "/estoque/")

        # Localiza o campo do formulário e insere um valor
        username = self.driver.find_element(By.XPATH, "//input[@name='username']")
        username.send_keys("kauan123@")

        password = self.driver.find_element(By.XPATH, "//input[@name='password']")
        password.send_keys("Graciebarra592@")

        # Localiza o botão e clica nele
        botao = self.driver.find_element(By.ID, "click_login")
        botao.click()

        # Aguarda 2 segundos para que a página seja atualizada após o clique no botão
        sleep(2)

        search = self.driver.find_element(By.XPATH, "//input[@name='search-area']")
        search.send_keys("Parafuso Sextavado")

        search_button = self.driver.find_element(By.CLASS_NAME, "search-btn")
        search_button.click()

        sleep(5)

        try:
            tabela = self.driver.find_element(By.XPATH, "//table[@class='content-table']")
            tabela.find_element(By.XPATH, f"//td[contains(text(), 'Parafuso Sextavado')]")
            assert True
        except:
            assert False, "Produto não encontrado na tabela"

