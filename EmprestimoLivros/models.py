from django.db import models
from django.contrib.auth.models import AbstractUser

# Classe Base
class Base(models.Model):
    criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    atualizacao = models.DateTimeField(auto_now=True, verbose_name="Última Atualização")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")

    class Meta:
        abstract = True

# Modelo de Usuário (Funcionário)
class User(AbstractUser):
    employee_id = models.CharField(
        max_length=20, unique=True, verbose_name="ID do Funcionário", blank=True
    )
    department = models.CharField(max_length=50, verbose_name="Departamento")

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        # Gera automaticamente o employee_id no formato EMP001 se ainda não existir
        if not self.employee_id:
            total_users = User.objects.count() + 1 
            self.employee_id = f"EMP{str(total_users).zfill(3)}" 
        super().save(*args, **kwargs)

# Modelo de Livro
class Livro(Base):
    nome = models.CharField("Nome do Livro", max_length=70)
    autor = models.CharField("Autor", max_length=100)
    resumo = models.CharField("Resumo", max_length=100)
    isbn = models.CharField("ISBN", max_length=13, unique=True)  # Identificador internacional do livro
    disponivel = models.BooleanField(default=True, verbose_name="Disponível")

    class Meta:
        verbose_name = "Livro"
        verbose_name_plural = "Livros"
        ordering = ["nome"]

    def __str__(self):
        return f"{self.nome} - {self.autor}"

# Modelo de Registro de Empréstimo
class RegistroEmprestimo(Base):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="emprestimos_gerenciados", verbose_name="Funcionário")
    solicitante = models.CharField(max_length=100, verbose_name="Nome do Solicitante")
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE, related_name="emprestimos", verbose_name="Livro")
    data_emprestimo = models.DateField(auto_now_add=True, verbose_name="Data do Empréstimo")
    data_devolucao = models.DateField(null=True, blank=True, verbose_name="Data de Devolução")
    devolvido = models.BooleanField(default=False, verbose_name="Devolvido")

    class Meta:
        verbose_name = "Registro de Empréstimo"
        verbose_name_plural = "Registros de Empréstimos"
        ordering = ["-data_emprestimo"]

    def __str__(self):
        return f"{self.livro.nome} emprestado para {self.solicitante} por {self.usuario.username}"
