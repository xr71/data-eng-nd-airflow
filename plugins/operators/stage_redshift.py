from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.hooks.postgres_hook import PostgresHook
from airflow.contrib.hooks.aws_hook import AwsHook

class StageToRedshiftOperator(BaseOperator):
    ui_color = '#358140'
    
    copy_sql_songs = """
        COPY {} FROM '{}'
        ACCESS_KEY_ID '{}'
        SECRET_ACCESS_KEY '{}'
        REGION '{}'
        {} 'auto';
    """
    
    copy_sql_events = """
        COPY {} FROM '{}'
        ACCESS_KEY_ID '{}'
        SECRET_ACCESS_KEY '{}'
        REGION '{}'
        FORMAT AS JSON 's3://udacity-dend/log_json_path.json';
    """

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 aws_conn_id="",
                 data_format="",
                 redshift_table="",
                 s3_path="",
                 aws_region="us-west-2",
                 *args, **kwargs):

        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        # Map params here
        # Example:
        # self.conn_id = conn_id

        self.redshift_conn_id = redshift_conn_id
        self.aws_conn_id = aws_conn_id
        self.data_format = data_format
        self.redshift_table = redshift_table
        self.s3_path = s3_path
        self.aws_region = aws_region
        self.execution_date = kwargs.get('execution_date')
        
    def execute(self, context):
        self.log.info('Starting Staging to Redshift Operator')
        aws = AwsHook(self.aws_conn_id)
        credentials = aws.get_credentials()
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        self.log.info("Clearing existing tables first")
        redshift.run(f"DELETE FROM {self.redshift_table};")
        
        self.log.info("Start copying files from S3")
        
        if self.redshift_table == "staging_events":
            formatted_sql = StageToRedshiftOperator.copy_sql_events.format(
                    self.redshift_table, 
                    self.s3_path, 
                    credentials.access_key,
                    credentials.secret_key, 
                    self.aws_region
                )
            
        if self.redshift_table == "staging_songs":
            formatted_sql = StageToRedshiftOperator.copy_sql_songs.format(
                    self.redshift_table, 
                    self.s3_path, 
                    credentials.access_key,
                    credentials.secret_key, 
                    self.aws_region,
                    self.data_format
                )
         
        
        redshift.run(formatted_sql)
        self.log.info("Finished copying from S3")
