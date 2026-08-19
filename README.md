# Prepare Script 🚀

Script de automação de tarefas para a plataforma **Prepará SP** - Sistema de quizzes online.

## Características

✅ **Automação completa** - Login, acesso ao quiz e preenchimento automático  
✅ **Interface Web** - Dashboard visual para controle fácil  
✅ **Configuração via JSON** - Suporte a múltiplos quizzes  
✅ **Logging detalhado** - Rastreamento de todas as ações  
✅ **Tratamento de erros** - Recuperação automática de falhas  

## Requisitos

- Python 3.8+
- Chrome/Chromium instalado
- Selenium WebDriver

## Instalação

1. **Clone o repositório:**
```bash
git clone https://github.com/isaqueolimpiodasilva799-collab/Prepare-Script.git
cd Prepare-Script
```

2. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

3. **Configure as credenciais:**
```bash
cp .env.example .env
# Edite o arquivo .env com suas credenciais
```

4. **Configure os quizzes:**
Edite `config.json` com o ID do quiz e as respostas desejadas.

## Uso

### Via Python (Terminal)
```bash
python main.py
```

### Via Interface Web
Abra o arquivo `index.html` em seu navegador e preencha o formulário.

## Estrutura do Projeto

```
Prepare-Script/
├── main.py              # Script principal de automação
├── config.json          # Configuração de quizzes
├── index.html           # Dashboard web
├── requirements.txt     # Dependências Python
├── .env.example         # Exemplo de variáveis de ambiente
└── README.md            # Este arquivo
```

## Configuração de Quizzes

Edite `config.json` para adicionar quizzes:

```json
{
  "quizzes": {
    "ID_DO_QUIZ": [
      "Resposta 1",
      "Resposta 2",
      "Resposta 3"
    ]
  }
}
```

## Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```
PREPARE_USERNAME=seu_email@email.com
PREPARE_PASSWORD=sua_senha_aqui
```

## Logs

Os logs são salvos em `task_automation.log` e também exibidos no console.

## ⚠️ Aviso Importante

Este script deve ser usado **apenas com autorização explícita**. Certifique-se de que tem permissão da plataforma antes de usar.

## Contribuição

Sinta-se livre para abrir issues e pull requests!

## Licença

MIT - Veja LICENSE para detalhes