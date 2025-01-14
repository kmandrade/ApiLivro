from django.contrib import admin
from .models import User, Livro, RegistroEmprestimo

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "employee_id", "department", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active", "department")
    search_fields = ("username", "email", "employee_id", "department")
    ordering = ("username",)

@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ("nome", "autor", "isbn", "disponivel", "criacao", "atualizacao")
    list_filter = ("disponivel", "criacao")
    search_fields = ("nome", "autor", "isbn")
    ordering = ("nome",)

@admin.register(RegistroEmprestimo)
class RegistroEmprestimoAdmin(admin.ModelAdmin):
    list_display = ("livro", "solicitante", "usuario", "data_emprestimo", "data_devolucao", "devolvido")
    list_filter = ("devolvido", "data_emprestimo", "data_devolucao")
    search_fields = ("livro__nome", "solicitante", "usuario__username")
    ordering = ("-data_emprestimo",)
