from rest_framework import serializers

from profiles.models import UserProfile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'first_name', 'middle_name', 'last_name', 'email', 'date_of_birth',
                  'bio', 'created_at', 'updated_at']
