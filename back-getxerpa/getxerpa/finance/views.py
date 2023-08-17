from django.contrib.auth.models import User, Group
from rest_framework import viewsets,permissions,generics
from getxerpa.finance.serializers import UserSerializer, GroupSerializer, CategorySerializer, TransactionSerializer,CategoryExpensesSerializer,CategoryExpensesDetailSerializer,CombinedResponseSerializer
from getxerpa.finance.models import Category, Transaction
from rest_framework.decorators import action
from rest_framework.response import Response

class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Categories to be viewed or edited.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=False, methods=['get'],url_path='category-expenses', url_name='category_expenses')
    def category_expenses(self, request,pk=None):
        categories = self.queryset.all()
        serializer_class = CategoryExpensesSerializer(categories,many=True)
        return Response(serializer_class.data)
    
    @action(detail=True, methods=['get'],url_path='category-detail', url_name='category_detail')
    def category_deatil(self, request,pk=None):
        category = self.get_object()
        category_serializer = CategoryExpensesDetailSerializer(category)
        transactions = Transaction.objects.filter(category=category).order_by('time_created')
        transactions_serializer = TransactionSerializer(transactions, many=True)
        response = {
            'category_detail': category_serializer.data,
            'transactions': transactions_serializer.data
        }
        return Response(response)
    
    @action(detail=True, methods=['get'],url_path='transaction-deatil', url_name='transaction_deatil')
    def transaction_deatil(self, request,pk=None):
        transactions = Transaction.objects.get(id=pk)
        transactions_serializer = TransactionSerializer(transactions)
        return Response(transactions_serializer.data)

class TransactionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Transactions to be viewed or edited.
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]



