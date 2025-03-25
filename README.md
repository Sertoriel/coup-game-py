```markdown
# 🃏 Coup Game

![Flask Version](https://img.shields.io/badge/Flask-3.1.0-blue) ![Python Version](https://img.shields.io/badge/Python-3.x-blue)

O **Coup Game** é uma implementação interativa do jogo de cartas *Coup* utilizando Flask para o backend e Tailwind CSS para o frontend. Este projeto permite que os jogadores realizem ações, desafiem, bloqueiem e troquem cartas conforme as regras do jogo.

---

## 📖 Índice

- [Recursos do Projeto](#-recursos-do-projeto)
- [Estrutura de Diretórios](#-estrutura-de-diretórios)
- [Instalação](#-instalação)
- [Executando o Projeto](#-executando-o-projeto)
- [Como Contribuir](#-como-contribuir)

---

## 🚀 Recursos do Projeto

- **Backend:** Desenvolvido em Python com o Flask.
- **Frontend:** Templates HTML com Tailwind CSS (incluso via CDN, mas customizável conforme necessário).
- **Lógica de Jogo:** Implementa as regras do jogo *Coup*, incluindo ações, bloqueios, desafios, revelação de cartas e troca de cartas pelo Embaixador.
- **Interatividade:** Páginas para cadastro de jogadores, execução de ações e reações (desafio, bloqueio, revelação e troca de cartas).

---

## 🗂️ Estrutura de Diretórios

A estrutura de diretórios do projeto está organizada da seguinte forma:

```
coup-game/
├── app.py                # Ponto de entrada da aplicação Flask
├── game.py               # Lógica principal do jogo e classes
├── requirements.txt      # Lista de dependências com versões fixas
├── README.md             # Este arquivo de documentação
├── .gitignore            # Arquivo para ignorar arquivos/pastas indesejados no Git
├── static/
│   └── css/
│       └── tailwind.css  # Arquivo CSS (pode ser gerado ou utilizar o CDN no HTML)
└── templates/
    ├── base.html         # Template base com layout e Tailwind incluído
    ├── index.html        # Página principal com estado do jogo e ações dos jogadores
    ├── add_players.html  # Página para cadastro de jogadores
    ├── reaction.html     # Página para reação à ação pendente (desafio/bloqueio)
    ├── reveal.html       # Página para o jogador que perdeu um desafio escolher qual carta revelar
    └── exchange.html     # Página para o Embaixador escolher quais cartas manter na troca
```

---

## 💻 Instalação

Siga os passos abaixo para configurar seu ambiente de desenvolvimento e instalar as dependências:

1. **Clone o repositório**

   ```bash
   git clone https://github.com/seu-usuario/coup-game.git
   cd coup-game
   ```

2. **Crie um ambiente virtual**

   É recomendado isolar as dependências do projeto:

   ```bash
   python -m venv venv
   ```

3. **Ative o ambiente virtual**

   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **Linux/MacOS:**
     ```bash
     source venv/bin/activate
     ```

4. **Instale as dependências**

   Com o ambiente virtual ativado, instale os pacotes necessários:

   ```bash
   pip install -r requirements.txt
   ```

   > O arquivo `requirements.txt` inclui:
   >
   > ```txt
   > Flask==3.1.0
   > click==8.1.8
   > itsdangerous==2.2.0
   > Jinja2==3.1.6
   > MarkupSafe==3.0.2
   > Werkzeug==3.1.3
   > blinker==1.9.0
   > colorama==0.4.6
   > ```

---

## 🚀 Executando o Projeto

Após instalar as dependências, inicie o servidor Flask:

```bash
python app.py
```

O servidor iniciará em modo de *debug* e estará disponível no endereço:  
**http://127.0.0.1:5000/**

- **Cadastro de Jogadores:** Ao acessar a aplicação, você será direcionado para a página de cadastro de jogadores. Informe os nomes (separados por vírgula) e inicie o jogo.
- **Jogabilidade:** Use as páginas para executar ações, reagir a desafios e realizar trocas de cartas conforme as regras.

---

## 🤝 Como Contribuir

Quer contribuir para o desenvolvimento do **Coup Game**? Siga os passos abaixo:

1. **Fork** deste repositório.
2. Crie uma nova branch para sua feature ou correção:

   ```bash
   git checkout -b minha-nova-feature
   ```

3. Faça suas alterações e commits com mensagens claras.
4. Envie sua branch para o seu repositório remoto:

   ```bash
   git push origin minha-nova-feature
   ```

5. Abra um **Pull Request** detalhando suas alterações e sugestões.

---

<div align="center">
  <p>Divirta-se desenvolvendo e jogando! 🎉🃏</p>
</div>
```