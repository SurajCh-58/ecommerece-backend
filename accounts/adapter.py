from allauth.account.adapter import DefaultAccountAdapter
from allauth.core.internal.cryptokit import generate_user_code

class CustomAccountAdapter(DefaultAccountAdapter):

    def generate_email_verification_code(self):
        return generate_user_code(numeric=True,dashed=False,length=6)
    
    def generate_password_reset_code(self):
        return generate_user_code(numeric=True,dashed=False,length=6)