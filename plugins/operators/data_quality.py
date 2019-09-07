from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id = "",
                 loaded_tables = [],
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        # Map params here
        # Example:
        # self.conn_id = conn_id
        self.redshift_conn_id = redshift_conn_id
        self.loaded_tables = loaded_tables

    def execute(self, context):
        self.log.info('Starting Data Quality Check')
        
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        # loaded_tables is a list of tables in redshift
        for table in self.loaded_tables:
            records = redshift.get_records("SELECT COUNT(*) FROM {}".format(table))
            self.log.info(table, records, records[0], records[0][0])
            
            if len(records) < 1 or len(records[0]) < 1:
                self.log.error("{} returned no results".format(table))
                raise ValueError("Data quality check failed. {} returned no results".format(table))
                
            num_records = records[0][0]
            if num_records == 0:
                self.log.error("No records present in destination table {}".format(table))
                raise ValueError("No records present in destination {}".format(table))
                
            # finally
            self.log.info("Data quality on table {} check passed with {} records".format(table, num_records))
        
        