#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PREPARE SCRIPT - Automação Completa
Tudo em um único arquivo!
"""

import requests
import json
import time
import logging
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

# ═══════════════════════════════════════════════════════════════
# CONFIGURAÇÃO - EDITE AQUI!
# ═══════════════════════════════════════════════════════════════

EMAIL = "seu_email@email.com"  # 👈 COLOQUE SEU EMAIL AQUI
SENHA = "sua_senha_aqui"       # 👈 COLOQUE SUA SENHA AQUI

# Seus quizzes - ADICIONE QUANTOS QUISER
QUIZZES = {
    # Exemplo 1:
    "quiz_1": {
        "id": "01a019af-2d8f-776a-9292-33aea2e58986",  # 👈 ID DO QUIZ
        "respostas": ["A", "B", "C", "D", "A"]        # 👈 SUAS RESPOSTAS
    },
    # Exemplo 2 (descomente para adicionar):
    # "quiz_2": {
    #     "id": "outro-id-aqui",
    #     "respostas": ["Opção 1", "Opção 2", "Opção 3"]
    # },
}

# ═══════════════════════════════════════════════════════════════
# ⚙️ CONFIGURAÇÕES AVANÇADAS (NÃO ALTERE SE NÃO SOUBER)
# ═══════════════════════════════════════════════════════════════

PLATAFORMA_URL = "https://preparasp.jovensgenios.com"
LOGIN_URL = f"{PLATAFORMA_URL}/login"
TIMEOUT = 10
ESPERA_ENTRE_RESPOSTAS = 1
MODO_HEADLESS = False  # False = mostra navegador | True = esconde

# ═════════════════════════════════════════════════════════════��═
# 🤖 CLASSE DE AUTOMAÇÃO
# ═══════════════════════════════════════════════════════════════

class PrepareScriptBot:
    def __init__(self):
        self.driver = None
        self.logger = self._setup_logging()
        self.logger.info("🚀 Bot iniciado!")
    
    def _setup_logging(self):
        """Configurar sistema de logs"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('prepare_script.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    
    def setup_driver(self):
        """Inicializar Selenium WebDriver"""
        try:
            self.logger.info("⚙️ Configurando WebDriver...")
            options = webdriver.ChromeOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            
            if MODO_HEADLESS:
                options.add_argument('--headless')
            
            self.driver = webdriver.Chrome(options=options)
            self.logger.info("✅ WebDriver pronto!")
            return True
        except Exception as e:
            self.logger.error(f"❌ Erro ao configurar WebDriver: {e}")
            return False
    
    def login(self):
        """Fazer login na plataforma"""
        try:
            self.logger.info(f"🔐 Conectando em {LOGIN_URL}...")
            self.driver.get(LOGIN_URL)
            
            # Esperar campo de email
            email_field = WebDriverWait(self.driver, TIMEOUT).until(
                EC.presence_of_element_located((By.ID, "email"))
            )
            email_field.send_keys(EMAIL)
            self.logger.info("📧 Email preenchido")
            
            # Preencher senha
            senha_field = self.driver.find_element(By.ID, "password")
            senha_field.send_keys(SENHA)
            self.logger.info("🔑 Senha preenchida")
            
            # Clicar em login
            login_btn = self.driver.find_element(By.ID, "login-btn")
            login_btn.click()
            self.logger.info("⏳ Aguardando login...")
            
            time.sleep(3)
            self.logger.info("✅ Login realizado com sucesso!")
            return True
        except Exception as e:
            self.logger.error(f"❌ Erro no login: {e}")
            return False
    
    def acessar_quiz(self, quiz_id):
        """Acessar um quiz específico"""
        try:
            url_quiz = f"{PLATAFORMA_URL}/quiz/{quiz_id}"
            self.logger.info(f"📚 Acessando quiz: {quiz_id}")
            self.driver.get(url_quiz)
            time.sleep(2)
            self.logger.info("✅ Quiz carregado!")
            return True
        except Exception as e:
            self.logger.error(f"❌ Erro ao acessar quiz: {e}")
            return False
    
    def preencher_respostas(self, respostas):
        """Preencher as respostas"""
        try:
            self.logger.info("✍️ Preenchendo respostas...")
            
            for num, resposta in enumerate(respostas, 1):
                opcoes = self.driver.find_elements(By.CLASS_NAME, "answer-option")
                
                for opcao in opcoes:
                    if opcao.text.strip() == resposta:
                        opcao.click()
                        self.logger.info(f"   Pergunta {num}: '{resposta}' selecionada ✓")
                        time.sleep(ESPERA_ENTRE_RESPOSTAS)
                        break
            
            self.logger.info(f"✅ Todas as {len(respostas)} respostas preenchidas!")
            return True
        except Exception as e:
            self.logger.error(f"❌ Erro ao preencher respostas: {e}")
            return False
    
    def submeter_quiz(self):
        """Submeter o quiz"""
        try:
            self.logger.info("🚀 Submetendo quiz...")
            botao_submit = self.driver.find_element(By.ID, "submit-btn")
            botao_submit.click()
            time.sleep(3)
            self.logger.info("✅ Quiz submetido com sucesso!")
            return True
        except Exception as e:
            self.logger.error(f"❌ Erro ao submeter: {e}")
            return False
    
    def executar_tudo(self):
        """Executar automação completa"""
        try:
            if not self.setup_driver():
                return False
            
            if not self.login():
                return False
            
            # Processar cada quiz
            for nome_quiz, config in QUIZZES.items():
                self.logger.info(f"\n{'='*50}")
                self.logger.info(f"Processando: {nome_quiz}")
                self.logger.info(f"{'='*50}")
                
                quiz_id = config["id"]
                respostas = config["respostas"]
                
                if self.acessar_quiz(quiz_id):
                    if self.preencher_respostas(respostas):
                        self.submeter_quiz()
                
                time.sleep(2)
            
            self.logger.info("\n" + "="*50)
            self.logger.info("🎉 AUTOMAÇÃO CONCLUÍDA COM SUCESSO!")
            self.logger.info("="*50)
            return True
        
        except Exception as e:
            self.logger.error(f"Erro geral: {e}")
            return False
        
        finally:
            if self.driver:
                self.driver.quit()
                self.logger.info("🔌 Navegador fechado")

# ═══════════════════════════════════════════════════════════════
# 🎯 EXECUTAR
# ═══════════════════════════════════════════════════════════════

def main():
    print("\n" + "="*60)
    print("  🚀 PREPARE SCRIPT - AUTOMAÇÃO DE TAREFAS")
    print("="*60)
    print(f"📧 Email: {EMAIL}")
    print(f"🎯 Quizzes a processar: {len(QUIZZES)}")
    print("="*60 + "\n")
    
    # Validações
    if EMAIL == "seu_email@email.com" or SENHA == "sua_senha_aqui":
        print("❌ ERRO: Configure seu email e senha no topo do arquivo!")
        print("   Edite as linhas:")
        print("   - EMAIL = 'seu_email@email.com'")
        print("   - SENHA = 'sua_senha_aqui'")
        sys.exit(1)
    
    if not QUIZZES:
        print("❌ ERRO: Configure pelo menos um quiz!")
        sys.exit(1)
    
    # Executar
    bot = PrepareScriptBot()
    sucesso = bot.executar_tudo()
    
    if not sucesso:
        print("\n⚠️ Verifique o arquivo 'prepare_script.log' para detalhes")
        sys.exit(1)

if __name__ == "__main__":
    main()
