from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import timedelta
from airflow.utils.dates import days_ago
import api_kafkaProducer

# Define your default arguments
default_args = {
    'owner': 'Uma Srikanth Reddy Koduru',
    'start_date': days_ago(0),
    'email': ['koduru@usf.edu'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Create your DAG
dag = DAG(
    'kafka',
    default_args=default_args,
    description='Data scheduler for Kafka producer',
    schedule_interval='0 1 * * *'  # This schedule interval runs the DAG daily at 1:00 AM
)

# Define your PythonOperator task
kafka_streaming_task = PythonOperator(
    task_id='kafka_stream',  # Task ID should be a string
    # Correct the function name if needed
    python_callable=api_kafkaProducer.api_Producer,
    dag=dag
)


kafka_streaming_task
