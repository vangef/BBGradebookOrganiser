import os
from datetime import datetime
import csv
import hashlib
import pandas as pd
from functools import partial

from utils.settings import CSV_DIR


def load_excluded_filenames(submissions_dir_name: str) -> list[str]:  # helper function for hashing all files
    csv_file_path = os.path.join(CSV_DIR, f'{submissions_dir_name}_excluded.csv')
    if not os.path.exists(csv_file_path):  # if csv file with excluded file names for submission does not exist
        print(f'[WARNING] Cannot find CSV file with list of excluded file names: {csv_file_path}\n[INFO] All files will be hashed & inspected')
        return []  # return empty list to continue without any excluded file names
    else:  # if csv file with excluded file names for submission exists
        try:            
            df = pd.read_csv(csv_file_path)
            filename_list = df['exclude_filename'].tolist()  # get the values of the 'filename' column as a list
            filename_list = [ f.lower() for f in filename_list ]  # convert to lowercase for comparison with submission files
            print(f'[INFO] Using CSV file with list of excluded file names: {csv_file_path}')
            return filename_list
        except Exception as e:  # any exception, print error and return empty list to continue without any excluded file names
            print(f'[WARNING] Unable to load / read CSV file with list of excluded file names: {csv_file_path}\n[INFO] All files will be hashed & inspected')
            print(f'[INFO] Error message: {e}')
            return []


def get_hashes_in_dir(dir_path: str, excluded_filenames: list = []) -> list:  # helper function for hashing all files
    hash_list = []
    for subdir, dirs, files in os.walk(dir_path):  # loop through all files in the directory and generate hashes
        for filename in files:
            if filename.lower() not in excluded_filenames:  # convert to lowercase for comparison with excluded files & do not hash if in the excluded list
                filepath = os.path.join(subdir, filename)
                with open(filepath, 'rb') as f: 
                    filehash = hashlib.sha256(f.read()).hexdigest()
                    if filehash != 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855':  # do not include hashes of empty files
                        hash_list.append({ 'filepath': filepath, 'filename': filename, 'sha256 hash': filehash})
    return hash_list


def generate_hashes_gradebook(gradebook_dir_path: str) -> str:  # main function for hashing all files in gradebook
    gradebook_dir_name = os.path.abspath(gradebook_dir_path).split(os.path.sep)  # get name of gradebook by separating path and use rightmost part
    if not os.path.isdir(gradebook_dir_path):
        exit(f'Directory {gradebook_dir_path} does not exist.\nMake sure "{gradebook_dir_name}" exists in "BB_gradebooks".\n')
    
    dicts_with_hashes_list = get_hashes_in_dir(gradebook_dir_path)
    for hash_dict in dicts_with_hashes_list:
        student_id = hash_dict['filename'].split('_attempt_')[0].split('_')[-1]
        del hash_dict['filepath']
        hash_dict.update({'Student ID': student_id})

    os.makedirs(CSV_DIR, exist_ok=True)
    csv_file_name = f'{gradebook_dir_name}_gradebook_file_hashes_{datetime.now().strftime("%Y%m%d-%H%M%S")}.csv'
    csv_file_path = os.path.join(CSV_DIR, csv_file_name)

    with open(csv_file_path, 'w', newline='') as csvfile:  # open the output CSV file for writing
        fieldnames = ['Student ID', 'filename', 'sha256 hash']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(dicts_with_hashes_list)
    print(f'[INFO] Created CSV file with all files & hashes in gradebook: {gradebook_dir_name}\nCSV file: {csv_file_path}')
    return csv_file_path


def generate_hashes_submissions(submissions_dir_path: str) -> str:  # main function for hashing all files in submissions
    submissions_dir_name = os.path.abspath(submissions_dir_path).split(os.path.sep)[-1]  # get name of submission/assignment by separating path and use rightmost part
    if not os.path.isdir(submissions_dir_path):
        exit(f'Directory {submissions_dir_path} does not exist.\nMake sure "{submissions_dir_name}" exists in "BB_submissions".\n')

    excluded_filenames = load_excluded_filenames(submissions_dir_name)
    dicts_with_hashes_list = []
    for student_dir_name in os.listdir(submissions_dir_path):  # loop through each student dir to get hashes for all files per student
        student_dir_path = os.path.join(submissions_dir_path, student_dir_name)
        student_dicts_with_hashes_list = get_hashes_in_dir(student_dir_path, excluded_filenames)  # dict with hashes for all student files - except for 'excluded' file names
        student_dicts_list = []
        for hash_dict in student_dicts_with_hashes_list:
            hash_dict.update({'Student ID': student_dir_name})  # update hash records with student id
            student_dicts_list.append(hash_dict)  # append file dict to student list of dict for csv export
    
        dicts_with_hashes_list.append(student_dicts_list)  # append student hashes to main list with all submissions

    os.makedirs(CSV_DIR, exist_ok=True)
    csv_file_name = f'{submissions_dir_name}_submissions_file_hashes_{datetime.now().strftime("%Y%m%d-%H%M%S")}.csv'
    csv_file_path = os.path.join(CSV_DIR, csv_file_name)
    
    with open(csv_file_path, 'w', newline='') as csvfile:  # open the output CSV file for writing
        fieldnames = ['Student ID', 'filepath', 'filename', 'sha256 hash']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for student_dict in dicts_with_hashes_list:
            writer.writerows(student_dict)
    print(f'[INFO] Created CSV file with all files & hashes for submissions in: {submissions_dir_name}\nCSV file: {csv_file_path}')
    return csv_file_path
   

def generate_duplicate_hashes_generic(hashes_csv_file_path: str, drop_columns: list[str]):
    csv = pd.read_csv(hashes_csv_file_path)
    df = pd.DataFrame(csv)  # df with all files and their hashes
    df_clean = df.drop(columns=drop_columns)  # clear not needed columns
    duplicate_hash = df_clean.loc[df_clean.duplicated(subset=['sha256 hash'], keep=False), :]  # all files with duplicate hash - incl. files from the same student id
    # agg() for 'Student ID' True if more than 1 in groupby (= files with the same hash by multiple student ids)
    # False if unique (= files from the same student id with the same hash)
    hash_with_multiple_student_ids = duplicate_hash.groupby('sha256 hash').agg(lambda x: len(x.unique())>1)
    
    # list with duplicate hashes - only if different student id (doesn't include files from same student id)
    duplicate_hashes_list = hash_with_multiple_student_ids[hash_with_multiple_student_ids['Student ID']==True].index.to_list()
    
    files_with_duplicate_hash = df[df['sha256 hash'].isin(duplicate_hashes_list)]  # df with all files with duplicate hash, excludes files from the same student id
    df_duplicate = files_with_duplicate_hash.sort_values(['sha256 hash', 'Student ID'])  # sort before output to csv
    
    gradebook_or_submissions_str = os.path.basename(hashes_csv_file_path).split('_file_hashes_')[0].split('_')[-1]  # 'gradebook' or 'submissions' depending on which files hashes csv is read 
    assignment_name = os.path.basename(hashes_csv_file_path).split(f'_{gradebook_or_submissions_str}_')[0]
    csv_out = hashes_csv_file_path.rsplit('_', 1)[0].replace('file_hashes', 'duplicate_') + datetime.now().strftime("%Y%m%d-%H%M%S") + '.csv'
    try:
        df_duplicate.to_csv(csv_out, index=False)
        print(f'[INFO] Created CSV file with duplicate hashes in {gradebook_or_submissions_str}: {assignment_name}\nCSV file: {csv_out}')
    except Exception as e:
        exit(f'[ERROR] Something went wrong while trying to save csv file with duplicate hashes\nError message: {e}')

# partials for generate_duplicate_hashes_generic(), setting the appropriate drop_columns for gradebook / submissions 
generate_duplicate_hashes_gradebook = partial(generate_duplicate_hashes_generic, drop_columns=['filename'])
generate_duplicate_hashes_submissions = partial(generate_duplicate_hashes_generic, drop_columns=['filepath', 'filename'])
