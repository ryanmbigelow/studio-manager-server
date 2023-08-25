from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from studiomanagerapi.models import Engineer

class EngineerView(ViewSet):
    """Studio Manager engineers typesview"""

    def retrieve(self, request, pk):
        """Gets an engineer by their pk

        Returns:
            Response --  single JSON serialized engineer dictionary
        """
        engineer = Engineer.objects.get(pk=pk)
        serializer = EngineerSerializer(engineer)
        return Response(serializer.data)

    def list(self, request):
        """Gets all engineers

        Returns:
            Response -- JSON serialized list of engineers
        """
        engineers = Engineer.objects.all()
        serializer = EngineerSerializer(engineers, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handles POST operations

        Returns:
            Response -- JSON serialized engineer instance
        """
        engineer = Engineer.objects.create(
            first_name=request.data["firstName"],
            last_name=request.data["lastName"],
            is_admin=request.data["isAdmin"],
            profile_picture=request.data["profilePicture"],
            uid=request.data["uid"],
        )
        serializer = EngineerSerializer(engineer)
        return Response(serializer.data)
    
    def update(self, request, pk):
        """Handles PUT requests for an engineer

        Returns:
            Response -- Empty body with 204 status code
        """
        engineer = Engineer.objects.get(pk=pk)
        engineer.first_name=request.data["firstName"]
        engineer.last_name=request.data["lastName"]
        engineer.is_admin=request.data["isAdmin"]
        engineer.profile_picture=request.data["profilePicture"]
        engineer.uid=request.data["uid"]
        engineer.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Handles DELETE requests for an engineer

        Returns:
            Response -- Empty body with 204 status code
        """
        engineer = Engineer.objects.get(pk=pk)
        engineer.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class EngineerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Engineer
        fields = ('id', 'first_name', 'last_name', 'is_admin', 'profile_picture', 'uid')
        depth: 2
