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
        # frontend sends an array of engineer ids
        print(request.data["engineerIds"])
        
        # engineers will be stored in this list
        engineers = []
        # each engineer from the array is appended to the engineer list by their pk
        for eng_id in request.data["engineerIds"]:
            engineers.append(Engineer.objects.get(pk=eng_id))
        # we get the session to match corresponding session engineers
        session = Session.objects.get(pk=request.data["sessionId"])
        # each time we create a new session engineer, we have to delete the old ones
        # from the corresponding session because it would otherwise create duplicates
        engineers_to_delete = SessionEngineer.objects.filter(session_id = session)
        for engineer in engineers_to_delete :
            engineer.delete()
        for eng in engineers:
            SessionEngineer.objects.create(
                engineer_id=eng,
                session_id=session,
            )
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
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
        # the session id is passed from the front end
        session = request.query_params.get('session_id', None)
        if session is not None:
            # Filter the SessionEngineer instances for the matching engineer and session
            session_engineer = SessionEngineer.objects.get(engineer_id=engineer, session_id=session)

            if session_engineer:
                session_engineer.delete()
                return Response(None, status=status.HTTP_204_NO_CONTENT)

        return Response({"detail": "SessionEngineer not found"}, status=status.HTTP_404_NOT_FOUND)


class SessionEngineerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionEngineer
        fields = ('id', 'engineer_id', 'session_id')
        depth: 2
