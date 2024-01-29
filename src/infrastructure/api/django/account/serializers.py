from rest_framework import serializers


class AccountSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    created = serializers.DateTimeField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    number_identity = serializers.CharField()
    date_birth = serializers.DateField()
    gender = serializers.IntegerField()
    status = serializers.IntegerField()