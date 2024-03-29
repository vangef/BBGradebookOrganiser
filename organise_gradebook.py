import os, sys

from utils.organiser import organise_gradebook, check_submissions_dir_for_compressed
from utils.settings import BB_GRADEBOOKS_DIR, BB_SUBMISSIONS_DIR


def main():
    gradebook_name = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else exit(f'\nNo gradebook name given. Provide the name as an argument.\n\nUsage: python {sys.argv[0]} [gradebook dir name]\n')
    gradebook_dir = os.path.join(BB_GRADEBOOKS_DIR, gradebook_name)  # gradebook from Blackboard with all submissions
    submissions_dir = os.path.join(BB_SUBMISSIONS_DIR, gradebook_name)  # target dir for extracted submissions

    abs_path = os.getcwd()  # absolute path of main/this script
    print(f'\nGradebook directory to organise:\n{os.path.join(abs_path, gradebook_dir)}', flush=True)
        
    organise_gradebook(gradebook_dir, submissions_dir)
    check_submissions_dir_for_compressed(submissions_dir) 


if __name__ == '__main__':    
    main()
