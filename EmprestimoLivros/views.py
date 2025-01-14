from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Livro, RegistroEmprestimo
from .serializers import (
    UserSerializer,
    LivroSerializer,
    RegistroEmprestimoSerializer,
    RegistroEmprestimoCreateSerializer
)

# Views para Livros
class LivroListCreateView(generics.ListCreateAPIView):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer

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
