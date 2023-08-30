from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from studiomanagerapi.models import Session, Engineer

class SessionView(ViewSet):
    """Studio Manager session typesview"""

    def retrieve(self, request, pk):
        """Gets a session by its pk

        Returns:
            Response --  single JSON serialized session dictionary
        """
        session = Session.objects.get(pk=pk)
        serializer = SessionSerializer(session)
        return Response(serializer.data)

    def list(self, request):
        """Gets all sessions

        Returns:
            Response -- JSON serialized list of sessions
        """
        sessions = Session.objects.all()
        """filter by engineer id"""
        engineer = request.query_params.get('engineer_id', None)
        if engineer is not None:
                sessions = sessions.filter(engineer_id=engineer)
        """serialize all list requests"""
        serializer = SessionSerializer(sessions, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handles POST operations

        Returns:
            Response -- JSON serialized session instance
        """
        engineer = Engineer.objects.get(pk=request.data["engineerId"])
        session = Session.objects.create(
            artist=request.data["artist"],
            date=request.data["date"],
            start_time=request.data["startTime"],
            end_time=request.data["endTime"],
            engineer_id=engineer,
        )
        serializer = SessionSerializer(session)
        return Response(serializer.data)
    
    def update(self, request, pk):
        """Handles PUT requests for sessions

        Returns:
            Response -- Empty body with 204 status code
        """
        session = Session.objects.get(pk=pk)
        session.artist=request.data["artist"]
        session.date=request.data["date"]
        session.start_time=request.data["startTime"]
        session.end_time=request.data["endTime"]
        engineer = Engineer.objects.get(pk=request.data["engineerId"])
        session.engineer_id = engineer
        session.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Handles DELETE requests for sessions

        Returns:
            Response -- Empty body with 204 status code
        """
        session = Session.objects.get(pk=pk)
        session.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ('id', 'artist', 'date', 'start_time', 'end_time', 'engineer_id')
        depth = 2
