import zipfile
import os
import math
import glob, os
import shutil



from hiking.utils import parser_helper, url_helper, file_io_helper


def zip_files(files, zip_file_path, delete_source=False):

    with zipfile.ZipFile(zip_file_path, 'w') as myzip:
        for name in files:
            myzip.write(name, os.path.basename(name), zipfile.ZIP_DEFLATED)
        # for file in files:
        #     myzip.write(file)
        #   
        #     
        
    for file in files:
        print(file)
        shutil.rmtree(file, ignore_errors=True)

if __name__ == "__main__":
    directory = os.path.expanduser('~/Downloads')

    files = []
    for file in os.listdir(directory):
        if file.endswith(".mp3"):
            files.append(os.path.abspath(os.path.join(
            directory, file)))

    batch_size = 500

    total_nums = int(math.ceil(len(files) * 1.0 / batch_size))

    for i in range(total_nums):
        start = i * batch_size
        end = (i + 1) * batch_size
        end = len(files) if len(files) < end else end

        file_to_zipped = files[start:end]

        zip_file_path = os.path.abspath(os.path.join(directory, "ec_file_{}.zip".format(i)))

        if os.path.exists(zip_file_path):
            shutil.rmtree(zip_file_path, ignore_errors=True)

        zip_files(file_to_zipped, zip_file_path)

        
    

    