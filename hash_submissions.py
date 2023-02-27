import os, sys
from datetime import datetime
import csv
import hashlib


def hash_files_in_dir(dir_path: str, csv_suffix: str):
    os.makedirs('csv', exist_ok=True)
    csv_file_name = f'file_hashes_{csv_suffix}_{datetime.now().strftime("%Y%m%d-%H%M%S")}.csv'
    csv_file = os.path.join('csv', csv_file_name)

    with open(csv_file, 'w', newline='') as csvfile:      # Open the output CSV file for writing
        fieldnames = ['Student ID', 'file', 'sha256 hash']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for subdir, dirs, files in os.walk(dir_path):  # Loop through all files in the directory and generate hashes
            for file in files:
                if 'README.md' not in file:
                    directories = [d for d in os.path.abspath(subdir).split(os.path.sep)]  # list of directories in the file path

                    student_id = directories[directories.index(csv_suffix)+1]  # use the index of 'csv_suffix' which is the gradebook name, and get the next directory which is the student id 
                    filepath = os.path.join(subdir, file)
                    with open(filepath, 'rb') as f:
                        filehash = hashlib.sha256(f.read()).hexdigest()
                        writer.writerow({'Student ID': student_id, 'file': filepath, 'sha256 hash': filehash})


def main():
    submissions_dir_name = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else exit(f'\nNo submissions dir name given. Provide the name as an argument.\n\nUsage: python {sys.argv[0]} [submissions dir name]\n')
    submissions_dir = os.path.join('BB_submissions', submissions_dir_name)  # dir with extracted submissions
    if os.path.isdir(submissions_dir):
        hash_files_in_dir(submissions_dir, submissions_dir_name)
    else:
        exit(f'Directory {submissions_dir} does not exist.\nMake sure "{submissions_dir_name}" exists in "BB_submissions".')


if __name__ == '__main__':    
    main()