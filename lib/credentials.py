import keyring


class Credentials:
    """
    This class is used for init of Credentials used in this app.

    It uses the keyring library to store and retrieve credentials securely.

    How to use Keyring?:
    - there are two ways of using keyring
    - 1st - usage in terminal
        - keyring set SERVICE_NAME USERNAME
    - 2nd - usage in Python
        - keyring.set_password("SERVICE_NAME", "USERNAME", "PASSWORD")
    """

    def __init__(self):
        self.pg_user = "postgres"
        self.keboola_user = "keboola"

    def get_postgres_credentials(self):
        """
        Get PostgreSQL credentials from keyring and credentials class.

        :return: Credentials config.
        """
        password = keyring.get_password("POSTGRESQL", self.pg_user)
        if password is None:
            raise ValueError(f"Password for {self.pg_user} is not set in Keyring.")

        return {
            "host": "shortline.proxy.rlwy.net:14542",
            "database": "trezor",
            "user": self.pg_user,
            "password": password,
        }

    def get_keboola_api_credentials(self):
        """
        Get OpenAI credentials from keyring and credentials class.

        :return: OpenAI API secret key
        """
        secret_key = keyring.get_password("KEBOOLA", self.keboola_user)
        if secret_key is None:
            raise ValueError(
                f"Password for '{self.keboola_user}' is not set in Keyring."
            )

        return secret_key
