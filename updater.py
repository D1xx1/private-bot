#updater.py

import requests
import zipfile
import os
import shutil

main_dir = os.getcwd()

class Downloader():
    def download_file(url):
        local_filename = url.split('/')[-1]
        with requests.get(url, stream=True, allow_redirects=True) as request:
            request.raise_for_status()
            with open(local_filename, 'wb') as file:
                for chunk in request.iter_content(chunk_size=8192):
                    file.write(chunk)
        return local_filename

    def download():
        filename = Downloader.download_file('https://github.com/D1xx1/private-bot/archive/refs/heads/main.zip')
        print(filename)
        zip = zipfile.ZipFile(filename)
        zip_extract = [text_file.filename for text_file in zip.infolist()]
        with zipfile.ZipFile(filename, 'r') as zip_file:
            zip_file.extractall(os.getcwd())
        try:
            os.chdir(zip_extract[0])
            print(os.getcwd())
            file = os.listdir()
            for i in range(0, len(file)):
                shutil.move(file[i], main_dir)
            os.chdir(main_dir)
            shutil.rmtree(zip_extract[0])
        except Exception as error:
            print(error)
            Start.start()

class Start:
    def start():
        while True:
            try:
                id = (input('Введите 1, чтобы скачать актуальную версию программы: '))
                if int(id) == 1:
                    Downloader.download()
                    break
                elif int(id) == 0:
                    break
                else:
                    print('Ошибка ввода...\n')
            except ValueError as error:
                print('Ошибка ввода...')
                pass



if __name__ == '__main__':
    Start.start()
