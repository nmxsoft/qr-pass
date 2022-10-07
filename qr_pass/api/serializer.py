from rest_framework import serializers

from qpass.models import Customer, Logs
from qpass.views import create_key


class CustomerViewSerializer(serializers.ModelSerializer):
    master = serializers.CharField(required=False)

    class Meta:
        model = Customer
        exclude = ['key']

    def create(self, validated_data):
        master = self.context['request'].user
        username = self.validated_data.pop('username')
        real_name = self.validated_data.pop('real_name')
        access = self.validated_data.pop('access')
        key = create_key()
        new_rec = Customer.objects.create(username=username,
                                          real_name=real_name,
                                          access=access,
                                          key=key,
                                          master=master)
        return new_rec


class RealNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ('real_name', 'username')


class LogsViewSerializer(serializers.ModelSerializer):
    user = RealNameSerializer()

    class Meta:
        model = Logs
        fields = '__all__'
