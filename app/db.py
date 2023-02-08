import csv
import pandas as pd

def read_log(log_file_name):
    with open(f"DB/{log_file_name}.csv", 'r') as f:
        data = pd.read_csv(f)
        return data.iloc[-1]

def write_log(log_file_name, user_input:dict):
    with open(f"DB/{log_file_name}.csv", 'a') as f:
        wr = csv.writer(f)
        wr.writerow(user_input.values())