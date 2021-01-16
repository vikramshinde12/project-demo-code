import os
import yaml
import datetime
import airflow
from airflow import DAG
from utils import utils
from airflow.operators.bash_operator import BashOperator
from utils.logging import get_logging_client

logging = get_logging_client()


def create_dag(dag_id, schedule, default_args, gcloud_function_url):
    with DAG(
            dag_id=dag_id,
            schedule_interval=schedule,
            default_args=default_args,
            description='Affiliate Window API data retrieval schedule',
            dagrun_timeout=datetime.timedelta(minutes=60)
    ) as dag:
        bash_operator = BashOperator(
            task_id='temp',
            bash_command='curl {0} -H "Authorization: bearer $(gcloud auth print-identity-token)"'.format(
                gcloud_function_url),
            dag=dag
        )
    return dag


default_args = {
    'start_date': airflow.utils.dates.days_ago(0),
    'retries': 1,
    'retry_delay': datetime.timedelta(minutes=5)
}

directory_path = os.path.dirname(__file__)
application_configuration_file_path = os.path.join(directory_path, 'conversion.yaml')

logging.info('Airflow directory path of zip={}'.format(directory_path))

application_configuration_file = utils.get_file_from_zip(application_configuration_file_path)
application_configuration = yaml.safe_load(application_configuration_file)

for processing_group in application_configuration['airflow']['processing_groups']:
    dag_id = processing_group['id']
    globals()[dag_id] = create_dag(
        dag_id,
        processing_group['schedule'],
        default_args,
        processing_group['gcloud_function_url']
    )