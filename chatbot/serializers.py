from rest_framework import serializers

class ChatRequestSerializer(serializers.Serializer):
    contents = serializers.ListField(
        child=serializers.DictField(),  # each item: {"role": "...", "content": "..."}
    )
