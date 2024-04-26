# **BBGradebookOrganiser**

Blackboard Gradebook Organiser

**Documentation**: [docs.vangef.net/BBGradebookOrganiser](https://docs.vangef.net/BBGradebookOrganiser)

**Source Code**: [github.com/vangef/BBGradebookOrganiser](https://github.com/vangef/BBGradebookOrganiser)

## **Description**

**Blackboard Gradebook Organiser** is a tool for organising a downloaded gradebook with assignment submissions from [Blackboard Learn &#x29c9;](https://en.wikipedia.org/wiki/Blackboard_Learn).  
The submission files are organised per student, by extracting the student number from the submission file names and creating a directory per student. Compressed files are extracted into the student's directory, and any remaining individually submitted files are also moved into the student's directory. Student comments from the submissions are also extracted into a single text file for convenient access and review.  
Optionally, you can inspect the submissions for identical files (by generating and comparing SHA256 hashes) and detect if any files have been submitted by multiple students. See [Inspect by hash](inspect/about.md) for more information.

## **Features**

- Extracts, and organises per student, the content of submitted compressed files with extensions: `.zip`, `.rar`, `.7z`

    - Detects invalid/corrupt files

    - Skips extracting files and directories if their path contains any of the *ignored dirs*, as set in *settings.py* - ignored directories by default:

        - `__MACOSX` (macOS system generated files)

        - `.git` (git repo files)

        - `node_modules` (npm)

        - `vendor` (composer / laravel)

- Deletes each compressed file after successful extraction into student directory

- Organises per student any remaining individually submitted files

- Checks and extracts any comments from the student submission generated text files

- Checks if any compressed files (from the contents of the submitted compressed files) have been extracted and organised per student

    - The path of any extracted and organised compressed files will be displayed on the terminal - they need to be extracted manually

- [Inspect by hash](inspect/about.md) generates and compares SHA256 hashes of all the submitted files, and detects files that are identical and have been submitted by multiple students. Two ways to inspect:

    - Inspect gradebook: Before organising a gradebook - for identical files in the files submitted to *Blackboard*

    - Inspect submissions: After organising a gradebook - for identical files in the files extracted from any submitted *compressed* files

## **Instructions**

See the documentation for [Setup](instructions/setup.md) and [Usage](instructions/usage.md) instructions, and more information & details about [***Inspect by hash***](inspect/about.md).

## **General notes**

The Blackboard generated name for submission files must follow the pattern:
> ANYTHING_STUDENTNUMBER_attempt_DATETIME_FILENAME

## **Changelog**

See [***Changelog***](CHANGELOG.md) for notable changes and updates.
