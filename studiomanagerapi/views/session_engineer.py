from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from studiomanagerapi.models import SessionEngineer, Session, Engineer

class SessionEngineerView(ViewSet):
    """Studio Manager session engineer typesview"""

    def retrieve(self, request, pk):
        """Gets a session engineer by their pk

        Returns:
            Response --  single JSON serialized session engineer dictionary
        """
        session_engineer = SessionEngineer.objects.get(pk=pk)
        serializer = SessionEngineerSerializer(session_engineer)
        return Response(serializer.data)

    def list(self, request):
        """Gets all session engineers

        Returns:
            Response -- JSON serialized list of session engineers
        """
        session_engineer = SessionEngineer.objects.all()
        serializer = SessionEngineerSerializer(session_engineer, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handles POST operations

        Returns:
            Response -- JSON serialized session engineer instance
        """
        engineer = Engineer.objects.get(pk=request.data["engineerId"])
        session = Session.objects.get(pk=request.data["sessionId"])
        session_engineer = SessionEngineer.objects.create(
            engineer_id=engineer,
            session_id=session,
        )
        serializer = SessionEngineerSerializer(session_engineer)
        return Response(serializer.data)
    
    def update(self, request, pk):
        """Handles PUT requests for session engineers

        Returns:
            Response -- Empty body with 204 status code
        """
        session_engineer = SessionEngineer.objects.get(pk=pk)
        engineer = Engineer.objects.get(pk=request.data["engineerId"])
        session_engineer.engineer_id = engineer
        session = Session.objects.get(pk=request.data["sessionId"])
        session_engineer.session_id = session
        session_engineer.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Handles DELETE requests for session engineers

        Returns:
            Response -- Empty body with 204 status code
        """
        engineer = Engineer.objects.get(pk=pk)
        session = request.query_params.get('session_id', None)
        if session is not None:
            # Filter the SessionEngineer instances for the matching engineer and session
            session_engineer = SessionEngineer.objects.get(engineer_id=engineer, session_id=session)

            if session_engineer:
                # Delete the first matching session_engineer instance
                session_engineer.delete()
                return Response(None, status=status.HTTP_204_NO_CONTENT)

        return Response({"detail": "SessionEngineer not found"}, status=status.HTTP_404_NOT_FOUND)

class SessionEngineerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionEngineer
        fields = ('id', 'engineer_id', 'session_id')
        depth: 2
