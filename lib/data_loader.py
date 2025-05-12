import requests
import pandas as pd
from io import StringIO

from requests import Response

from lib import credentials
from lib import database_connector


class DataLoader:
    """Main class for handling API, data loading."""

    def __init__(self):
        # Get credentials for connections
        pg_creds = credentials.Credentials().get_postgres_credentials()
        self.keboola_creds = credentials.Credentials().get_keboola_api_credentials()

        # Create connections
        postgres_conn = database_connector.PostgresConnector(pg_creds)

        # Output connections
        self.postgres_conn = postgres_conn

        # API URL
        self.api_url = "https://connection.eu-central-1.keboola.com/v2/storage/tables"

        print("DataLoader successfully initialized.")

    def invoke_api_call(self, table_id: str):
        """
        Invoke API call to Keboola and return the response.

        :return: Response from the API call.
        """

        url = f"{self.api_url}/{table_id}/data-preview/"
        headers = {"X-StorageApi-Token": self.keboola_creds, "Accept-encoding": "gzip"}

        # invoke api call
        response = requests.get(url, headers=headers)

        # read response, if response is 200 all good if not throw exception
        if response.status_code == 200:
            return response.text
        else:
            raise Exception(f"API call failed with status code {response.status_code}")

    @staticmethod
    def create_df_from_api(response: Response):
        """
        Create a DataFrame from the API response.

        :param response: API response.

        :return: DataFrame created from the API response.
        """

        # read df, convert cols to lowercase and return df
        df = pd.read_csv(StringIO(response))
        df.columns = df.columns.str.lower()
        return df

    def truncate_table_in_postgres(self, table_name: str):
        """
        Truncate a table in Postgres.

        :param table_name: Name of the table to truncate.

        :return: None
        """

        # truncate table in postgres
        query = f"TRUNCATE TABLE {table_name};"
        self.postgres_conn.execute_sql_query(query)
        print(f"Table {table_name} truncated in Postgres.")

    def insert_data_into_postgres(
        self, df: pd.DataFrame, table_name: str, schema_name: str
    ):
        """
        Run a query on Postgres and return the result as a DataFrame.

        :param schema_name:
        :param table_name:
        :param df:

        :return: df - Result of the query as a DataFrame.
        """

        # Insert data into Postgres
        df.to_sql(
            name=table_name,
            con=self.postgres_conn.engine,
            schema=schema_name,
            if_exists="append",
            index=False,
        )
        print(f"Data inserted into {table_name} table in Postgres.")
