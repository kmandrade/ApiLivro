Para rodar o projeto no Windows:

Crie um ambiente virtual com o comando: python -m venv venv

Ative o ambiente virtual com o comando: venv\Scripts\Activate

Instale as dependências com o comando: pip install -r requirements.txt

Altere em ApiLivro => settings.py em 'NAME': 'EmprestimoLivros' as configurações de banco de dados para o seu ambiente local (atualmente configurado para uso do PostegreSql Local)

Atualize o banco de dados com o comando: python manage.py migrate

Rode o projeto com o comando: python manage.py runserver

Tudo pronto! Basta utilizar a aplicação.