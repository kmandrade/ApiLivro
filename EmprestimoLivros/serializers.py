from rest_framework import serializers
from .models import User, Livro, RegistroEmprestimo
from django.contrib.auth import get_user_model

User = get_user_model()

class LivroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Livro
        fields = ['id', 'nome', 'autor', 'resumo', 'isbn', 'disponivel', 'ativo', 'criacao', 'atualizacao']
        read_only_fields = ['id', 'criacao', 'atualizacao']

    def validate_isbn(self, value):
        livro_com_isbn = Livro.objects.filter(isbn=value).exclude(id=self.instance.id if self.instance else None)

        if livro_com_isbn.exists():
            raise serializers.ValidationError("Já existe um livro com este ISBN.")
        
        return value

    def validate(self, data):
        if self.instance and data.get('ativo') and self.instance.ativo:
            raise serializers.ValidationError({"ativo": "O livro já está ativo."})

        return data

class LivroDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Livro
        fields = ['id', 'ativo', 'disponivel']

    def validate(self, data):
        if not self.instance.ativo:
            raise serializers.ValidationError({"detail": "O livro já está inativo."})

        return data

    def update(self, instance, validated_data):
        instance.ativo = False
        instance.disponivel = False
        instance.save()
        return instance

class RegistroEmprestimoSerializer(serializers.ModelSerializer):
    usuario = serializers.StringRelatedField(read_only=True)
    livro = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = RegistroEmprestimo
        extra_kwargs = {
            'id': {'read_only': True},
            'solicitante': {'required': False}, 
        }
        fields = [
            'id', 'usuario', 'solicitante', 'livro', 'data_emprestimo',
            'data_devolucao', 'devolvido', 'criacao', 'atualizacao', 'ativo'
        ]
        read_only_fields = ['id', 'data_emprestimo', 'criacao', 'atualizacao']

    def validate(self, data):
        if self.context['request'].method in ['PUT', 'PATCH']:
            data.pop('solicitante', None) 
        return data


class RegistroEmprestimoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroEmprestimo
        fields = ['usuario', 'solicitante', 'livro', 'data_devolucao', 'devolvido']
        extra_kwargs = {'solicitante': {'required': False}}

    def validate_livro(self, value):
        try:
            livro = Livro.objects.get(pk=value.id)
        except Livro.DoesNotExist:
            raise serializers.ValidationError("Este livro não existe.")

        if not livro.ativo:
            raise serializers.ValidationError("Este livro não está ativo.")

        if not livro.disponivel:
            raise serializers.ValidationError("Este livro não está disponível para empréstimo.")
        return value

    def create(self, validated_data):
        livro = validated_data['livro']
        livro.disponivel = False
        livro.save()
        return super().create(validated_data)


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