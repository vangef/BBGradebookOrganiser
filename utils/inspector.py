import os
from datetime import datetime
import csv
import hashlib
import pandas as pd

CSV_DIR = os.path.join(os.getcwd(), 'csv')

def get_hashes_in_dir(dir_path: str) -> list:
    hash_list = []
    for subdir, dirs, files in os.walk(dir_path):  # Loop through all files in the directory and generate hashes
        for file in files:
            filepath = os.path.join(subdir, file)
            with open(filepath, 'rb') as f:
                filehash = hashlib.sha256(f.read()).hexdigest()
                hash_list.append({ 'file': filepath, 'sha256 hash': filehash})
    return hash_list


def hash_submissions(submissions_dir_path: str):
    os.makedirs(CSV_DIR, exist_ok=True)

    submissions_dir_name = os.path.abspath(submissions_dir_path).split(os.path.sep)[-1]
    csv_file_name = f'{submissions_dir_name}_file_hashes_{datetime.now().strftime("%Y%m%d-%H%M%S")}.csv'
    csv_file_path = os.path.join(CSV_DIR, csv_file_name)
    with open(csv_file_path, 'w', newline='') as csvfile:      # Open the output CSV file for writing
        fieldnames = ['Student ID', 'file', 'sha256 hash']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for student_dir_name in os.listdir(submissions_dir_path):
            student_dir_path = os.path.join(submissions_dir_path, student_dir_name)
            hashes_dict = get_hashes_in_dir(student_dir_path)        
            for d in hashes_dict:
                d.update({'Student ID': student_dir_name})  # update hash records with student id
            writer.writerows(hashes_dict)
    return csv_file_path

def get_suspicious_hashes(df: pd.DataFrame) -> list:
    drop_columns = ['file']
    df = df.drop(columns=drop_columns).sort_values('sha256 hash')  # clear not needed colums & sort by hash
    duplicate_hash = df.loc[df.duplicated(subset=['sha256 hash'], keep=False), :]  # all files with duplicate hash - incl. files from the same student id

    hash_with_multiple_student_ids = duplicate_hash.groupby('sha256 hash').agg(lambda x: len(x.unique())>1)  # true if more than 1 unique student ids (= multiple student ids with same hash), false if unique (= same student id re-submitting with the same hash)

    suspicious_hashes_list = hash_with_multiple_student_ids[hash_with_multiple_student_ids['Student ID']==True].index.to_list()  # list with duplicate hashes - only if different student id (doesn't include attempts from same student id)
    return suspicious_hashes_list  


def suspicious_by_hash(df: pd.DataFrame) -> pd.DataFrame:
    suspicious_hashes_list = get_suspicious_hashes(df)

    files_with_suspicious_hash = df[df['sha256 hash'].isin(suspicious_hashes_list)]  # excluding duplicate from same student id
    return files_with_suspicious_hash.sort_values(['sha256 hash', 'Student ID'])
     
