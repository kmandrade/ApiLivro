# ApiLivro

Para rodar o projeto no Windows:

Crie um ambiente virtual com o comando: python -m venv venv

Ative o ambiente virtual com o comando: venv\Scripts\Activate

Instale as dependências com o comando: pip install -r requirements.txt

Altere em ApiLivro => settings.py em 'NAME': 'EmprestimoLivros' as configurações de banco de dados para o seu ambiente local (atualmente configurado para uso do PostegreSql Local)

Atualize o banco de dados com o comando: python manage.py migrate

Rode o projeto com o comando: python manage.py runserver

Anexado à pasta raiz do projeto, contém uma collection (EmpresitmoLivros.postman) .json para ser importada, onde contém as rotas 
para criação de usuário e realização de requests que atenderão ao desafio.

Para autenticar é necessário criar o usuario, gerar o token e no header adicionar a chave Authorization com valor Token {token}

Tudo pronto! Basta utilizar a aplicação.