from rest_framework import generics, serializers
from .models import Profile


class ProfileView(generics.RetrieveUpdateAPIView):
    class ProfileSerializer(serializers.ModelSerializer):
        class Meta:
            model = Profile
            fields = [
                "first_name",
                "last_name",
            ]

    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user.profile
