# **Using Inspect by hash** :mag:

## **Inspect gradebook**

If you haven't already, extract the downloaded from *Blackboard* gradebook in a new directory inside *BB_gradebooks*

- e.g. for `AssignmentX` extract the gradebook in *BB_gradebooks*/`AssignmentX`

To inspect a *gradeboook* run **`inspect_gradebook.py`** and provide the name of the gradebook directory as an argument, e.g. for the gradebook `AssignmentX` run:

```console
python inspect_gradebook.py AssignmentX
```

**Note:** run ***before*** organising a gradebook with *organise_gradebook.py* (or extract, again, the downloaded gradebook, if you want to inspect it after organising its submissions)

Generated CSV files can be found in directory `csv-inspect`, with the inspected gradebook's name as file name prefix - e.g. inspecting gradebook `AssignmentX` will create 2 CSV files:

- `AssignmentX_gradebook_file_hashes_[datetime].csv` - all files and their hashes
  
- `AssignmentX_gradebook_duplicate_[datetime].csv` - files with duplicate hashes

## **Inspect submissions**

To inspect *submissions* run **`inspect_submissions.py`** and provide the name of the directory with the *organised* gradebook submissions as an argument.

- e.g. for the organised gradebook `AssignmentX` (in *BB_submissions*/`AssignmentX`) run:

```console
python inspect_submissions.py AssignmentX
```

**Note:** run ***after*** organising a gradebook with *organise_gradebook.py*

Generated CSV files can be found in directory `csv-inspect`, with the inspected submission's name as file name prefix - e.g. inspecting submissions for `AssignmentX` will create 2 CSV files:

- `AssignmentX_submissions_file_hashes_[datetime].csv` - all files and their hashes
  
- `AssignmentX_submissions_duplicate_[datetime].csv` - files with duplicate hashes

*(Optional)* In order to exclude submission files from hashing, create a CSV file in directory `csv-inspect` to provide the file names to be excluded - e.g. for `AssignmentX` create:

- `AssignmentX_excluded.csv` with a column named `exclude_filename` and list the file names

**Note:** the directory *csv-inspect* is automatically created when you run *inspect_gradebook.py* or *inspect_submissions.py* - if you want to exclude files before the first run, you need to create it manually.
