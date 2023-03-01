import os, shutil, re
from utils.extractor import extract_file_to_dir

BAD_DIR_NAME = '__BAD__'

def remove_trailing_spaces_from_filenames(gradebook_dir):
    for filename in os.listdir(gradebook_dir):
        if BAD_DIR_NAME not in filename:
            name, ext = os.path.splitext(filename)  # separate file name from extension
            if name != name.rstrip():
                new_filename = name.rstrip() + ext  # remove trailing spaces from file name and combines with extension
                new_file_path = os.path.join(gradebook_dir, new_filename)
                old_file_path = os.path.join(gradebook_dir, filename)
                os.rename(old_file_path, new_file_path)  # rename file


def validate_gradebook_dir_name(src_dir):
    if not os.path.isdir(src_dir):  # check if it exists and is a directory
        print(f"\n[Error] Incorrect directory: {src_dir}\n[Info] Make sure the directory exists in 'BB_gradebooks'")
        exit()
    if not os.listdir(src_dir):  # check if there are any files in the directory
        print(f'\n[Info] No files found in this gradebook - nothing to organise')
        exit()
    if len(os.listdir(src_dir)) == 1 and BAD_DIR_NAME in os.listdir(src_dir):  # if there is 1 file/directory and it is the 'BAD' directory
        print(f'\n[Info] Gradebook has only invalid compressed files in: {os.path.join(src_dir, BAD_DIR_NAME)}\n[Info] Nothing to organise')
        exit()


def get_comment_from_submission_txt(file_path):
    no_comment_text = f'Comments:\nThere are no student comments for this assignment.'
    no_comment_text_regex = no_comment_text
    no_comment_regex_compile = re.compile(no_comment_text_regex)

    with open(file_path) as f:
        file_contents = f.read()
        if not no_comment_regex_compile.findall(file_contents):
            regular_expression = f'Comments:\n.*'
            regex_compile = re.compile(regular_expression)
            match = regex_compile.findall(file_contents)
            match = str(match).replace('\\n', '').replace('[','').replace(']','').replace('"','')
            match = str(match).split('Comments:')[-1]
            return match


def get_gradebook_stats(src_dir):
    all_files = [ os.path.join(src_dir, f) for f in os.listdir(src_dir) if BAD_DIR_NAME not in f ]
    dirs = [ f for f in all_files if os.path.isdir(f) and BAD_DIR_NAME not in f ]
    normal_files = [ f for f in all_files if os.path.isfile(f) ]
    
    tracked_file_extensions = [ '.zip', '.rar', '.7z', '.txt' ]  # add extension in list to track stats for more
    files_counter = {}
    files_counter['all'], files_counter['dirs'], files_counter['normal'] = len(all_files), len(dirs), len(normal_files)

    tracked_files_counter = 0
    for ext in tracked_file_extensions:
        files_counter[ext] = len([ f for f in normal_files if f.lower().endswith(ext) ])
        tracked_files_counter += files_counter[ext]
    
    files_counter['tracked'] = tracked_files_counter
    files_counter['untracked'] = files_counter['normal'] - tracked_files_counter

    dirs_msg = f'. Also found {len(dirs)} dir(s), wasn\'t expecting any!' if len(dirs) else ''
    tracked_files_list = [ f'{files_counter[ext]} {ext}' for ext in tracked_file_extensions ] 
    tracked_msg = f"{', '.join(str(f) for f in tracked_files_list)}"
    msg = f'\n[Stats] Gradebook contains {files_counter["all"]} file(s){dirs_msg}\n[Stats] Tracking {len(tracked_file_extensions)} file extension(s), files found: {tracked_msg}\n[Stats] Files with untracked extension: {files_counter["untracked"]}'
    print(msg)
    return files_counter


def organise_file_per_student(src_dir, dest_dir, file_name, student_no):
    student_dir = os.path.join(dest_dir, student_no)
    os.makedirs(student_dir, exist_ok=True)  # create student directory if it doesn't exist
    file_path = os.path.join(src_dir, file_name)
    if os.path.isfile(file_path):
        file_path_lowercase = file_path.lower()
        if file_path_lowercase.endswith('.zip') or file_path_lowercase.endswith('.rar') or file_path_lowercase.endswith('.7z'):
            extract_file_to_dir(file_path, student_dir)  # extract the file to student directory
            if os.path.exists(file_path):  # check if compressed file exists (or it was BAD and moved), and remove if exists
                os.remove(file_path)  # delete compressed file after successful extraction
        else:
            if file_path_lowercase.endswith('.txt'):
                comment = get_comment_from_submission_txt(file_path)  # get student comment (if any) from submission txt file
                if comment:
                    comments_filename = f'{dest_dir}_comments.txt'
                    with open(comments_filename, 'a') as f:
                        f.write(f'\nStudent number: {student_no} - File: {file_path}\nComment: {comment}\n')
            else:
                file_name = file_name.split('_attempt_')[1].split('_', 1)[1]  # rename any remaining files before moving - remove the BB generated info added to the original file name
            new_file_path = os.path.join(student_dir, os.path.basename(file_name))
            shutil.move(file_path, new_file_path)  # move the file to student directory


def organise_gradebook(src_dir, dest_dir):
    """1) extracts .zip, .rar, .7z files, organises contents into directories per student number, and deletes compressed files after successful extraction
    2) organises all other files in gradebook into directories per student number
    3) checks if there are any comments in submission text files and extracts them into a file
    """
    validate_gradebook_dir_name(src_dir)  # check if dir exists, and has files in it - exits if not
    os.makedirs(dest_dir, exist_ok=True)  # create the destination directory if it doesn't exist
    files_counter = get_gradebook_stats(src_dir)  # print stats about the files in gradebook and get files_counter dict to use later
    students_numbers = []  # list to add and count unique student numbers from all files in gradebook 
    print('\nStart organising...\n')
    for file_name in os.listdir(src_dir):  # iterate through all files in the directory
        if BAD_DIR_NAME not in file_name:  # ignore dir BAD_DIR_NAME (created after first run if corrupt compressed files found)
            student_no = file_name.split('_attempt_')[0].split('_')[-1]  # get student number from file name !! pattern might need adjusting if file name format from blackboard changes !!
            students_numbers.append(student_no)
            organise_file_per_student(src_dir, dest_dir, file_name, student_no)
    
    abs_path = os.getcwd()  # absolute path of main script
    print(f'[Info] Submissions organised into directory: {os.path.join(abs_path, dest_dir)}')
    print(f'[Info] Unique student numbers in gradebook files: {len(set(students_numbers))}')
    if files_counter['.txt'] == 0:
        print(f'[Info] No submission text files found, file with comments not created')
    else:
        print(f'[Info] Comments in file: {dest_dir}_comments.txt')
    
    print(f'[Note] Compressed files (.zip, .rar, .7z) are automatically deleted from the gradebook directory after successful extraction')

    
def check_submissions_dir_for_compressed(submissions_dir):
    """checks if any submitted compressed files contain more compressed files inside (they are not recursively extracted)
    \nprints any compressed files location that need to be extracted manually
    """
    compressed_files = []
    abs_path = os.getcwd()
    for the_path, dirc, files in os.walk(submissions_dir):
        for fname in files:
            if fname.lower().endswith('.zip') or fname.lower().endswith('.rar') or fname.lower().endswith('.7z'):
                f = os.path.join(abs_path, the_path, fname)
                compressed_files.append(f)
    
    if compressed_files:
        compressed_files_str = '\n'.join(compressed_files)
        print(f'\n[Warning] One or more compressed files from the gradebook contain compressed file(s) inside ({len(compressed_files)} found in total)')
        print('\nSee below the organised per student compressed files, and extract them manually:\n')
        print(compressed_files_str)
