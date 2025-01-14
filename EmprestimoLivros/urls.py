from django.urls import path
from .views import (
    LivroListCreateView,
    LivroUpdateView,
    LivroListView,
    RegistroEmprestimoListCreateView,
    RegistroEmprestimoUpdateView,
    RegistroEmprestimoDeleteView,
)

urlpatterns = [
    # URLs para Livros
    path('livros/', LivroListCreateView.as_view(), name='livro-list-create'),
    path('livros/<int:pk>/', LivroUpdateView.as_view(), name='livro-update'),
    path('livros/todos/', LivroListView.as_view(), name='livro-list'),

    # URLs para Registros de Empréstimos
    path('emprestimos/', RegistroEmprestimoListCreateView.as_view(), name='emprestimo-list-create'),
    path('emprestimos/<int:pk>/', RegistroEmprestimoUpdateView.as_view(), name='emprestimo-update'),
    path('emprestimos/<int:pk>/delete/', RegistroEmprestimoDeleteView.as_view(), name='emprestimo-delete'),
]
