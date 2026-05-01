from accounts.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Promote a user to Admin by email"

    def add_arguments(self, parser):
        parser.add_argument("email", type=str)

    def handle(self, *args, **kwargs):
        email = kwargs["email"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            self.stderr.write(self.style.ERROR(f"No user found with email: {email}"))
            return

        self.stdout.write("\nAbout to promote this user:\n")
        self.stdout.write(f"  Email: {user.email}")
        self.stdout.write(f"  Current type: {user.type}")
        self.stdout.write(f"  is_staff: {user.is_staff}")
        self.stdout.write(f"  is_superuser: {user.is_superuser}\n")

        confirm = input("Are you sure? Type 'yes' to continue: ").strip().lower()
        if confirm != "yes":
            self.stdout.write(self.style.WARNING("Aborted."))
            return

        user.is_staff = True
        user.is_superuser = True
        user.save()

        self.stdout.write(self.style.SUCCESS("\nUser successfully promoted to ADMIN."))
