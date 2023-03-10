# **BBGradebookOrganiser**

Blackboard Gradebook Organiser

## **Description**

**Blackboard Gradebook Organiser** is a tool for organising a downloaded gradebook with assignment submissions from [Blackboard Learn &#x29c9;](https://en.wikipedia.org/wiki/Blackboard_Learn).  
The submission files are organised per student, by extracting the student number from the submission file names and creating a directory per student. Compressed files are extracted into the student's directory, and any remaining individually submitted files are also moved into the student's directory. Student comments from the submissions are also extracted into a single text file for convenient access and review.  
Optionally, you can inspect the submissions for identical files (by generating and comparing SHA256 hashes) and detect if any files have been submitted by multiple students. See [Inspect by hash](README-inspect.md) for more information.

## **Features**

- Extracts, and organises per student, the content of submitted compressed files with extensions: `.zip`, `.rar`, `.7z`

  - Detects invalid/corrupt files

  - Doesn't extract macOS system generated files (ignores directory *__MACOSX* inside the compressed file)

- Deletes each compressed file after successful extraction into student directory

- Organises per student any remaining individually submitted files

- Checks and extracts any comments from the student submission generated text files

- Checks if any compressed files (from the contents of the submitted compressed files) have been extracted and organised per student

  - The path of any extracted and organised compressed files will be displayed on the terminal - they need to be extracted manually

- [Inspect by hash](README-inspect.md) generates and compares SHA256 hashes of all the submitted files, and detects files that are identical and have been submitted by multiple students. Two ways to inspect:

  - Inspect gradebook: Before organising a gradebook - for identical files in the files submitted to *Blackboard*

  - Inspect submissions: After organising a gradebook - for identical files in the files extracted from any submitted *compressed* files

## **Instructions**

### **Download gradebook**

1. Go to the course page on Blackboard

2. Go to *Grade Centre -> Full Grade Centre*

3. Find the assignment and click on the arrow for more options, and select *Assignment File Download*

4. Select all (click *Show All* at the bottom first, to display all users) and click submit to generate the gradebook zip file

5. Wait for the generated download link to appear, and click to download

### **Extract gradebook**

Extract the downloaded gradebook in a new directory inside [*BB_gradebooks*](BB_gradebooks).

- e.g. for `AssignmentX` extract the gradebook in [*BB_gradebooks*](BB_gradebooks)/`AssignmentX`

### **Organise gradebook**

Before running the script for the first time, install the required packages (*py7z*, *rarfile*):

```python
python -m pip install py7zr rarfile
```

Note: If running on Linux/Mac, you also need to have `unrar` installed in order to be able to extract *.rar* files.

- `sudo apt install unrar` for Linux

- `brew install rar` for Mac

&nbsp;  
To organise the gradebook run **`organise_gradebook.py`** and provide the name of the directory with the *extracted* gradebook (from section *Extract gradebook* above) as an argument.

- e.g. for gradebook `AssignmentX` (in [*BB_gradebooks*](BB_gradebooks)/`AssignmentX`) run:

```python
python organise_gradebook.py AssignmentX
```

While running, the script displays on the terminal information and stats about the gradebook submissions and files.

### **Post-run**

- All submission files can be found - organised in directories per student number - in directory [*BB_submissions*](BB_submissions), under the sub-directory named after the gradebook name provided when running the script

  - e.g. `organise_gradebook.py AssignmentX` creates the directory `AssignmentX` inside [*BB_submissions*](BB_submissions)

- Each student directory contains:

  - the extracted files from the submitted `.zip`, `.rar`, `.7z`
  
  - the individually submitted files
  
  - the text file generated by Blackboard for the submission (which also contains any comments left by the student)

- All comments found in the gradebook are extracted in a text file in [*BB_submissions*](BB_submissions), with the gradebook name as prefix

  - e.g. `AssignmentX_comments.txt` will be created for gradebook `AssignmentX`

- Compressed files are deleted after successfully extracting and organising the contents

  - Any invalid/corrupt compressed files are moved into folder `__BAD__` inside the gradebook directory

## **Inspect by hash** :mag:

See [***Inspect by hash***](README-inspect.md) for more information & details.

## **General notes**

The Blackboard generated name for submission files must follow the pattern:
> ANYTHING_STUDENTNUMBER_attempt_DATETIME_FILENAME
