# 🎙️ Microserviço de Transcrição de Vídeos

## 📌 Visão Geral
O **Microserviço de Transcrição de Vídeos** é responsável por baixar vídeos, extrair áudio e realizar a transcrição do conteúdo falado. Esse serviço opera de forma assíncrona, consumindo mensagens de uma fila RabbitMQ e publicando as transcrições processadas de volta na fila de resposta.

## ⚙️ Tecnologias Utilizadas
- **Linguagem:** Python 3.10
- **Framework Web:** FastAPI
- **Transcrição:** OpenAI Whisper
- **Download de Vídeos:** yt-dlp
- **Mensageria:** RabbitMQ
- **Gerenciamento de Dependências:** `requirements.txt`

## 📂 Estrutura do Projeto

```
.
├── README.MD
├── requirements.txt
├── src
│   ├── application
│   │   ├── dtos
│   │   │   ├── download_and_transcribe_dto.py
│   │   └── use_cases
│   │       ├── downloader.py
│   │       ├── fetch_and_transcribe.py
│   │       └── transcriber.py
│   ├── config
│   │   └── settings.py
│   ├── domain
│   │   ├── download.py
│   │   └── transcription.py
│   ├── infrastructure
│   │   ├── interfaces
│   │   │   ├── downloader.py
│   │   │   ├── message_broker.py
│   │   │   └── transcriber.py
│   │   ├── rabbitmq.py
│   │   ├── whisper.py
│   │   └── youtube_downloader.py
│   ├── main.py
```

## 🔄 Fluxo de Funcionamento
1. **Recepção de Mensagem:** O microserviço recebe uma URL de vídeo através de uma fila RabbitMQ.
2. **Download do Áudio:** O serviço baixa o áudio do vídeo utilizando `yt-dlp`.
3. **Transcrição do Áudio:** O áudio é processado pelo Whisper para gerar o texto transcrito.
4. **Publicação da Transcrição:** O texto transcrito é publicado na fila de resposta RabbitMQ.
5. **Retorno ao Usuário:** O backend consome a resposta e retorna a transcrição ao usuário.

## 📄 Configuração de Variáveis de Ambiente

Crie um arquivo **.env.exemplo** com as seguintes configurações:

```env
# Configuração do RabbitMQ
RABBIT_HOST="localhost"
RABBIT_PORT=5672
RABBIT_USER="guest"
RABBIT_PASSWORD="guest"
RABBIT_URI="amqp://${RABBIT_HOST}:${RABBIT_PORT}"
```

## 🚀 Como Executar o Microserviço

### 1. Clonar o Repositório
```bash
git clone https://github.com/joaogabriel1995/echoText.git
cd speakly-transcriber
```

### 2. Criar um ambiente virtual e instalar dependências
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configurar as variáveis de ambiente
Crie um arquivo **.env** e adicione as configurações necessárias:
```env
RABBITMQ_URL=amqp://user:password@localhost:5672/
```

### 4. Executar o Serviço
```bash
python src/main.py
```

## 🛠 Fila de Mensagens
O microserviço opera de forma assíncrona através de filas do RabbitMQ:
- **Fila de Entrada:** `transcription-queue` (recebe URLs para processar)
- **Fila de Saída:** `transcription-response-queue` (retorna o texto transcrito)

