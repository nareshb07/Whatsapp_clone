from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError



class SpaceValidator:
    """
    Validate that the password doesn't contain spaces
    """

    def validate(self, password, user=None):
        if " " in password:
            raise ValidationError(
                _("This password doesn't contain spaces"),
                code="password_have_spaces",
            )

    def get_help_text(self):
        return _("Your password should not have spaces ")
