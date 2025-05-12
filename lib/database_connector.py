from abc import ABC, abstractmethod
from sqlalchemy.engine import Engine
from sqlalchemy import create_engine
from sqlalchemy import text
import pandas as pd


class BaseDatabaseConnector(ABC):
    """
    Database connector is the main class for connecting to database. It provides a common interface for
    connecting to a database and executing queries. It also provides a method for closing the connection. Could also
    be used for connecting to multiple databases.

    :param creds: Dictionary containing database credentials.
    """

    def __init__(self, creds: dict = None):
        self.credential_config = creds
        self.engine: Engine = self.create_engine()

    @abstractmethod
    def create_engine(self) -> Engine:
        """Creates and returns a database engine for the specific database type."""
        pass

    def read_from_db(self, query: str) -> pd.DataFrame:
        """Executes an SQL query and returns the results as a DataFrame."""
        print(f"Running query: {query}")
        return pd.read_sql(query, self.engine)

    def execute_sql_query(self, query: str):
        """Executes an SQL query without returning results."""
        print(f"Executing query: {query}")
        try:
            with self.engine.connect() as connection:
                connection.execute(text(query))
                connection.commit()
        except Exception as e:
            print(f"Error executing query: {e}")
            raise

    def close(self):
        """Closes the database connection."""
        if self.engine:
            self.engine.dispose()
            self.engine = None


class PostgresConnector(BaseDatabaseConnector):
    """PostgreSQL specific connector class that inherits from BaseDatabaseConnector."""

    def create_engine(self) -> Engine:
        creds = self.credential_config
        url = f"postgresql+psycopg2://{creds['user']}:{creds['password']}@{creds['host']}/{creds['database']}"
        connection = create_engine(url)
        return connection
