from rest_framework import status
from rest_framework.response import Response

from .constants import SUCCESS, REPEATED_ACTION


def success_response(name):
    return Response(
        {name: SUCCESS},
        status=status.HTTP_200_OK,
    )


def repeated_action_response(name):
    return Response(
        {name: REPEATED_ACTION},
        status=status.HTTP_400_BAD_REQUEST,
    )
