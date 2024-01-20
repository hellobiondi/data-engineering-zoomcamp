#!/usr/bin/env python
# coding: utf-8

from time import time
import pandas as pd
from sqlalchemy import create_engine
import argparse
import os

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    file_name = 'output'
    CHUNKSIZE = 100000

    # download file
    os.system(f"wget {url} -O {file_name}.parquet")

    # convert parquet to csv
    pd.read_parquet(f'{file_name}.parquet').to_csv(f'{file_name}.csv')

    # create engine
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    df_iter = pd.read_csv(f'{file_name}.csv', iterator=True, chunksize=CHUNKSIZE)

    df = next(df_iter)

    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
    df.to_sql(name=table_name, con=engine, if_exists='append')


    while True:
        try:
            t_start = time()
            df = next(df_iter)

            df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
            df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)

            df.to_sql(name=table_name, con=engine, if_exists='append')

            t_end = time()

            print(f'inserted another chunk of size {CHUNKSIZE}, took {(t_end - t_start):.2f} seconds')

        except StopIteration:
            print("Finished ingesting data into the postgres database")
            break

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', required=True, help='user name for postgres')
    parser.add_argument('--password', required=True, help='password for postgres')
    parser.add_argument('--host', required=True, help='host for postgres')
    parser.add_argument('--port', required=True, help='port for postgres')
    parser.add_argument('--db', required=True, help='database name for postgres')
    parser.add_argument('--table_name', required=True, help='name of the table where we will write the results to')
    parser.add_argument('--url', required=True, help='url of the csv file')

    args = parser.parse_args()

    main(args)
