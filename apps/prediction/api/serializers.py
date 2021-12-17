from rest_framework import serializers


class SearchQuerySerializer(serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    query = serializers.CharField(required=True, max_length=512)
