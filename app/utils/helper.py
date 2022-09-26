from passlib.context import CryptContext


class Helper:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def encrypt_password(cls, password):
        return cls.pwd_context.hash(password)

    @classmethod
    def verify_password(cls, password, enc_password):
        return cls.pwd_context.verify(password, enc_password)
