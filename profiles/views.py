from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from profiles.models import UserProfile
from profiles.serializers import ProfileSerializer


@api_view(['GET'])
def profile(request, id):
    # Get the profile of the user
    try:
        # Try to get the current user
        current_user = UserProfile.objects.get(id=id)
    except UserProfile.DoesNotExist:
        return Response(
            {
                "success": False,
                "message": "Could not find your user profile",
                "data": None
            },
            status=status.HTTP_404_NOT_FOUND
        )
    if request.method == 'GET':
        # Serialize the profile
        serializer = ProfileSerializer(current_user)

        return Response(
            {
                "success": True,
                "message": "Profile returned successfully",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


@api_view(['POST'])
def create_profile(request):
    if request.method == 'POST':
        # Create a serializer
        serializer = ProfileSerializer(data=request.data)

        # Add the data to db
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Profile created successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        else:
            missing_keys = list(serializer.errors.keys())
            # error_messages = list(serializer.errors.values())
            #
            # error_detail = error_messages[0][0]
            #
            # user_already_exists = "already exists" in error_detail
            #
            # if user_already_exists:
            #     message_output = f"user with the same {' or '.join(missing_keys)} already exists"
            # else:
            #     message_output = f"required field(s) {missing_keys} are missing"

            message_output = f"there is an issue with your {' and '.join(missing_keys)}"

            return Response(
                {
                    "success": False,
                    "message": f"Could not create profile because {message_output}",
                    "data": None
                },
                status=status.HTTP_400_BAD_REQUEST
            )
    else:
        return Response(
            {
                "success": False,
                "message": "Method not allowed",
                "data": None
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


@api_view(['PATCH'])
def update_profile(request, id):
    # Get the profile of the user
    try:
        # Try to get the current user
        current_user = UserProfile.objects.get(id=id)
    except UserProfile.DoesNotExist:
        return Response(
            {
                "success": False,
                "message": "Could not find your user profile",
                "data": None
            },
            status=status.HTTP_404_NOT_FOUND
        )
    if request.method == 'PATCH':
        # Create a serializer
        serializer = ProfileSerializer(current_user, data=request.data, partial=True)

        # Add the data to db
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Profile updated successfully",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )
        else:
            missing_keys = list(serializer.errors.keys())
            return Response(
                {
                    "success": False,
                    "message": f"Could not update profile because required field(s) {missing_keys} are missing",
                    "data": None
                },
                status=status.HTTP_400_BAD_REQUEST
            )
