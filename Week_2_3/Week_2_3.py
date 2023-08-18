import dask.dataframe as dd
from dask.distributed import Client

client = Client(n_workers=4)
client
