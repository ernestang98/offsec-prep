#!/usr/bin/python3
# https://stackoverflow.com/questions/5442910/how-to-use-multiprocessing-pool-map-with-multiple-arguments
# https://medium.com/python-experiments/parallelising-in-python-mutithreading-and-mutiprocessing-with-practical-templates-c81d593c1c49

import datetime
import time

from multiprocessing import Pool

filenames = [i for i in range(15)]

def long_running_task(filename):
    time.sleep(1)
    print(f"{datetime.datetime.now()} finished: {filename}")
    
START = datetime.datetime.now()
with Pool(15) as mp_pool:
    mp_pool.map(long_running_task, filenames)
END = datetime.datetime.now()
print(END - START)


START = datetime.datetime.now()
for _file in filenames:
    long_running_task(_file)
END = datetime.datetime.now()
print(END - START)

filenames_multi_args = [(i, i+10) for i in range(15)]

def long_running_task_multi_args(filename, useless):
    time.sleep(1)
    print(f"{datetime.datetime.now()} finished: {filename}")
    print(f"Argument \"{useless}\" is useless")
    
START = datetime.datetime.now()
with Pool(15) as mp_pool:
    mp_pool.starmap(long_running_task_multi_args, filenames_multi_args)
END = datetime.datetime.now()
print(END - START)


START = datetime.datetime.now()
for _file in filenames_multi_args:
    long_running_task_multi_args(_file[0], _file[1])
END = datetime.datetime.now()
print(END - START)



