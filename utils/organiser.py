import os, shutil, re
from collections import defaultdict
from utils.extractor import extract_file_to_dir
from utils.settings import BAD_DIR_NAME, MULTIPLE_DIR_NAME, BB_GRADEBOOKS_DIR, IGNORE_DIRS, TRACKED_FILE_EXT


def _parse_filename(file_path: str) -> tuple[str, str] | None:
    """Extract STUDENTNUMBER and DATETIME from the filename."""
    pattern = r'^(.*?)_(\d+)_attempt_(\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2})(?:_.*)?(?:\..+)?$'
    match = re.match(pattern, file_path)
    if match:
        return match.group(2), match.group(3)  # STUDENTNUMBER, DATETIME
    return None, None

def _filter_multiple_attempts(directory: str) -> None:
    """Keep only the latest attempt for each student and move older attempts to MULTIPLE_DIR_NAME."""
    submissions = defaultdict(list)
    
    multiple_folder = os.path.join(directory, MULTIPLE_DIR_NAME)
    os.makedirs(multiple_folder, exist_ok=True)
    
    # collect all valid files
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            student_number, timestamp = _parse_filename(filename)
            if student_number and timestamp:
                submissions[student_number].append((timestamp, filepath))
    
    # process submissions
    for student, files in submissions.items():
        files.sort(reverse=True, key=lambda x: x[0])  # sort by timestamp (most recent first)
        latest_timestamp = files[0][0]  # get the most recent timestamp
        
        # keep all files from the latest attempt, move older ones
        for timestamp, filepath in files:
            if timestamp != latest_timestamp:
                shutil.move(filepath, os.path.join(multiple_folder, os.path.basename(filepath)))

    print(f"\n[Info] Multiple submission attempts filtering completed.\nOlder submissions moved to folder: {MULTIPLE_DIR_NAME}")

def _validate_gradebook_dir_name(src_dir: str) -> None:
    if not os.path.isdir(src_dir):  # check if it exists and is a directory
        print(f'\n[ERROR] Incorrect directory: {src_dir}\n[Info] Make sure the directory exists in "{BB_GRADEBOOKS_DIR}"')
        exit()
    if not os.listdir(src_dir):  # check if there are any files in the directory
        print(f'\n[Info] No files found in this gradebook - nothing to organise')
        exit()
    if len(os.listdir(src_dir)) == 1 and BAD_DIR_NAME in os.listdir(src_dir):  # if there is 1 file/directory and it is the 'BAD' directory
        print(f'\n[Info] Gradebook has only invalid compressed files in: {os.path.join(src_dir, BAD_DIR_NAME)}\n[Info] Nothing to organise')
        exit()

def _get_comment_from_submission_txt(file_path: str) -> tuple[str, str] | None:
    no_comment_regex = f'Comments:\nThere are no student comments for this assignment.'
    no_comment_pattern = re.compile(no_comment_regex)

    with open(file_path, encoding='utf-8') as f:
        file_contents = f.read()
        if not no_comment_pattern.findall(file_contents):
            comment_regex = f'Comments:\n.*'
            name_regex = f'^Name:\s*.*'
            comment_pattern = re.compile(comment_regex)
            name_pattern = re.compile(name_regex)
            if comment_pattern.findall(file_contents):
                comment_match = comment_pattern.findall(file_contents)[0]
                comment = comment_match.split('\n')[1]
                name_match = name_pattern.findall(file_contents)[0]
                name = name_match.split('Name:')[1].split('(')[0].strip() or ''
                return comment, name
    return None, None

def _get_comment_from_submission_txt_BB_ultra(file_path: str) -> tuple[str, str] | None:
    with open(file_path, encoding='utf-8') as f:
        file_contents = f.read()
    
    match = re.search(r'Submission Field:\s*<br>(.*)', file_contents, re.DOTALL)  # find the section starting with "Submission Field: <br>"
    if not match:
        return None, None
    
    section = match.group(1)    
    section = re.sub(r'\s*<p><a href.*?</a>', '', section, flags=re.DOTALL)  # remove the part starting with "<p><a href" and ending with "</a></p>"    
    paragraphs = re.findall(r'<p>(.*?)</p>', section, re.DOTALL) or None  # extract text inside <p> tags
    
    if not paragraphs:
        return None, None
        
    cleaned_text = '\n'.join(p.replace('<br>', '\n') for p in paragraphs)  # replace <br> with new lines within paragraphs
    
    if not cleaned_text:
        return None, None
    
    name_regex = f'^Name:\s*.*'
    name_pattern = re.compile(name_regex)
    name_match = name_pattern.findall(file_contents)[0]
    name = name_match.split('Name:')[1].split('(')[0].strip() or ''

    return cleaned_text.strip(), name  # comment, name

def _get_gradebook_stats(src_dir: str) -> dict[str, int]:
    all_files = [ os.path.join(src_dir, f) for f in os.listdir(src_dir) if BAD_DIR_NAME not in f and MULTIPLE_DIR_NAME not in f ]
    dirs = [ f for f in all_files if os.path.isdir(f) and BAD_DIR_NAME not in f and MULTIPLE_DIR_NAME not in f ]
    normal_files = [ f for f in all_files if os.path.isfile(f) ]
    
    files_counter = {}
    files_counter['all'], files_counter['dirs'], files_counter['normal'] = len(all_files), len(dirs), len(normal_files)

    tracked_files_counter = 0
    for ext in TRACKED_FILE_EXT:
        files_counter[ext] = len([ f for f in normal_files if f.lower().endswith(ext) ])
        tracked_files_counter += files_counter[ext]
    
    files_counter['tracked'] = tracked_files_counter
    files_counter['untracked'] = files_counter['normal'] - tracked_files_counter

    dirs_msg = f'. Also found {len(dirs)} dir(s), wasn\'t expecting any!' if len(dirs) else ''
    tracked_files_list = [ f'{files_counter[ext]} {ext}' for ext in TRACKED_FILE_EXT ] 
    tracked_msg = f"{', '.join(str(f) for f in tracked_files_list)}"
    msg = f'\n[Stats] Gradebook contains {files_counter["all"]} file(s){dirs_msg}\n[Stats] Tracking {len(TRACKED_FILE_EXT)} file extension(s), files found: {tracked_msg}\n[Stats] Files with untracked extension: {files_counter["untracked"]}'
    print(msg, flush=True)
    return files_counter

def _organise_file_per_student(src_dir: str, dest_dir: str, file_name: str, student_no: str) -> None:
    student_dir = os.path.join(dest_dir, student_no)
    os.makedirs(student_dir, exist_ok=True)  # create student directory if it doesn't exist
    file_path = os.path.join(src_dir, file_name)
    if os.path.isfile(file_path):
        file_path_lowercase = file_path.lower()
        if file_path_lowercase.endswith('.zip') or file_path_lowercase.endswith('.rar') or file_path_lowercase.endswith('.7z'):
            exception_flag = extract_file_to_dir(file_path, student_dir)  # extract the file to student directory
            # check if compressed file exists (or it was BAD and moved), and no exception was returned from extracting - remove if both true
            if os.path.exists(file_path) and exception_flag is None:
                os.remove(file_path)  # delete compressed file after successful extraction
        else:
            if file_path_lowercase.endswith('.txt'):
                comment, name = _get_comment_from_submission_txt_BB_ultra(file_path)  # get student comment (if any), and name, from submission txt file
                if comment and name:
                    comments_filename = f'{dest_dir}_comments.txt'
                    with open(comments_filename, 'a') as f:
                        f.write(f'\nStudent number: {student_no} - Student name: {name}\nFile: {file_path}\nComment: {comment}\n')
            else:
                try:
                    file_name = file_name.split('_attempt_', 1)[1].split('_', 1)[1]  # rename any remaining files before moving - remove the BB generated info added to the original file name
                except IndexError as e:
                    print(f'Cannot process file - possible incorrect format of filename')
            new_file_path = os.path.join(student_dir, os.path.basename(file_name))
            shutil.move(file_path, new_file_path)  # move the file to student directory

def organise_gradebook(src_dir: str, dest_dir: str) -> None:
    """1) extracts .zip, .rar, .7z files, organises contents into directories per student number, and deletes compressed files after successful extraction
    2) organises all other files in gradebook into directories per student number
    3) checks if there are any comments in submission text files and extracts them into a file
    """
    _validate_gradebook_dir_name(src_dir)  # check if dir exists, and has files in it - exits if not
    os.makedirs(dest_dir, exist_ok=True)  # create the destination directory if it doesn't exist
    _filter_multiple_attempts(src_dir)
    print('\nGetting gradebook stats...', flush=True)
    files_counter = _get_gradebook_stats(src_dir)  # print stats about the files in gradebook and get files_counter dict to use later
    students_numbers: list[str] = []  # list to add and count unique student numbers from all files in gradebook 
    print('\nStart organising... (this may take a while depending on the number -and size- of submissions)\n', flush=True)

    for file_name in os.listdir(src_dir):  # iterate through all files in the directory
        if BAD_DIR_NAME not in file_name and MULTIPLE_DIR_NAME not in file_name:  # ignore dirs BAD_DIR_NAME (created after first run if corrupt compressed files found) and MULTIPLE_DIR_NAME (dir with older attempts)
            student_no = file_name.split('_attempt_', 1)[0].split('_')[-1]  # get student number from file name !! pattern might need adjusting if file name format from blackboard changes !!
            students_numbers.append(student_no)
            _organise_file_per_student(src_dir, dest_dir, file_name, student_no)
    
    ignored_str = ', '.join(IGNORE_DIRS)
    print(f'[Info] Skipped extracting files in dirs with name that includes any of the following strings: {ignored_str}\n', flush=True)
    abs_path = os.getcwd()  # absolute path of main script
    print(f'[Info] Submissions organised into directory: {os.path.join(abs_path, dest_dir)}\n', flush=True)
    print(f'[Info] Unique student numbers in gradebook files: {len(set(students_numbers))}\n', flush=True)
    if files_counter['.txt'] == 0:
        print(f'[Info] No submission text files found, file with comments not created\n', flush=True)
    else:
        print(f'[Info] Comments in file: {dest_dir}_comments.txt\n', flush=True)
    
    print(f'[Info] Compressed files (.zip, .rar, .7z) are automatically deleted from the gradebook directory after successful extraction\n', flush=True)
    
def check_submissions_dir_for_compressed(submissions_dir: str) -> None:
    """checks if any submitted compressed files contain more compressed files inside (they are not recursively extracted)
    \nprints any compressed files location that need to be extracted manually
    """
    compressed_files: list[str] = []
    abs_path = os.getcwd()
    for the_path, dirc, files in os.walk(submissions_dir):
        for fname in files:
            if fname.lower().endswith('.zip') or fname.lower().endswith('.rar') or fname.lower().endswith('.7z'):
                f = os.path.join(abs_path, the_path, fname)
                compressed_files.append(f)
    
    if compressed_files:
        compressed_files_str = '\n'.join(compressed_files)
        print(f'\n[Warning] One or more compressed files found in the extracted and organised submission files ({len(compressed_files)} found in total)')
        print('\n[Info] See below the list of compressed files, organised per student, and extract them manually if necessary:\n')
        print(compressed_files_str)
