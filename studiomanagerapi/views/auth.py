from rest_framework.decorators import api_view
from rest_framework.response import Response
from studiomanagerapi.models import Engineer
from rest_framework import status

@api_view(['POST'])
def check_user(request):
    '''Checks to see if User has Associated Engineer Profile

    Method arguments:
      request -- The full HTTP request object
    '''
    uid = request.data['uid']

    # Use the built-in authenticate method to verify
    # authenticate returns the user object or None if no user is found
    engineer = Engineer.objects.filter(uid=uid).first()

    # If authentication was successful, respond with their token
    if engineer is not None:

        data = {
            'id': engineer.id,
            'uid': engineer.uid,
            'first_name': engineer.first_name,
            'last_name': engineer.last_name,
            'is_admin': engineer.is_admin,
            'profile_picture': engineer.profile_picture,
        }
        return Response(data)
    else:
        # Bad login details were provided. So we can't log the user in.
        data = { 'valid': False }
        return Response(data)


@api_view(['POST'])
def register_user(request):
    '''Handles the creation of a new engineer for authentication

    Method arguments:
      request -- The full HTTP request object
    '''

    engineer = Engineer.objects.create(
        first_name=request.data["firstName"],
        last_name=request.data["lastName"],
        is_admin=request.data["isAdmin"],
        profile_picture=request.data["profilePicture"],
        uid=request.data["uid"],
        )

    data = {
        'id': engineer.id,
        'uid': engineer.uid,
        'first_name': engineer.first_name,
        'last_name': engineer.last_name,
        'is_admin': engineer.is_admin,
        'profile_picture': engineer.profile_picture,
    }
 
    return Response(data)
