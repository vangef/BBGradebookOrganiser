# **Inspect by hash** :mag:

Blackboard Gradebook Organiser - Inspect gradebook & submissions by hash

## **Description**

With **Inspect by hash** you can inspect the submissions for identical files (by generating and comparing SHA256 hashes) and detect if any files have been submitted by multiple students. The tool has two variations:

[*Inspect gradebook*](usage.md#inspect-gradebook): Before organising a gradebook - for identical files in the files submitted to *Blackboard*

[*Inspect submissions*](usage.md#inspect-submissions): After organising a gradebook - for identical files in the files extracted from any submitted compressed files

## **Features**

- Generates SHA256 hashes for each submitted file, and outputs the list to a CSV file

    - Can exclude files from hashing, if provided with a CSV file listing the file names (only applicable for *Inspect submissions*)

- Compares the generated hashes and finds any duplicates - ignores duplicates if they are by the same student/submission

- Finds all files with the same hash and outputs the list to a CSV file with the following information:

    - *Inspect gradebook*: `Student ID`, `file name`, `SHA256 hash`

    - *Inspect submissions*: `Student ID`, `file path`, `file name`, `SHA256 hash`

- File names and paths listed in the generated CSV files have hyperlinks to the actual files for a quick inspection of the file contents (or running the files, if executable)

*Note:* Further analysis needs to be done manually by inspecting and filtering the generated output, depending on the submission and its files.
