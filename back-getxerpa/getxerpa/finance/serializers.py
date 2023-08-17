from django.contrib.auth.models import User, Group
from rest_framework import serializers
from getxerpa.finance.models import Category, Transaction


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CategoryExpensesSerializer(serializers.ModelSerializer):
    total_expenses = serializers.SerializerMethodField()
    percent_expensed = serializers.SerializerMethodField()
    count_transactions = serializers.SerializerMethodField()
    amount_avilable = serializers.SerializerMethodField()

    def get_common_totals(self, obj):
        transactions = Transaction.objects.filter(category=obj)
        total = sum([transaction.amount for transaction in transactions])
        return total

    def get_total_expenses(self, obj):
        return self.get_common_totals(obj)

    def get_percent_expensed(self, obj):
        if obj.limit > 0:
            total = self.get_common_totals(obj)
            percent = total / obj.limit * 100
            return percent
        return None

    def get_count_transactions(self, obj):
        transactions_count = Transaction.objects.filter(category=obj).count()
        return transactions_count

    def get_amount_avilable(self, obj):
        if obj.limit == 0:
            total = self.get_common_totals(obj)
            am_available = total - obj.limit
            return am_available
        return None

    class Meta:
        model = Category
        fields = '__all__'


class CategoryExpensesDetailSerializer(CategoryExpensesSerializer):
    def get_amount_avilable(self, obj):
        if obj.limit > 0:
            total = self.get_common_totals(obj)
            am_available = obj.limit - total
            return am_available
        return None

    class Meta(CategoryExpensesSerializer.Meta):
        model = Category
        fields = '__all__'




class TransactionSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    class Meta:
        model = Transaction
        fields = '__all__'
        
class CombinedResponseSerializer(serializers.Serializer):
    category_detail = CategoryExpensesDetailSerializer()
    transactions = TransactionSerializer(many=True)

