# **Requirements & Settings**

## **Install requirements**

Before running the script for the first time, install the required python packages:

Option 1 - Install `py7z`, `rarfile`

```console
python -m pip install py7zr rarfile
```

Option 2 - Install all packages, including `pandas` which is used in [Inspect by hash](../inspect/about.md), using the requirements file

```console
python -m pip install -r requirements.txt
```

**Note**: If running on Linux/Mac, you also need to have `unrar` installed in order to be able to extract `.rar` files (applies for both options 1 and 2)

- `sudo apt install unrar` for Linux

- `brew install rar` for Mac

## (Optional) **Edit settings**

You can change the default settings by editing *utils/settings.py*. The main setting you might want to edit is `IGNORE_DIRS` - the list of names for directories, or files, to ignore when extracting from compressed files.

Ignored directories by default:

- `__MACOSX` (macOS system generated files)

- `.git` (git repo files)

- `node_modules` (npm)

- `vendor` (composer / laravel)
