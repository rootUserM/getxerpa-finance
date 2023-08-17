from django.contrib.auth.models import User, Group
from rest_framework import viewsets,permissions,generics
from getxerpa.finance.serializers import UserSerializer, GroupSerializer, CategorySerializer, TransactionSerializer,CategoryExpensesSerializer,CategoryExpensesDetailSerializer
from getxerpa.finance.models import Category, Transaction
from rest_framework.decorators import action
from datetime import datetime
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
        transactions = Transaction.objects.filter(category=category).order_by('-time_created')
        grouped_transactions = self.group_transactions_by_date(transactions)
        response_data = []
        for group_date, group_transactions in grouped_transactions.items():
            response_data.append({
                'group_name': group_date,
                'transactions': TransactionSerializer(group_transactions, many=True).data
            })
        
        response = {
            'category_detail': CategoryExpensesDetailSerializer(category).data,
            'transactions': response_data
        }
        return Response(response)
    
    @action(detail=True, methods=['get'],url_path='transaction-deatil', url_name='transaction_deatil')
    def transaction_deatil(self, request,pk=None):
        transactions = Transaction.objects.get(id=pk)
        transactions_serializer = TransactionSerializer(transactions)
        return Response(transactions_serializer.data)
    
    def group_transactions_by_date(self, transactions):
        grouped_transactions = {}
        
        for transaction in transactions:
            trans_date = transaction.time_created.date()
            group_date = trans_date.strftime('%d %B')
            
            if trans_date == datetime.now().date():
                group_date = 'Hoy'
            
            if group_date in grouped_transactions:
                grouped_transactions[group_date].append(transaction)
            else:
                grouped_transactions[group_date] = [transaction]
        
        return grouped_transactions

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



