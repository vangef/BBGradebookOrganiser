# BBGradebookOrganiser

Blackboard Gradebook Organiser

## Description

**Blackboard Gradebook Organiser** is a tool for organising a downloaded gradebook with assignment submissions from [Blackboard Learn](https://en.wikipedia.org/wiki/Blackboard_Learn).
The submission files are organised per student, by extracting the student number from the submission file names and creating a directory per student. Any compressed files (.zip, .rar, .7z) are extracted into the student's directory, with any remaining files submitted individually also moved into the student's directory. Student comments from submissions are also extracted into a single text file for convenient access and review.  
Additionally, after organising submissions, you can inspect all submitted files to detect duplicated files from different submissions/students by generating and comparing SHA256 hashes. See section [Inspect submissions](#inspect-submissions-mag) for details.

### Features

- Extracts, and organises per student, the content of submitted compressed files with extensions: .zip, .rar, .7z
  - Detects invalid/corrupt files
  - Doesn't extract macOS system generated files (ignores directory *__MACOSX* inside the compressed file)
- Deletes each compressed file after successful extraction into student directory
- Organises per student any remaining individually submitted files
- Checks and extracts any comments from the student submission generated text files
- Checks if any compressed files (from the contents of the submitted compressed files) have been extracted and organised per student
  - The path of any extracted and organised compressed files will be displayed on the terminal - they need to be extracted manually
- [Inspect submissions](#inspect-submissions-mag) by SHA256 hash :new:

## Instructions

### Download gradebook

- Go to the course page on Blackboard
- Go to *Grade Centre -> Full Grade Centre*
- Find assignment and click on the arrow for more options, and select *Assignment File Download*
- Select all (click *Show All* at the bottom first, to display all users) and click submit to generate the gradebook zip file
- Wait for the generated download link to appear, and click to download

### Extract gradebook

- Extract the downloaded gradebook in a new directory inside *BB_gradebooks*

### Run script

- Before running the script for the first time, install the required packages 
  - `python -m pip install -r requirements.txt`
  - If running on Linux/Mac, you also need to have *unrar* installed in order to be able to extract .rar files
    - `sudo apt install unrar` for Linux
    - `brew install rar` for Mac
- Provide the name of the directory (from section *Extract gradebook* above) as an argument when running the script
  - `python organise_gradebook.py GRADEBOOK_DIR_NAME`
- While running, the script displays on the terminal information and stats about the gradebook submissions and files

### Post-run

- All submission files can be found - organised in directories per student number - in directory *BB_submissions* under the sub-directory named after the gradebook name provided when running the script
  - e.g. `python organise_gradebook.py GRADEBOOK_DIR_NAME` creates the directory *GRADEBOOK_DIR_NAME* inside *BB_submissions*
- Each student directory contains the student's extracted and individually submitted files, and the text file generated by Blackboard with the submission (which also contains any comments left by the student)
- All comments found in the gradebook are extracted in a text file in *BB_submissions*, with the gradebook name as prefix
  - e.g. *AssignmentX_comments.txt* will be created for gradebook *AssignmentX*
- Compressed files are deleted after successfully extracting and organising the contents
  - any invalid/corrupt compressed files are moved into folder *\_\_BAD\_\_* inside the gradebook directory

## Inspect submissions :mag:

### Information

- Generates SHA256 hashes for each submitted file, and outputs list to CSV file
  - Can exclude files from hashing, if provided with a CSV file listing the file names 
- Compares the generated hashes and finds any duplicate hashes - ignores duplicates if they are by the same student/submission
- Finds all files with a duplicated hash and outputs them to CSV file with the following information: Student ID, file path, file name (without path), SHA256 hash
  - Further inspection and filtering needs to be done manually, depending on the submission files

### Usage

- For this feature you also need to install the pandas package
  - `python -m pip install pandas`
- Usage: `python inspect_submissions.py GRADEBOOK_DIR_NAME`
  - Note: run **after** organising a gradebook with `organise_gradebook.py`
- In order to exclude files from hashing, create a CSV file in directory *csv* to provide the file names to be excluded
  - e.g. for AssignmentX: create *AssignmentX_excluded.csv*, with a column named "exclude_filename" and list the file names
  - Note: the directory *csv* is automatically created when you run `inspect_submissions.py` - you need to create it manually if you want to exclude files before the first run 
- Generated CSV files can be found in directory *csv*, with *GRADEBOOK_DIR_NAME* as file name prefix
  - e.g. inspecting submissions for *AssignmentX* will create 2 csv files:
    - AssignmentX_file_hashes_[datetime].csv
    - AssignmentX_suspicious_[datetime].csv

## Notes

The Blackboard generated name for submission files must follow the pattern:
> ANYTHING_STUDENTNUMBER_attempt_DATETIME_FILENAME
