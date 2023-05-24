from rest_framework import serializers

from api.IVSMethods import ivs_channel_data
from api.models import CustomUser


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "phone", "password"]

    def create(self, validated_data):
        validated_data["playback_url"] = ivs_channel_data.get("playback_url")
        validated_data["rtmps_server"] = ivs_channel_data.get("rtmps_server")
        validated_data["streaming_key"] = ivs_channel_data.get("streaming_key")
        user = CustomUser(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["username", "playback_url"]


class SelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email", "username", "playback_url", "rtmps_server", "streaming_key"]
