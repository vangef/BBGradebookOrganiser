import os, shutil, platform
import zipfile, rarfile
from py7zr import SevenZipFile, exceptions

from utils.settings import BAD_DIR_NAME


def mark_file_as_BAD(file: str, bad_exception: Exception) -> None:
    try:
        filename = os.path.basename(file)
        bad_dir = os.path.join(os.path.dirname(file), BAD_DIR_NAME)
        os.makedirs(bad_dir, exist_ok=True)
        bad_file_path = os.path.join(bad_dir, filename)
        shutil.move(file, bad_file_path)
        print(f'[Warning] Found BAD compressed file: {filename}\nMoved to: {bad_file_path}\nError message: {bad_exception}')
    except Exception as e: 
        print(f'[Error] {e}')


def extract_zip(zip_file: str, target_dir: str) -> None | Exception:
    try:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            members = [ m for m in zip_ref.infolist() if "__MACOSX" not in m.filename ]
            zip_ref.extractall(target_dir, members=members)  # extract all files, ignoring those with the "__MACOSX" string in the name
            zip_ref.close()
    except zipfile.BadZipfile as e:
        mark_file_as_BAD(zip_file, e)
    except Exception as e:
        print(f'[ERROR] Something went wrong while extracting the contents of a submitted zip file. Check the error message, get student id and download / organise manually\nError message: {e}')
        return e


def extract_rar(rar_file: str, target_dir: str) -> None:
    try:    
        with rarfile.RarFile(rar_file, 'r') as rar_ref:
            if platform.system() == 'Windows':
                rarfile.UNRAR_TOOL = os.path.join('utils', 'UnRAR.exe')
            else:  # if Linux or Mac
                rarfile.UNRAR_TOOL = 'unrar'
            files = rar_ref.namelist()
            files = [ f for f in files if "__MACOSX" not in f ]  # filter out files with "__MACOSX" in the name
            rar_ref.extractall(target_dir, files)  # extract the remaining files
            rar_ref.close()
    except rarfile.BadRarFile as e:
        mark_file_as_BAD(rar_file, e)
    except rarfile.NotRarFile as e:
        mark_file_as_BAD(rar_file, e)
    except rarfile.RarCannotExec as e:
        print('[Error] Missing unrar tool\nfor Windows: make sure file UnRAR.exe exists in directory \'utils\'\nfor Linux/Mac: need to install unrar (check README)')
        exit()


def extract_7z(seven_zip_file: str, target_dir: str) -> None:
    try:  # extract the 7z file using py7zr
        with open(seven_zip_file, 'rb') as f:
            seven_zip = SevenZipFile(seven_zip_file, mode='r')
            if not seven_zip.getnames():
                raise exceptions.Bad7zFile
            files = seven_zip.getnames()
            files = [ f for f in files if "__MACOSX" not in f ]  # filter out files with "__MACOSX" in the name
            seven_zip.extract(target_dir, targets=files)  # extract the remaining files
            seven_zip.close()
    except exceptions.Bad7zFile as e:
        mark_file_as_BAD(seven_zip_file, e)
    except Exception as e:
        mark_file_as_BAD(seven_zip_file, e)


def extract_file_to_dir(file_path: str, student_dir: str) -> None | Exception:
    os.makedirs(student_dir, exist_ok=True)  # create the subdirectory for student

    if file_path.lower().endswith('.zip'):
        return extract_zip(file_path, student_dir)
    elif file_path.lower().endswith('.rar'):
        extract_rar(file_path, student_dir) 
    elif file_path.lower().endswith('.7z'):
        extract_7z(file_path, student_dir) 
    else:
        print(f"[Error] unknown file type: {file_path}")
