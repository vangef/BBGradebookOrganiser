import os


BB_GRADEBOOKS_DIR = 'BB_gradebooks'  # directory with extracted gradebooks downloaded from Blackboard
BB_SUBMISSIONS_DIR = 'BB_submissions'  # directory with organised gradebook submissions
BAD_DIR_NAME = '__BAD__'  # for organise_gradebook.py - directory with corrupt/invalid compressed files
CSV_DIR = os.path.join(os.getcwd(), 'csv-inspect')  # for inspect_gradebook.py and inspect_submissions.py - output dir for generated CSV files
IGNORE_DIRS = [ '__MACOSX', '.git', 'node_modules', 'vendor' ]  # list of dir names to ignore from extracting
