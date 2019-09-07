from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from helpers import SqlQueries

class LoadFactOperator(BaseOperator):

    ui_color = '#F98866'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 table="",
                 sql="",        
                 append_only=False,
                 *args, **kwargs):

        super(LoadFactOperator, self).__init__(*args, **kwargs)
        # Map params here
        # Example:
        # self.conn_id = conn_id
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.sql = sql
        self.append_only = append_only
        

    def execute(self, context):
        self.log.info('Starting fact loading operator')
        
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        if not self.append_only:
            self.log.info(f"Delete {self.table} fact table")
            redshift.run(f"DELETE FROM {self.table}")
        
        self.log.info(f"Insert data from staging tables into {self.table}")
        formatted_sql = getattr(SqlQueries, self.sql).format(self.table)
        redshift.run(formatted_sql)
        
        self.log.info("Fact loading operator complete")

