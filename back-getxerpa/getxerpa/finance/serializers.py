from django.contrib.auth.models import User, Group
from rest_framework import serializers
from datetime import datetime
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
    t_config = serializers.SerializerMethodField()
    group_title = serializers.SerializerMethodField()

    def get_t_config(self,obj):
        date_n_m = obj.time_created.strftime('%d %B')
        month = obj.time_created.strftime('%B')
        hour = obj.time_created.strftime("%I:%M %p")
        result = {
            'date_n_m':date_n_m,
            'month':month,
            'hour':hour
        }
        return result
    def get_group_title(self, obj):
        today = datetime.now().date()
        trans_date = obj.time_created.date()
        
        if trans_date == today:
            return 'Hoy'
        else:
            return trans_date.strftime('%d %B')

    class Meta:
        model = Transaction
        fields = '__all__'
        
class CombinedResponseSerializer(serializers.Serializer):
    category_detail = CategoryExpensesDetailSerializer()
    transactions = TransactionSerializer(many=True)

