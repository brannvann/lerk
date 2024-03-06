import os
import subprocess
from pathlib import Path
from pdf2image import convert_from_path

def process_folder(dirpath:str)->bool:
    print(f'process {dirpath}')
    dirs = [d for d in os.listdir(dirpath) if ( os.path.isdir(os.path.join(dirpath, d)) and (not '.pages' in d)  )]
    for d in dirs:
        process_folder(os.path.join(dirpath, d))
    pass
    files = [f for f in os.listdir(dirpath) if os.path.isfile(os.path.join(dirpath, f))]
    for f in files:
        process_file(dirpath, f)
    return True

def process_file(dirpath, filename)->bool:
    print(f'process {filename} in {dirpath}')
    issue_dir_name = filename.replace('.pdf', '.pages')
    issue_dir_path = os.path.join(dirpath, issue_dir_name)
    if not os.path.exists(issue_dir_path):
        os.makedirs(issue_dir_path)
    if not os.path.exists(issue_dir_path):
        print(f'cannot create directory {issue_dir_path}')
        return False
    if not os.listdir(issue_dir_path):
        images = convert_from_path(os.path.join(dirpath, filename))
        for indx, image in enumerate(images):
            image_name = f"{filename.replace('.pdf', '')}_page_{indx:02}.jpg"
            image_path = os.path.join(issue_dir_path, image_name)
            image.save(image_path, 'JPEG')
        pass
    pass  
    ocr_dir(issue_dir_path)
    return True

def ocr_dir(dirpath, mask='.jpg', lang='rus'):
    print(f'ocr {dirpath}')
    files = [f for f in os.listdir(dirpath) if ( os.path.isfile(os.path.join(dirpath, f)) and (mask in f) )]
    for f in files:
        file_path = os.path.join(dirpath, f)
        text_path = os.path.join(dirpath, f.replace(mask, ''))
        cmd_line = f"tesseract '{file_path}' '{text_path}' -l {lang}"
        print(f'run {cmd_line}')
        proc = subprocess.Popen(["tesseract", file_path, text_path, '-l', 'rus'])
        proc.communicate()
        proc.wait(timeout=60)
    pass

def main( dirpath:str = None ):
    print(f'start in {dirpath}')
    if os.path.isdir(dirpath):
        process_folder(dirpath)
    else:
        print(f'{dirpath} is not a directory')
    pass
    return

if __name__ == '__main__':
    curdir = Path(__file__).parent.absolute()
    dirpath = os.path.join(curdir.parent, 'test_data')
    main(dirpath)