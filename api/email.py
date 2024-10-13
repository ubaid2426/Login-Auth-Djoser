from djoser import email


class ActivationEmail(email.ActivationEmail):
    template_name = 'api/activation.html'


class ConfirmationEmail(email.ConfirmationEmail):
    template_name = 'api/confirmation.html'


class PasswordResetEmail(email.PasswordResetEmail):
    template_name = 'api/password_reset.html'


class PasswordChangedConfirmationEmail(email.PasswordChangedConfirmationEmail):
    template_name = 'api/password_changed_confirmation.html'
