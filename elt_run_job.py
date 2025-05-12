import json
from lib.data_loader import DataLoader


def run_job(elt_job_list=None):
    data_loader = DataLoader()

    with open("elt_jobs.json", "r") as file:
        data = json.load(file)

    for job in elt_job_list:
        try:
            job_config = data[job]
        except KeyError:
            print(f"Job '{job}' not found in configuration.")
            break

        print(f"========\nRUNNING JOB '{job}'...\n========")

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

        print(f"========\nJOB '{job}' COMPLETED.\n========\n")


if __name__ == "__main__":
    run_job(["products"])
