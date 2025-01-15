from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Livro, RegistroEmprestimo
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from .serializers import (
    LivroSerializer,
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

    def perform_update(self, serializer):
        # Permite marcar o livro como não disponível
        if 'disponivel' in self.request.data:
            serializer.save(disponivel=self.request.data['disponivel'])
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
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegistroEmprestimoUpdateView(generics.UpdateAPIView):
    queryset = RegistroEmprestimo.objects.all()
    serializer_class = RegistroEmprestimoSerializer

class RegistroEmprestimoDeleteView(generics.DestroyAPIView):
    queryset = RegistroEmprestimo.objects.all()


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
                    "employee_id": user.employee_id,  # Retorna a matrícula gerada
                },
                "token": token.key
            }, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)