from rest_framework import serializers
from .models import User, Livro, RegistroEmprestimo

# (Funcionário)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        extra_kwargs = {
            'id': {'read_only': True},
        }
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'employee_id', 'department',
            'criacao', 'atualizacao', 'ativo'
        ]
        read_only_fields = ['id', 'criacao', 'atualizacao']

class LivroSerializer(serializers.ModelSerializer):
    class Meta:
        extra_kwargs = {
            'id': {'read_only': True},
        }
        model = Livro
        fields = ['id', 'nome', 'autor', 'isbn', 'resumo', 'disponivel', 'criacao', 'atualizacao']
        read_only_fields = ['id', 'criacao', 'atualizacao']

class RegistroEmprestimoSerializer(serializers.ModelSerializer):
    usuario = serializers.StringRelatedField(read_only=True)
    livro = serializers.StringRelatedField(read_only=True) 

    class Meta:
        model = RegistroEmprestimo
        extra_kwargs = {
            'id': {'read_only': True},
        }
        fields = [
            'id', 'usuario', 'solicitante', 'livro', 'data_emprestimo',
            'data_devolucao', 'devolvido', 'criacao', 'atualizacao', 'ativo'
        ]
        read_only_fields = ['id', 'data_emprestimo', 'criacao', 'atualizacao']

class RegistroEmprestimoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroEmprestimo
        extra_kwargs = {
            'id': {'read_only': True},
        }
        fields = ['usuario', 'solicitante', 'livro', 'data_devolucao', 'devolvido']

    def validate(self, data):
        # Valida se o livro está disponível para empréstimo
        livro = data.get('livro')
        if livro and not livro.disponivel:
            raise serializers.ValidationError({'livro': 'Este livro não está disponível para empréstimo.'})

        return data

    def create(self, validated_data):
        # Marca o livro como indisponível após a criação do registro de empréstimo
        livro = validated_data['livro']
        livro.disponivel = False
        livro.save()

        return super().create(validated_data)