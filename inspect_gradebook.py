import os, sys

from utils.inspector import generate_hashes_gradebook, generate_duplicate_hashes_gradebook
from utils.settings import BB_GRADEBOOKS_DIR


def main():
    gradebook_dir_name = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else exit(f'\nNo gradebook directory name given. Provide the name as an argument.\n\nUsage: python {sys.argv[0]} [gradebook dir name]\nExample: python {sys.argv[0]} AssignmentX\n')

    gradebook_dir_path = os.path.join(BB_GRADEBOOKS_DIR, gradebook_dir_name)
    if not os.path.exists(gradebook_dir_path):
        exit('[Info] Gradebook directory does not exist - nothing to inspect')
    if not os.listdir(gradebook_dir_path):  # if no files in gradebook dir
        exit(f'[Info] No files found in this gradebook - nothing to inspect')
    hashes_csv_file_path = generate_hashes_gradebook(gradebook_dir_path)  # generate CSV file with hashes for all files in gradebook & return path to CSV file for finding duplicate hashes
    generate_duplicate_hashes_gradebook(hashes_csv_file_path)  # generate CSV file with files having duplicate hashes


if __name__ == '__main__':
    main()
