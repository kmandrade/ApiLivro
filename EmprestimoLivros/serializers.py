from rest_framework import serializers
from .models import User, Livro, RegistroEmprestimo
from django.contrib.auth import get_user_model

User = get_user_model()

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


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    department = serializers.CharField(required=True)  
    email = serializers.EmailField(required=False, allow_blank=True)  
    first_name = serializers.CharField(required=False, allow_blank=True)  
    last_name = serializers.CharField(required=False, allow_blank=True) 
    employee_id = serializers.CharField(required=False, allow_blank=True) 

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'employee_id', 'department']
        read_only_fields = ['employee_id'] 

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            department=validated_data['department'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            employee_id=validated_data.get('employee_id', ''),
        )
        return user