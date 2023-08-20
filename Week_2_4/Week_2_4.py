import os
from joblib import delayed
import yaml
import time
import pandas as pd
import dask.dataframe as dd
import dask
from dask.distributed import Client

#inspired by https://fennaf.gitbook.io/bfvm22prog1/data-processing/configuration-files/yaml

def configReader():
    """
    explanation: This function open config,yaml file 
    and fetch the gonfigue file information
    input: ...
    output: configue file
    """
    with open("config.yaml", "r") as inputFile:
        config = yaml.safe_load(inputFile)
    return config

def dataframe_maker(config, df_type='pandas', partition=False, parquet=False):
    start = time.time()
    file_directory, file_name = config.values()
    os.chdir(file_directory)

    if partition:

        # make a whle dataset from all the partition files
        df = dd.read_csv(
             os.path.join(file_directory, "*.part"), 
             dtype= {
                    "id1": "string[pyarrow]",
                    "id2": "string[pyarrow]",
                    "id3": "string[pyarrow]",
                    "id4": "int64",
                    "id5": "int64",
                    "id6": "int64",
                    "v1": "int64",
                    "v2": "int64",
                    "v3": "float64",
                    }
                    )

    if parquet:
        # make a whle dataset from all the partition files
        df = dd.read_parquet(
             os.path.join(file_directory, "*.parquet"),
             #columns=['id1', 'v1'],
             dtype= {
                    "id1": "string[pyarrow]",
                    "id2": "string[pyarrow]",
                    "id3": "string[pyarrow]",
                    "id4": "int64",
                    "id5": "int64",
                    "id6": "int64",
                    "v1": "int64",
                    "v2": "int64",
                    "v3": "float64",
                    }
                    )
    else:
        if df_type == 'pandas':
            df = pd.read_csv(file_name)

        else:
            df = dd.read_csv(file_name, dtype= {
                                                "id1": "string[pyarrow]",
                                                "id2": "string[pyarrow]",
                                                "id3": "string[pyarrow]",
                                                "id4": "int64",
                                                "id5": "int64",
                                                "id6": "int64",
                                                "v1": "int64",
                                                "v2": "int64",
                                                "v3": "float64",
                                                })
            #df = df.repartition(partition_size='100MB')
            #df.to_csv(file_directory, index=False)
            dd.to_parquet(df, file_directory, compression='snappy', engine='pyarrow')

    end = time.time()
    total_time = end - start
    return df, total_time


def perform_test(df):

    start = time.time()

    if isinstance(df, pd.DataFrame):
        sum_v1 = df.groupby('id1').v1.sum()
    else:
        sum_v1 = df.groupby('id1').v1.sum().persist().compute()

    end = time.time()
    return f'the data type {type(df)}\nThe running time is: {round(end-start, 3)}'

@delayed
def costly_simulation(df):

    start = time.time()

    if isinstance(df, pd.DataFrame):
        sum_v1 = df.groupby('id1').v1.sum()
    else:
        sum_v1 = df.groupby('id1').v1.sum().persist()

    end = time.time()
    return f'the data type {type(df)}\nThe running time is: {round(end-start, 3)}'


if __name__ == '__main__':

    df, reading_time = dataframe_maker(configReader(), 'dask', False, False)
    print(df.head())
    print(f'\nreading time is: {reading_time}')

    print(f'\n{perform_test(df)}')

    
    # Dask delayed computation
    print(f'\n{costly_simulation(df)}')
