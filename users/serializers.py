from django.contrib.auth.models import User
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    # This is a special field declaration. It overrides the default.
    # It tells the serializer: "Accept a 'password' field in the incoming JSON,
    # but NEVER, EVER include it in the outgoing JSON response."
    # This is a critical security measure to prevent password hashes from ever
    # being accidentally sent back to the client.
    password = serializers.CharField(write_only=True)

    # --- Explanation of the inner `class Meta` ---
    # The inner `Meta` class is a convention in Django and DRF. It's used to provide
    # configuration and instructions to the main serializer class.
    # Think of it like this:
    # - The main class defines the "ingredients" (the data fields).
    # - The `Meta` class provides the "recipe instructions" (how the serializer should behave).
    # This separation is crucial because it cleanly separates the field definitions from the
    # configuration options (like which model to use or which fields to include),
    # preventing ambiguity and potential naming conflicts.
    class Meta:
        # This links the serializer to Django's built-in User model.
        # DRF will use this to automatically understand things like 'username'
        # and 'email' should be character fields.
        model = User     
        # These are the fields the "application form" requires from the user.
        # The client MUST provide a username, email, and password.
        fields = ['username', 'email', 'password']

    # This is the most important part of this serializer.
    # We are OVERRIDING the default 'create' method of the ModelSerializer.
    # WHY? Because the default method would save the password as plain text,
    # which is a catastrophic security vulnerability.
    def create(self, validated_data):
        # `validated_data` is a dictionary containing the clean data
        # (e.g., {'username': 'newuser', 'email': 'a@b.com', 'password': '...'})
        # after DRF has confirmed it's valid.

        # Step 1: Create a User instance, but DON'T save the password yet.
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )

        # Step 2: Use the special `set_password` method. This doesn't just
        # set the password; it runs it through Django's secure hashing
        # algorithm. The result is a long, irreversible string.
        # e.g., 'pbkdf2_sha256$390000$....'
        user.set_password(validated_data['password'])

        # Step 3 (Optional but good practice): Explicitly set the user as active.
        # In more complex scenarios, you might set this to `False` and require
        # the user to click an email confirmation link to activate their account.
        user.is_active = True
        # Step 4: Now that the password is a secure hash, save the
        # complete user object to the database.
        user.save()

        # Step 5: Return the newly created user object.
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        # Again, it's linked to the User model.
        model = User
        
        # This is the most important part. Notice what's INCLUDED and what's MISSING.
        # We are explicitly listing the fields that are SAFE to show to the public
        # or to the user themselves.
        #
        # - 'id': The user's unique primary key.
        # - 'username': The user's public name.
        # - 'email': The user's email address.
        #
        # CRUCIALLY, 'password' is NOT in this list. Because of this, even if you
        # tried to serialize a user object that has a password hash, this serializer
        # would simply ignore it. It acts as a filter to prevent sensitive data leaks.
        fields = ['id', 'username', 'email']
