import os, sys
import pandas as pd
from datetime import datetime
from utils.inspector import hash_submissions, suspicious_by_hash

CSV_DIR = os.path.join(os.getcwd(), 'csv')

def main():
    submissions_dir_name = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else exit(f'\nNo submissions dir name given. Provide the name as an argument.\n\nUsage: python {sys.argv[0]} [submissions dir name]\nExample: python {sys.argv[0]} AssignmentX\n')
    submissions_dir_path = os.path.join('BB_submissions', submissions_dir_name)
    if not os.path.isdir(submissions_dir_path):
        exit(f'Directory {submissions_dir_path} does not exist.\nMake sure "{submissions_dir_name}" exists in "BB_submissions".')
    else:
        hashes_csv_file_path = hash_submissions(submissions_dir_path)  # generate hashes for all files and return output csv file to load & find duplicate/suspicious hashes
        csv = pd.read_csv(hashes_csv_file_path)
        df = pd.DataFrame(csv)  # df with all files and their hashes
        df_suspicious = suspicious_by_hash(df)  # df with all files with duplicate/suspicious hash, excludes files from the same student id
        
        csv_name = f'{submissions_dir_name}_suspicious_{datetime.now().strftime("%Y%m%d-%H%M%S")}.csv'
        csv_out = os.path.join(CSV_DIR, csv_name)
        df_suspicious.to_csv(csv_out, index=False)
        print(f'[INFO] Created CSV file with duplicate/suspicious hashes in {submissions_dir_name}\nCSV file: {csv_out}')


if __name__ == '__main__':    
    main()
