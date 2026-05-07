from email_validator import validate_email, EmailNotValidError
import re



class Validators:

    @staticmethod
    def validate_email(email):
        if not email:
            raise ValueError("Email é obrigatório.")

        try:
            validate_email(email)
        except EmailNotValidError:
            raise ValueError("Email inválido.")

    

    @staticmethod
    def validate_phone(phone):

        if not phone:

            raise ValueError("Telefone é obrigatório.")

        clean_phone = re.sub(r"\D", "", phone)

        if len(clean_phone) not in [10, 11]:

            raise ValueError("Telefone inválido.")

        if len(clean_phone) == 11 and clean_phone[2] != "9":

            raise ValueError("Celular inválido.")

        return clean_phone

