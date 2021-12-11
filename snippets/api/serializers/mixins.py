from rest_framework import serializers


class SEOSerializerMixin(serializers.Serializer):

    meta = serializers.SerializerMethodField()

    @staticmethod
    def get_meta(obj):
        return {
            'seo_title': obj.seo_title,
            'seo_description': obj.seo_description
        }


class CommonSerializer(serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
