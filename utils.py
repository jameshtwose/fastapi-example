from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Define a function to create a hashed password
def get_password_hash(password: str) -> str:
    """Create a password hash.

    Parameters
    ----------
    password : str
        The password to hash.

    Returns
    -------
    str
        The hashed password.

    """
    return pwd_context.hash(password)


# Define a function to verify a password
def verify_password(plain_password, hashed_password) -> bool:
    """Verify a password.

    Parameters
    ----------
    plain_password : str
        The password to verify.
    hashed_password : str
        The hashed password to compare with.

    Returns
    -------
    bool
        True if the password is correct, False otherwise.

    """
    return pwd_context.verify(plain_password, hashed_password)
