from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

#This generates link for the activation
class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.emailConfirmed)
        )

accountActivationToken = AccountActivationTokenGenerator()
