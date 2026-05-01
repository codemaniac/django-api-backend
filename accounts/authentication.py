from clerk_backend_api import AuthenticateRequestOptions, Clerk, authenticate_request
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import authentication, exceptions


User = get_user_model()


class ClerkAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None

        try:
            request_state = authenticate_request(
                request,
                AuthenticateRequestOptions(
                    secret_key=settings.CLERK_API_SECRET_KEY,
                ),
            )
        except Exception as exc:
            raise exceptions.AuthenticationFailed("Invalid authentication token.") from exc

        if not request_state.is_signed_in:
            raise exceptions.AuthenticationFailed("User is not signed in.")

        payload = request_state.payload or {}
        clerk_user_id = payload.get("sub")
        if not clerk_user_id:
            raise exceptions.AuthenticationFailed("Missing user identifier in token.")

        email = None
        email = payload.get("email")
        if not email:
            try:
                with Clerk(bearer_auth=settings.CLERK_API_SECRET_KEY) as clerk:
                    user_data = clerk.users.get(user_id=clerk_user_id)
                    primary_email_id = user_data.primary_email_address_id
                    primary_email = next(
                        (
                            item
                            for item in user_data.email_addresses
                            if item.id == primary_email_id
                        ),
                        None,
                    )
                    email = primary_email.email_address if primary_email else None
            except Exception as e:
                raise exceptions.AuthenticationFailed("Could not fetch Clerk user.") from e

        if not email:
            raise exceptions.AuthenticationFailed("Could not fetch user email id.")

        user, _ = User.objects.get_or_create(
            username=clerk_user_id,
            defaults={"email": email},
        )

        if user.email != email:
            user.email = email
            user.save(update_fields=["email"])

        return (user, None)
