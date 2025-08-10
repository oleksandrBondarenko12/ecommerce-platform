# This file contains the logic that handles requests and returns responses.
# A view is a function or class that takes a web request and returns a web
# response. Think of these views as the public-facing "desks" in your application's
# office. Each desk has a specific purpose (e.g., registration, profile viewing)
# and a set of rules about who can access it.

from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import RegisterSerializer, UserSerializer
from django.contrib.auth.models import User


# This is the "New User Registration Desk".
class RegisterView(generics.CreateAPIView):
    # `generics.CreateAPIView` is a pre-built "generic" view from DRF.
    # It's specifically designed to handle POST requests for creating a new object.
    # By inheriting from it, we get all the logic for handling a creation request
    # for free, without having to write it ourselves.

    # `queryset`: Even though we are creating a user, not listing them, generic
    # views need to know what model they are operating on. This tells the view
    # that any operations it performs are related to the `User` model objects.
    queryset = User.objects.all()

    # `serializer_class`: This is the most important instruction for this view.
    # It tells the view: "When you receive data to create a new user, you MUST
    # use the `RegisterSerializer` to validate and process that data."
    # The view delegates the "how-to-create" logic to the serializer.
    serializer_class = RegisterSerializer
    
    # `permission_classes`: This sets the security rules for this desk.
    # `permissions.AllowAny` means that ANYONE, even an unauthenticated visitor,
    # is allowed to access this view. This is essential for a registration endpoint,
    # as new users don't have an account yet.
    permission_classes = [permissions.AllowAny]


# This is the "View Your Personal Profile Desk".
class ProfileView(generics.RetrieveAPIView):
    # `generics.RetrieveAPIView` is another pre-built view. It's designed to
    # handle GET requests for fetching a single object instance.

    # `serializer_class`: This tells the view: "When you have a user object ready
    # to be sent to the client, you MUST use the `UserSerializer` to format it."
    # This ensures that only the safe fields ('id', 'username', 'email') are returned,
    # and sensitive data like the password hash is never exposed.
    serializer_class = UserSerializer

    # `permission_classes`: The security rules here are much stricter.
    # `permissions.IsAuthenticated` means that a user MUST be successfully
    # authenticated (i.e., they must provide a valid JWT token) to access this view.
    # If they are not, they will receive a "401 Unauthorized" error.
    permission_classes = [permissions.IsAuthenticated]

    # This is a custom method we are overriding.
    # By default, a `RetrieveAPIView` expects to find a primary key (like 'pk' or 'id')
    # in the URL (e.g., /api/users/5/). It uses that key to fetch the object.
    # Our URL is simply `/api/profile/`, so there's no ID in the URL.
    # We override `get_object` to tell Django a different way to find the object.
    def get_object(self):
        # Instead of looking for a `pk` in the URL, we are telling the view:
        # "The object you need to show is the user who is making this request."
        # The `self.request.user` object is automatically attached to the request
        # by Django's AuthenticationMiddleware after it successfully validates
        # the user's JWT token. This is a secure and convenient way to get the
        # currently logged-in user.
        return self.request.user
