#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PREPARE SCRIPT - Automação Completa com RA
Script que faz login com RA e automação completa!
"""

import requests
import json
import time
import logging
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

# ═══════════════════════════════════════════════════════════════
# ⚙️ CONFIGURAÇÕES
# ═══════════════════════════════════════════════════════════════

# 📋 SEUS DADOS
RA = "00001203274324"
SENHA = "Aa12345!"

# 🌐 PLATAFORMA
PLATAFORMA_URL = "https://preparasp.jovensgenios.com"
LOGIN_URL = f"{PLATAFORMA_URL}/login"
CURSOS_URL = f"{PLATAFORMA_URL}/cursos"

# ⏱️ TIMINGS
TIMEOUT = 15
ESPERA_ENTRE_RESPOSTAS = 1.5
MODO_HEADLESS = False  # False = mostra navegador | True = esconde

# ═══════════════════════════════════════════════════════════════
# 🤖 CLASSE PRINCIPAL
# ═══════════════════════════════════════════════════════════════

class PrepareScriptRA:
    def __init__(self):
        self.driver = None
        self.logger = self._setup_logging()
        self.logger.info("🚀 Bot inicializado com RA!")
    
    def _setup_logging(self):
        """Configurar sistema de logs"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('prepare_ra.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    
    def setup_driver(self):
        """Inicializar Selenium WebDriver"""
        try:
            self.logger.info("⚙️ Configurando navegador...")
            options = webdriver.ChromeOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            if MODO_HEADLESS:
                options.add_argument('--headless')
            
            self.driver = webdriver.Chrome(options=options)
            self.logger.info("✅ Navegador pronto!")
            return True
        except Exception as e:
            self.logger.error(f"❌ Erro ao configurar navegador: {e}")
            return False
    
    def login_com_ra(self):
        """Fazer login usando RA e senha"""
        try:
            self.logger.info(f"🔐 Acessando {LOGIN_URL}...")
            self.driver.get(LOGIN_URL)
            time.sleep(2)
            
            # Tentar encontrar campo de RA
            self.logger.info("📝 Procurando campo de RA...")
            
            # Tenta diferentes seletores para o campo RA
            campos_ra = [
                (By.ID, "ra"),
                (By.NAME, "ra"),
                (By.ID, "login"),
                (By.NAME, "login"),
                (By.CLASS_NAME, "ra-input"),
                (By.XPATH, "//input[@type='text']")
            ]
            
            campo_encontrado = False
            for by, value in campos_ra:
                try:
                    campo = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((by, value))
                    )
                    campo.clear()
                    campo.send_keys(RA)
                    self.logger.info(f"✓ RA preenchido: {RA}")
                    campo_encontrado = True
                    break
                except:
                    continue
            
            if not campo_encontrado:
                self.logger.warning("⚠️ Campo de RA não encontrado, tentando campo de email/login...")
                campo = WebDriverWait(self.driver, TIMEOUT).until(
                    EC.presence_of_element_located((By.TAG_NAME, "input"))
                )
                campo.send_keys(RA)
                self.logger.info(f"✓ Credencial preenchida: {RA}")
            
            time.sleep(1)
            
            # Preencher senha
            self.logger.info("🔑 Preenchendo senha...")
            campos_senha = [
                (By.ID, "password"),
                (By.NAME, "password"),
                (By.ID, "senha"),
                (By.NAME, "senha"),
                (By.CLASS_NAME, "password-input")
            ]
            
            senha_encontrada = False
            for by, value in campos_senha:
                try:
                    campo_senha = self.driver.find_element(by, value)
                    campo_senha.clear()
                    campo_senha.send_keys(SENHA)
                    self.logger.info("✓ Senha preenchida")
                    senha_encontrada = True
                    break
                except:
                    continue
            
            if not senha_encontrada:
                inputs = self.driver.find_elements(By.TAG_NAME, "input")
                if len(inputs) > 1:
                    inputs[1].send_keys(SENHA)
                    self.logger.info("✓ Senha preenchida (campo alternativo)")
            
            time.sleep(1)
            
            # Clicar em login
            self.logger.info("🚀 Clicando em Login...")
            botoes_login = [
                (By.ID, "login-btn"),
                (By.NAME, "login"),
                (By.CLASS_NAME, "btn-login"),
                (By.XPATH, "//button[contains(text(), 'Login')]"),
                (By.XPATH, "//button[contains(text(), 'Entrar')]"),
                (By.TAG_NAME, "button")
            ]
            
            botao_clicado = False
            for by, value in botoes_login:
                try:
                    botao = self.driver.find_element(by, value)
                    if botao.is_displayed():
                        botao.click()
                        self.logger.info("✓ Botão de login clicado")
                        botao_clicado = True
                        break
                except:
                    continue
            
            if not botao_clicado:
                self.logger.error("❌ Não conseguiu clicar no botão de login")
                return False
            
            # Aguardar redirecionamento
            self.logger.info("⏳ Aguardando redirecionamento...")
            time.sleep(4)
            
            # Verificar se logou
            if "cursos" in self.driver.current_url or "dashboard" in self.driver.current_url:
                self.logger.info("✅ Login realizado com sucesso!")
                return True
            else:
                self.logger.warning(f"⚠️ URL atual: {self.driver.current_url}")
                self.logger.info("✅ Continuando (pode estar em página de transição)...")
                return True
        
        except Exception as e:
            self.logger.error(f"❌ Erro no login: {e}")
            return False
    
    def acessar_cursos(self):
        """Acessar página de cursos"""
        try:
            self.logger.info(f"📚 Acessando cursos...")
            self.driver.get(CURSOS_URL)
            time.sleep(3)
            self.logger.info("✅ Página de cursos carregada!")
            return True
        except Exception as e:
            self.logger.error(f"❌ Erro ao acessar cursos: {e}")
            return False
    
    def encontrar_e_fazer_quizzes(self):
        """Encontrar e fazer quizzes/lições automaticamente"""
        try:
            self.logger.info("🔍 Procurando por quizzes/lições...")
            
            # Encontrar links de quiz
            links_quiz = self.driver.find_elements(By.XPATH, "//a[contains(@href, '/quiz') or contains(text(), 'Quiz') or contains(text(), 'Lição')]")
            
            if not links_quiz:
                self.logger.warning("⚠️ Nenhum quiz encontrado")
                return False
            
            self.logger.info(f"📚 Encontrados {len(links_quiz)} quizzes/lições")
            
            for idx, link in enumerate(links_quiz[:3], 1):  # Fazer os 3 primeiros
                try:
                    titulo = link.text.strip() or f"Quiz {idx}"
                    self.logger.info(f"\n{'='*50}")
                    self.logger.info(f"Processando {idx}: {titulo}")
                    self.logger.info(f"{'='*50}")
                    
                    link.click()
                    time.sleep(3)
                    
                    # Fazer o quiz
                    self._responder_quiz_automaticamente()
                    
                    # Voltar
                    self.driver.back()
                    time.sleep(2)
                    
                except Exception as e:
                    self.logger.warning(f"⚠️ Erro ao processar quiz {idx}: {e}")
                    continue
            
            return True
        except Exception as e:
            self.logger.error(f"❌ Erro ao encontrar quizzes: {e}")
            return False
    
    def _responder_quiz_automaticamente(self):
        """Responder perguntas do quiz automaticamente"""
        try:
            self.logger.info("✍️ Respondendo perguntas...")
            
            # Encontrar todas as perguntas
            perguntas = self.driver.find_elements(By.CLASS_NAME, "question")
            
            if not perguntas:
                perguntas = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'question') or contains(@class, 'pergunta')]")
            
            self.logger.info(f"📊 Total de perguntas: {len(perguntas)}")
            
            for num, pergunta in enumerate(perguntas, 1):
                try:
                    # Encontrar opções de resposta
                    opcoes = pergunta.find_elements(By.CLASS_NAME, "answer-option")
                    
                    if not opcoes:
                        opcoes = pergunta.find_elements(By.TAG_NAME, "button")
                    
                    if not opcoes:
                        opcoes = pergunta.find_elements(By.TAG_NAME, "input")
                    
                    if opcoes:
                        # Selecionar a primeira opção (ou estratégia inteligente)
                        opcao_selecionada = opcoes[0]
                        opcao_selecionada.click()
                        self.logger.info(f"   Pergunta {num}: Respondida ✓")
                        time.sleep(ESPERA_ENTRE_RESPOSTAS)
                    else:
                        self.logger.warning(f"   Pergunta {num}: Sem opções encontradas")
                
                except Exception as e:
                    self.logger.warning(f"   Pergunta {num}: Erro - {e}")
                    continue
            
            # Submeter
            self._submeter_quiz()
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao responder quiz: {e}")
    
    def _submeter_quiz(self):
        """Submeter o quiz"""
        try:
            self.logger.info("🚀 Procurando botão de envio...")
            
            botoes = [
                (By.ID, "submit-btn"),
                (By.NAME, "submit"),
                (By.CLASS_NAME, "btn-submit"),
                (By.XPATH, "//button[contains(text(), 'Enviar')]"),
                (By.XPATH, "//button[contains(text(), 'Submeter')]"),
                (By.XPATH, "//button[contains(text(), 'Confirmar')]")
            ]
            
            for by, value in botoes:
                try:
                    botao = self.driver.find_element(by, value)
                    if botao.is_displayed():
                        botao.click()
                        self.logger.info("✅ Quiz enviado!")
                        time.sleep(2)
                        return True
                except:
                    continue
            
            self.logger.warning("⚠️ Botão de envio não encontrado")
            return False
        except Exception as e:
            self.logger.error(f"❌ Erro ao submeter: {e}")
            return False
    
    def executar_tudo(self):
        """Executar automação completa"""
        try:
            if not self.setup_driver():
                return False
            
            if not self.login_com_ra():
                return False
            
            if not self.acessar_cursos():
                return False
            
            if not self.encontrar_e_fazer_quizzes():
                self.logger.warning("⚠️ Não conseguiu fazer quizzes")
            
            self.logger.info("\n" + "="*60)
            self.logger.info("🎉 AUTOMAÇÃO CONCLUÍDA!")
            self.logger.info("="*60)
            return True
        
        except Exception as e:
            self.logger.error(f"❌ Erro geral: {e}")
            return False
        
        finally:
            if self.driver:
                self.logger.info("Fechando navegador em 5 segundos...")
                time.sleep(5)
                self.driver.quit()
                self.logger.info("🔌 Navegador fechado")

# ═══════════════════════════════════════════════════════════════
# 🎯 EXECUTAR
# ═══════════════════════════════════════════════════════════════

def main():
    print("\n" + "="*70)
    print("  🚀 PREPARE SCRIPT - AUTOMAÇÃO COM RA")
    print("="*70)
    print(f"📋 RA: {RA}")
    print(f"🔐 Senha: {'*' * len(SENHA)}")
    print(f"🌐 Plataforma: {PLATAFORMA_URL}")
    print("="*70 + "\n")
    
    # Iniciar bot
    bot = PrepareScriptRA()
    sucesso = bot.executar_tudo()
    
    if not sucesso:
        print("\n⚠️ Verifique o arquivo 'prepare_ra.log' para detalhes")
        sys.exit(1)

if __name__ == "__main__":
    main()
