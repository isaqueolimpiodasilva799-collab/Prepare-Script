import requests
import json
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('task_automation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class PrepareScriptBot:
    def __init__(self, config_file='config.json'):
        """Inicializar o bot com configurações"""
        self.config = self.load_config(config_file)
        self.driver = None
        self.session = requests.Session()
        logger.info("Bot inicializado")
    
    def load_config(self, config_file):
        """Carregar configurações do arquivo JSON"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            logger.info(f"Configurações carregadas de {config_file}")
            return config
        except FileNotFoundError:
            logger.error(f"Arquivo {config_file} não encontrado")
            return {}
    
    def setup_driver(self):
        """Configurar Selenium WebDriver"""
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            # Descomente a linha abaixo para modo headless (sem interface gráfica)
            # options.add_argument('--headless')
            
            self.driver = webdriver.Chrome(options=options)
            logger.info("WebDriver configurado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao configurar WebDriver: {e}")
            raise
    
    def login(self, url, username, password):
        """Fazer login na plataforma"""
        try:
            logger.info(f"Tentando fazer login em {url}")
            self.driver.get(url)
            
            # Aguardar campo de email
            email_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "email"))
            )
            email_field.send_keys(username)
            
            # Preencher senha
            password_field = self.driver.find_element(By.ID, "password")
            password_field.send_keys(password)
            
            # Clicar em login
            login_button = self.driver.find_element(By.ID, "login-btn")
            login_button.click()
            
            # Aguardar redirecionamento
            time.sleep(3)
            logger.info("Login realizado com sucesso")
            return True
        except Exception as e:
            logger.error(f"Erro durante login: {e}")
            return False
    
    def access_quiz(self, quiz_id):
        """Acessar um quiz específico"""
        try:
            logger.info(f"Acessando quiz: {quiz_id}")
            quiz_url = f"https://preparasp.jovensgenios.com/quiz/{quiz_id}"
            self.driver.get(quiz_url)
            time.sleep(2)
            logger.info(f"Quiz {quiz_id} acessado")
            return True
        except Exception as e:
            logger.error(f"Erro ao acessar quiz: {e}")
            return False
    
    def fill_answers(self, answers):
        """Preencher respostas no quiz"""
        try:
            logger.info("Preenchendo respostas...")
            
            for question_num, answer in enumerate(answers, 1):
                # Localizar opcoes de resposta
                options = self.driver.find_elements(By.CLASS_NAME, "answer-option")
                
                for option in options:
                    if option.text.strip() == answer:
                        option.click()
                        logger.info(f"Pergunta {question_num}: {answer} selecionada")
                        time.sleep(1)
                        break
            
            logger.info("Todas as respostas foram preenchidas")
            return True
        except Exception as e:
            logger.error(f"Erro ao preencher respostas: {e}")
            return False
    
    def submit_quiz(self):
        """Submeter o quiz"""
        try:
            logger.info("Submetendo quiz...")
            submit_button = self.driver.find_element(By.ID, "submit-btn")
            submit_button.click()
            time.sleep(3)
            logger.info("Quiz submetido com sucesso")
            return True
        except Exception as e:
            logger.error(f"Erro ao submeter quiz: {e}")
            return False
    
    def run_automation(self, quiz_ids):
        """Executar automação completa"""
        try:
            self.setup_driver()
            
            # Credenciais do arquivo .env
            username = os.getenv('PREPARE_USERNAME')
            password = os.getenv('PREPARE_PASSWORD')
            login_url = "https://preparasp.jovensgenios.com/login"
            
            if not self.login(login_url, username, password):
                logger.error("Falha no login")
                return False
            
            # Processar cada quiz
            for quiz_id in quiz_ids:
                if self.access_quiz(quiz_id):
                    answers = self.config.get('quizzes', {}).get(quiz_id, [])
                    if answers:
                        self.fill_answers(answers)
                        self.submit_quiz()
                    else:
                        logger.warning(f"Nenhuma resposta configurada para {quiz_id}")
                
                time.sleep(2)
            
            logger.info("Automação concluída!")
            return True
        
        except Exception as e:
            logger.error(f"Erro geral na automação: {e}")
            return False
        
        finally:
            if self.driver:
                self.driver.quit()
                logger.info("WebDriver fechado")

def main():
    """Função principal"""
    bot = PrepareScriptBot('config.json')
    
    # Quizzes a processar
    quiz_ids = [
        "01a019af-2d8f-776a-9292-33aea2e58986"
    ]
    
    bot.run_automation(quiz_ids)

if __name__ == "__main__":
    main()