import json
from lib.data_loader import DataLoader


def perform_daily_load():
    data_loader = DataLoader()

    with open("elt_jobs.json", "r") as file:
        data = json.load(file)

    for key, job_config in data.items():
        print(f"========\nRUNNING JOB '{key}'...\n========")

        keboola_table_id = job_config["keboola_table_id"]
        postgres_schema_name = job_config["postgres_schema_name"]
        postgres_table_name = job_config["postgres_table_name"]

        # get df
        api_response = data_loader.invoke_api_call(keboola_table_id)
        df = data_loader.create_df_from_api(api_response)

        data_loader.truncate_table_in_postgres(
            postgres_schema_name + "." + postgres_table_name
        )
        data_loader.insert_data_into_postgres(
            df, postgres_table_name, postgres_schema_name
        )
        print(f"========\nJOB '{key}' COMPLETED.\n========\n")


if __name__ == "__main__":
    perform_daily_load()
