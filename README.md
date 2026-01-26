# 💾 Arquivo Nostalgia

[![Read in English](https://img.shields.io/badge/Read%20in-English-blue?style=for-the-badge)](#english-version)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)

O **Arquivo Nostalgia** é um sistema web que permite aos usuários registrar e organizar **filmes, séries, desenhos e jogos** que marcaram suas vidas. Uma plataforma nostálgica para catalogar suas memórias culturais.

![Screenshot da aplicação](static/img/screenshot.png)

## 🎯 Objetivo

Este projeto visa resolver o problema das **memórias afetivas fragmentadas** na era digital, permitindo que cada usuário monte seu próprio "arquivo nostálgico" personalizado, reunindo em um só lugar todo o entretenimento que fez parte de sua história.

## ✨ Funcionalidades

- 🎬 **Catálogo de Filmes** - Navegue por filmes populares e clássicos
- 📺 **Catálogo de Séries** - Descubra séries nostálgicas e atuais
- 🎮 **Catálogo de Jogos** - Explore jogos de diferentes plataformas
- 🔍 **Sistema de Busca** - Pesquise por títulos específicos
- 🏷️ **Filtros por Gênero** - Filtre conteúdo por categorias
- 📝 **Arquivo Confidencial** - Curiosidades diárias geradas por IA
- 👤 **Sistema de Autenticação** - Registro e login de usuários
- 📱 **Design Responsivo** - Funciona em desktop e mobile
- 🏆 **Sistema de Ranks Dinâmicos** - Ranks globais e por categoria (filmes, séries, jogos) com cores e frases personalizadas
- 📊 **Ranking da Comunidade** - Ranking diário dos itens mais salvos pela comunidade
- 📥 **Exportação de Listas** - Baixe sua lista pessoal em CSV formatado
- ✏️ **Edição de Perfil** - Edite seu nome de usuário diretamente no perfil
- 📈 **Estatísticas do Usuário** - Veja seu progresso e conquistas nostálgicas
- 🔒 **Integração com Supabase Auth** - Segurança e gerenciamento de sessões
- 💾 **Backup e persistência** - Dados salvos em nuvem

## 🛠️ Tecnologias Utilizadas

### Backend
- **[Flask](https://flask.palletsprojects.com/)** - Framework web Python
- **[Supabase](https://supabase.com/)** - Backend as a Service (autenticação e banco de dados)
- **[Flask-Login](https://flask-login.readthedocs.io/)** - Gerenciamento de sessões
- **[Flask-WTF](https://flask-wtf.readthedocs.io/)** - Formulários e validação

### APIs Externas
- **[TMDB API](https://www.themoviedb.org/documentation/api)** - Dados de filmes e séries
- **[RAWG API](https://rawg.io/apidocs)** - Dados de jogos
- **[Steam API](https://steamcommunity.com/dev)** - Informações complementares de jogos
- **[Google Gemini API](https://ai.google.dev/)** - Geração de curiosidades com IA

### Frontend
- **HTML5/CSS3** - Estrutura e estilização
- **JavaScript** - Interatividade
- **[Font Awesome](https://fontawesome.com/)** - Ícones

## 📋 Pré-requisitos

- Python 3.8 ou superior
- Chaves de API:
  - [TMDB API Key](https://www.themoviedb.org/settings/api)
  - [RAWG API Key](https://rawg.io/apidocs)
  - [Google Gemini API Key](https://ai.google.dev/)

## 🚀 Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/lucascarvalho1808/arquivo-nostalgia.git
cd arquivo-nostalgia

```

### 2. Crie um ambiente virtual

```bash
python -m venv venv

```

### 3. Ative o ambiente virtual

**Windows:**

```bash
venv\Scripts\activate

```

**Linux/Mac:**

```bash
source venv/bin/activate

```

### 4. Instale as dependências

```bash
pip install -r requirements.txt

```

### 5. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# Flask
FLASK_SECRET_KEY=sua_chave_secreta_aqui

# Supabase
SUPABASE_URL=sua_url_supabase
SUPABASE_KEY=sua_chave_supabase

# APIs Externas
TMDB_API_KEY=sua_chave_tmdb
RAWG_API_KEY=sua_chave_rawg
GEMINI_API_KEY=sua_chave_gemini

```

### 6. Execute a aplicação

```bash
python app.py

```

A aplicação estará disponível em `http://localhost:5000`

## 🎨 Capturas de Tela

### Página Inicial
![Screenshot da Página Inicial](CAMINHO/DA/IMAGEM_HOME.png)

### Páginas de conteúdos Filmes

### Páginas de conteúdos Séries

### Páginas de conteúdos Jogos

### Sistema de Busca

### Página "Meus Arquivos"

### Perfil do Usuário

## 🔒 Autenticação

O sistema utiliza **Supabase Auth** para gerenciar:

* Registro de novos usuários
* Login/Logout
* Recuperação de senha via e-mail
* Sessões persistentes

## 🤖 IA Generativa

A funcionalidade "Arquivo Confidencial" utiliza o **Google Gemini** para gerar curiosidades diárias sobre filmes, séries e jogos de forma automática e contextualizada.

## 📊 APIs e Integrações

### TMDB (The Movie Database)

* Busca de filmes e séries populares
* Filmes clássicos (Top Rated)
* Séries nostálgicas (anos 90-2000)
* Filtros por gênero
* Detalhes completos de títulos

### RAWG

* Catálogo de jogos populares
* Informações de plataformas
* Avaliações e metacríticas
* Integração com Steam para capas verticais

### Steam

* Capas verticais de jogos
* Trailers de jogos
* Informações complementares

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](https://www.google.com/search?q=LICENSE) para mais detalhes.

## 👤 Autores

**Lucas Carvalho**

* GitHub: [@lucascarvalho1808](https://github.com/lucascarvalho1808)

**Vinícius Rocha**

* GitHub: [@ViniciusGomes13](https://github.com/ViniciusGomes13)

**Renan Gurgel**

* GitHub: [@renan-gurgel](https://github.com/renan-gurgel)

---

<div id="english-version"></div>

# 💾 Arquivo Nostalgia (Nostalgia Archive)

**Arquivo Nostalgia** is a web system that allows users to register and organize **movies, series, cartoons, and games** that marked their lives. A nostalgic platform to catalog your cultural memories.

## 🎯 Goal

This project aims to solve the problem of **fragmented affective memories** in the digital age, allowing each user to build their own personalized "nostalgia archive", gathering all the entertainment that was part of their history in one place.

## ✨ Features

* 🎬 **Movies Catalog** - Browse popular and classic movies
* 📺 **Series Catalog** - Discover nostalgic and current series
* 🎮 **Games Catalog** - Explore games from different platforms
* 🔍 **Search System** - Search for specific titles
* 🏷️ **Genre Filters** - Filter content by categories
* 📝 **Confidential File** - Daily trivia generated by AI
* 👤 **Authentication System** - User registration and login
* 📱 **Responsive Design** - Works on desktop and mobile
* 🏆 **Dynamic Rank System** - Global and category ranks (movies, series, games) with custom colors and phrases
* 📊 **Community Ranking** - Daily ranking of the most saved items by the community
* 📥 **List Export** - Download your personal list in formatted CSV
* ✏️ **Profile Editing** - Edit your username directly in the profile
* 📈 **User Stats** - View your progress and nostalgic achievements
* 🔒 **Supabase Auth Integration** - Security and session management
* 💾 **Backup and Persistence** - Data saved in the cloud

## 🛠️ Technologies Used

### Backend

* **[Flask](https://flask.palletsprojects.com/)** - Python web framework
* **[Supabase](https://supabase.com/)** - Backend as a Service (authentication and database)
* **[Flask-Login](https://flask-login.readthedocs.io/)** - Session management
* **[Flask-WTF](https://flask-wtf.readthedocs.io/)** - Forms and validation

### External APIs

* **[TMDB API](https://www.themoviedb.org/documentation/api)** - Movie and series data
* **[RAWG API](https://rawg.io/apidocs)** - Game data
* **[Steam API](https://steamcommunity.com/dev)** - Complementary game information
* **[Google Gemini API](https://ai.google.dev/)** - AI-generated trivia

### Frontend

* **HTML5/CSS3** - Structure and styling
* **JavaScript** - Interactivity
* **[Font Awesome](https://fontawesome.com/)** - Icons

## 📋 Prerequisites

* Python 3.8 or higher
* API Keys:
* [TMDB API Key](https://www.themoviedb.org/settings/api)
* [RAWG API Key](https://rawg.io/apidocs)
* [Google Gemini API Key](https://ai.google.dev/)



## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/lucascarvalho1808/arquivo-nostalgia.git
cd arquivo-nostalgia

```

### 2. Create a virtual environment

```bash
python -m venv venv

```

### 3. Activate the virtual environment

**Windows:**

```bash
venv\Scripts\activate

```

**Linux/Mac:**

```bash
source venv/bin/activate

```

### 4. Install dependencies

```bash
pip install -r requirements.txt

```

### 5. Configure environment variables

Create a `.env` file in the project root:

```env
# Flask
FLASK_SECRET_KEY=your_secret_key_here

# Supabase
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

# External APIs
TMDB_API_KEY=your_tmdb_key
RAWG_API_KEY=your_rawg_key
GEMINI_API_KEY=your_gemini_key

```

### 6. Run the application

```bash
python app.py

```

The application will be available at `http://localhost:5000`

## 🎨 Screenshots

### Home Page

### Movies Content Pages

### Series Content Pages

### Games Content Pages

### Search System

### "My Archives" Page

### User Profile

## 🔒 Authentication

The system uses **Supabase Auth** to manage:

* New user registration
* Login/Logout
* Password recovery via email
* Persistent sessions

## 🤖 Generative AI

The "Confidential File" feature uses **Google Gemini** to generate daily trivia about movies, series, and games automatically and contextually.

## 📊 APIs and Integrations

### TMDB (The Movie Database)

* Search for popular movies and series
* Classic movies (Top Rated)
* Nostalgic series (90s-2000s)
* Filters by genre
* Complete title details

### RAWG

* Catalog of popular games
* Platform information
* Ratings and metacritics
* Steam integration for vertical covers

### Steam

* Vertical game covers
* Game trailers
* Complementary information

## 📝 License

This project is under the MIT license. See the [LICENSE](https://www.google.com/search?q=LICENSE) file for more details.

## 👤 Authors

**Lucas Carvalho**

* GitHub: [@lucascarvalho1808](https://github.com/lucascarvalho1808)

**Vinícius Rocha**

* GitHub: [@ViniciusGomes13](https://github.com/ViniciusGomes13)

**Renan Gurgel**

* GitHub: [@renan-gurgel](https://github.com/renan-gurgel)

---

<p align="center">
Made with ❤️ by those who don't forget where they came from
</p>
