from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    LivroListCreateView,
    LivroUpdateView,
    LivroListView,
    RegistroEmprestimoListCreateView,
    RegistroEmprestimoUpdateView,
    LivroDeleteView,
    RegisterUserView
)

urlpatterns = [
    # URLs para Livros
    path('livros', LivroListCreateView.as_view(), name='livro-list-create'),
    path('livros/<int:pk>', LivroUpdateView.as_view(), name='livro-update'),
    path('livros/inativar/<int:pk>', LivroDeleteView.as_view(), name='livro-update'),
    path('livros/todos', LivroListView.as_view(), name='livro-list'),

    # URLs para Registros de Empréstimos
    path('emprestimos', RegistroEmprestimoListCreateView.as_view(), name='emprestimo-list-create'),
    path('emprestimos/<int:pk>', RegistroEmprestimoUpdateView.as_view(), name='emprestimo-update'),

    # Url para obter token
    path('token', obtain_auth_token, name='api_token_auth'),

     # URL para Registro de Usuário
    path('usuarios/registrar', RegisterUserView.as_view(), name='user-register'),
]
