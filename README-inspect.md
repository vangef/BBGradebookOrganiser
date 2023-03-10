# **Inspect by hash** :mag:

Blackboard Gradebook Organiser - Inspect gradebook & submissions by hash

## **Description**

With **Inspect by hash** you can inspect the submissions for identical files (by generating and comparing SHA256 hashes) and detect if any files have been submitted by multiple students. The tool has two variations:

[*Inspect gradebook*](#inspect-gradebook): Before organising a gradebook - for identical files in the files submitted to *Blackboard*

[*Inspect submissions*](#inspect-submissions): After organising a gradebook - for identical files in the files extracted from any submitted compressed files

## **Features**

- Generates SHA256 hashes for each submitted file, and outputs the list to a CSV file.

  - Can exclude files from hashing, if provided with a CSV file listing the file names (only applicable for *Inspect submissions*)

- Compares the generated hashes and finds any duplicate hashes - ignores duplicates if they are by the same student/submission.

- Finds all files with the same hash and outputs the list to a CSV file with the following information:

  - *Inspect gradebook*: `Student ID`, `file name`, `SHA256 hash`

  - *Inspect submissions*: `Student ID`, `file path`, `file name`, `SHA256 hash`

Further analysis needs to be done manually by inspecting and filtering the generated output, depending on the submission and its files.

## **Instructions**

Before running the *inspect* scripts for the first time, you also need to install the *pandas* package:

```python
python -m pip install pandas
```

### **Inspect gradebook**

To inspect a *gradeboook* run **`inspect_gradebook.py`** and provide the name of the gradebook directory as an argument.

- e.g. for the gradebook `AssignmentX` (in [*BB_gradebooks*](BB_gradebooks)/`AssignmentX`) run:

```python
python inspect_gradebook.py AssignmentX
```

**Note:** run ***before*** organising a gradebook with *organise_gradebook.py*

Generated CSV files can be found in directory `csv-inspect`, with the inspected gradebook's name as file name prefix - e.g. inspecting gradebook `AssignmentX` will create 2 CSV files:

- `AssignmentX_gradebook_file_hashes_[datetime].csv` - all files and their hashes
  
- `AssignmentX_gradebook_duplicate_[datetime].csv` - files with duplicate hashes

### **Inspect submissions**

To inspect *submissions* run **`inspect_submissions.py`** and provide the name of the directory with the *organised* gradebook submissions as an argument.

- e.g. for the organised gradebook `AssignmentX` (in [*BB_submissions*](BB_submissions)/`AssignmentX`) run:

```python
python inspect_submissions.py AssignmentX
```

**Note:** run ***after*** organising a gradebook with *organise_gradebook.py*

Generated CSV files can be found in directory `csv-inspect`, with the inspected submission's name as file name prefix - e.g. inspecting submissions for `AssignmentX` will create 2 CSV files:

- `AssignmentX_submissions_file_hashes_[datetime].csv` - all files and their hashes
  
- `AssignmentX_submissions_duplicate_[datetime].csv` - files with duplicate hashes

*(Optional)* In order to exclude submission files from hashing, create a CSV file in directory `csv-inspect` to provide the file names to be excluded - e.g. for `AssignmentX` create:

- `AssignmentX_excluded.csv` with a column named `exclude_filename` and list the file names

**Note:** the directory *csv-inspect* is automatically created when you run *inspect_gradebook.py* or *inspect_submissions.py* - if you want to exclude files before the first run, you need to create it manually.
