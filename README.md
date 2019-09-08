# Udacity Project - Data Engineer - Data Pipelines with Airflow

## Introduction
Sparkify is a streaming song company that stores its event logs in JSON format on S3. To make these large semi-structured files usable for anlytics and downstream applications, we will be transforming the files using Spark (SparkSQL) and then loading the files back into S3 as Parquet files.

## Directory Structure
This directory contains two folders:  

The first folder is the `dags` folder
  * Inside this folder, you will find just the `main_dag.py` file. This dag file defines the entire workflow structure of this project.
    * First, upon execution, we start with the staging operator, which copies JSON files from S3 to Redshift. This is done for both `events` and `songs` which are stored at s3://udacity-dend/log_data and at s3://udacity-dend/song_data respectively. 
    * When the staging operators are completed successfully (that is, without failure), we proceed to the FACT loading stage
    * When the FACT loading stage finishes successully, the pipeline proceeds to the DIM loading stage
    * The DIM loading stage will create four different tables and upon successful completion, the pipeline will perform a data quality check run, ensuring that none of the previous tables have zero records
    
  
The second folder is the `plugins` folder, which also contains our reusable Airlofw Operators as well as our SQL Helper Class
  * Within the first folder called helpers, we have all of INSERT ETL SQL scripts, which will be used by our operators and called by our DAG
  * Within the second folder called operators, we have three files:
    * The load_dimension.py file creates the DIM tables in our DAG
    * The load_fact.py file creates the FACT table in our DAG
    * The stage_redshift.py file creates the COPY command that moves our JSON files from S3 to Redshift

## Instructions
  * `git clone` this repository and `cd` into the directory
  * to run this Airflow dag, I suggest that you have Airflow running locally such as in Docker 
    * another option is to run it in a managed environment, such as Google Cloud's CloudComposer
  * go through the `operators` folder to really understand reusable components that are used to build the DAG
  * OPTIONAL: go through the sql_queries.py file in the helpers folder within plugins folder to see the ETL statements
  * go through the main dag file in the dags folder and read through the components and most importantly, look at the way the dependency network graph is built at the end
  * launch the airflow scheduler and webserver (if applicable) and navigate to the web UI
    * here, it is crucial to put in your credentials for AWS
    * it is also crucial to put in your credentials for a Redshift host
  * navigate the DAGS tab of the web GUI and turn on the dag
  
  
