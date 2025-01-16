from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from .models import Livro, RegistroEmprestimo
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from .serializers import (
    LivroSerializer,
    LivroDeleteSerializer,
    RegistroEmprestimoSerializer,
    RegistroEmprestimoCreateSerializer,
    RegisterUserSerializer
)

# Views para Livros
class LivroListCreateView(generics.ListCreateAPIView):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer
    permission_classes = [IsAuthenticated]

class LivroUpdateView(generics.UpdateAPIView):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        # Permite atualizações parciais
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

    def perform_update(self, serializer):
        if 'ativo' in self.request.data and self.request.data['ativo'] is True:
            serializer.save(ativo=True, disponivel=True)
        else:
            serializer.save()


class LivroListView(generics.ListAPIView):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer
    permission_classes = [IsAuthenticated]


# Views para Registros de Empréstimos
class RegistroEmprestimoListCreateView(APIView):
    def get(self, request):
        registros = RegistroEmprestimo.objects.all()
        serializer = RegistroEmprestimoSerializer(registros, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RegistroEmprestimoCreateSerializer(data=request.data)
        if serializer.is_valid():
            usuario = request.user
            serializer.save(usuario=usuario, solicitante=usuario.username)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    permission_classes = [IsAuthenticated]

class RegistroEmprestimoUpdateView(generics.UpdateAPIView):
    queryset = RegistroEmprestimo.objects.all()
    serializer_class = RegistroEmprestimoSerializer

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.devolvido:
            instance.livro.disponivel = True
            instance.livro.save()
        elif not instance.devolvido and not instance.livro.disponivel:
            raise ValidationError({"error": "O livro já está indisponível e não pode ser emprestado novamente."})
    permission_classes = [IsAuthenticated]


class LivroDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Livro.objects.all()
    serializer_class = LivroDeleteSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        serializer = self.get_serializer(instance=instance, data={}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"detail": "Livro inativado com sucesso."}, status=status.HTTP_200_OK)
    permission_classes = [IsAuthenticated]


class RegisterUserView(APIView):
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "user": {
                    "username": user.username,
                    "email": user.email,
                    "department": user.department,
                    "employee_id": user.employee_id,
                },
                "token": token.key
            }, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)