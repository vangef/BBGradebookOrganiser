import os, sys
from utils.inspector import hash_submissions, inspect_for_duplicate_hashes

CSV_DIR = os.path.join(os.getcwd(), 'csv')

def main():
    submissions_dir_name = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else exit(f'\nNo submissions dir name given. Provide the name as an argument.\n\nUsage: python {sys.argv[0]} [submissions dir name]\nExample: python {sys.argv[0]} AssignmentX\n')
    submissions_dir_path = os.path.join('BB_submissions', submissions_dir_name)
    if not os.path.isdir(submissions_dir_path):
        exit(f'Directory {submissions_dir_path} does not exist.\nMake sure "{submissions_dir_name}" exists in "BB_submissions".\n')
    else:
        hashes_csv_file_path = hash_submissions(submissions_dir_path)  # generate CSV file with hashes for all files (except for any 'excluded') & return path to CSV file for finding duplicate/suspicious hashes
        inspect_for_duplicate_hashes(hashes_csv_file_path)  # generate CSV file with files having duplicate/suspicious hashes


if __name__ == '__main__':    
    main()
