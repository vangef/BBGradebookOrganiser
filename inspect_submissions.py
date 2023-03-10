import os, sys
from utils.inspector import generate_hashes_submissions, generate_duplicate_hashes_submissions


def main():
    submissions_dir_name = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else exit(f'\nNo submissions dir name given. Provide the name as an argument.\n\nUsage: python {sys.argv[0]} [submissions dir name]\nExample: python {sys.argv[0]} AssignmentX\n')
    
    submissions_dir_path = os.path.join('BB_submissions', submissions_dir_name)
    # generate CSV file with hashes for all files in submissions (except for any 'excluded') & return path to CSV file for finding duplicate hashes
    hashes_csv_file_path = generate_hashes_submissions(submissions_dir_path)
    # generate CSV file with files having duplicate hashes
    generate_duplicate_hashes_submissions(hashes_csv_file_path)


if __name__ == '__main__':    
    main()
