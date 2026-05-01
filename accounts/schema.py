from drf_spectacular.extensions import OpenApiAuthenticationExtension


class ClerkAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = "accounts.authentication.ClerkAuthentication"
    name = "ClerkBearerAuth"

    def get_security_definition(self, auto_schema):
        return {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Clerk session token passed as Bearer token in the Authorization header.",
        }
