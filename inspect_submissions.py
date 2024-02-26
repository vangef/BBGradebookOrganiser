import os, sys

from utils.inspector import generate_hashes_submissions, generate_duplicate_hashes_submissions
from utils.settings import BB_SUBMISSIONS_DIR


def main():
    submissions_dir_name = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else exit(f'\nNo submissions directory name given. Provide the name as an argument.\n\nUsage: python {sys.argv[0]} [submissions dir name]\nExample: python {sys.argv[0]} AssignmentX\n')
    
    submissions_dir_path = os.path.join(BB_SUBMISSIONS_DIR, submissions_dir_name)
    if not os.path.exists(submissions_dir_path):
        exit('[Info] Directory does not exist - nothing to inspect')
    if not os.listdir(submissions_dir_path):  # if no files in dir
        exit(f'[Info] No files found in this submissions directory - nothing to inspect')    
    hashes_csv_file_path = generate_hashes_submissions(submissions_dir_path)  # generate CSV file with hashes for all files in submissions (except for any 'excluded') & return path to CSV file for finding duplicate hashes
    generate_duplicate_hashes_submissions(hashes_csv_file_path)  # generate CSV file with files having duplicate hashes


if __name__ == '__main__':    
    main()
