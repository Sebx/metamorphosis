
from contextlib import contextmanager
import multiprocessing as mp
from contextlib import asynccontextmanager

@contextmanager
def managed_resource(*args, **kwds):
    # Code to acquire resource, e.g.:
    resource = acquire_resource(*args, **kwds)
    try:
        yield resource
    finally:
        # Code to release resource, e.g.:
        release_resource(resource)

#with managed_resource(timeout=3600) as resource:
    # Resource is released at the end of this block,
    # even if code in the block raises an exception
    

@asynccontextmanager
async def get_connection():
    conn = await acquire_db_connection()
    try:
        yield conn
    finally:
        await release_db_connection(conn)

async def get_all_users():
    async with get_connection() as conn:
        return conn.query('SELECT ...')


#@contextmanager
#def example_manager(message):
#    print('Starting', message)
#    try:
#        yield
#    finally:
#        print('Done', message)

#with example_manager('printing Hello World'):
#    print('Hello, World!')


#@example_manager('running my function')
#def some_function():
#    print('Inside my function')


## https://docs.python.org/3/library/multiprocessing.html

#
 
#filename = "employees.txt"
#companyid_column = 3
#rate_column = 4
 
#def process_line(sdict, line):
#	val = line.split(',')
#	idx = int(val[companyid_column])
#	# avoid duplication using dictionary
#	if(idx not in sdict):
#    	sdict[idx] = val
 
#if __name__ == "__main__":
#    cores = 2
#	pool = mp.Pool(cores)
#	shared_dict = mp.Manager().dict()
	
#	#create jobs per file line
#	with open(filename) as file:
#    	jobs = [pool.apply_async(process_line, args=(shared_dict, line)) for line in file]
 
#	# wait for all jobs to finish
#	for job in jobs:
#    	job.get()
	
#	# get employees with rate < 0.151
#	condition = lambda val : float(val[rate_column]) < 0.151
#	employees = [value for key, value in shared_dict.items() if condition(value)]
	
#	# show results
#	print(employees)
	
#	#clean up
#	pool.close()
