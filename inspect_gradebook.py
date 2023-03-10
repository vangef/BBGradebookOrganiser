import os, sys
from utils.inspector import generate_hashes_gradebook, generate_duplicate_hashes_gradebook


def main():
    gradebook_dir_name = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else exit(f'\nNo gradebook dir name given. Provide the name as an argument.\n\nUsage: python {sys.argv[0]} [gradebook dir name]\nExample: python {sys.argv[0]} AssignmentX\n')

    gradebook_dir_path = os.path.join('BB_gradebooks', gradebook_dir_name)
    # generate CSV file with hashes for all files in gradebook & return path to CSV file for finding duplicate hashes
    hashes_csv_file_path = generate_hashes_gradebook(gradebook_dir_path)
    # generate CSV file with files having duplicate hashes
    generate_duplicate_hashes_gradebook(hashes_csv_file_path)


if __name__ == '__main__':
    main()