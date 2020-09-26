import requests
import pickle
from bs4 import BeautifulSoup
import ezlog
import zipfile
import os


log = ezlog.MyLogger(
    'driver', file=r'C:\Users\HASSANIN\Desktop\PythonProj\Local\dirver update\driver.log', form='time: [function]: msg')
FILEURL = 'https://chromedriver.storage.googleapis.com/'
FILENAME = 'chromedriver_win32.zip'


def cur_version():
    with open(r'C:\Users\HASSANIN\Desktop\PythonProj\Local\dirver update\version', 'rb') as file:
        return pickle.load(file)


def update_version(new):
    with open(r'C:\Users\HASSANIN\Desktop\PythonProj\Local\dirver update\version', 'wb') as file:
        pickle.dump(new, file)


def check_new():
    url = 'https://chromedriver.chromium.org/'
    html = requests.get(url)
    html.raise_for_status()
    html = html.text
    soup = BeautifulSoup(html, 'html.parser')
    lates = soup.select_one(
        '#sites-canvas-main-content > table > tbody > tr > td > div > div:nth-child(5) > ul > li:nth-child(2) > a')
    version = lates.text.split(' ')[1]
    log.debug('checked latest version of driver')
    return version


def download_new():
    version = check_new()
    old = cur_version()
    new = float(version[:4])
    if new > old:
        log.debug('there is a new version of driver')
        log.info(f'old version: {old} >>> new version: {new}')
        log.debug("getting file data")
        data = requests.get(FILEURL + version + '/' + FILENAME)
        data.raise_for_status()
        with open(FILENAME, 'wb') as file:
            log.debug('downloading zip file')
            file.write(data.content)
            log.debug('zip file ready')
        extract_zip()
        return new

    else:
        log.debug('no new version')
        return old


def extract_zip():
    log.debug('extracting driver from zip')
    with zipfile.ZipFile(FILENAME, 'r') as zip_file:
        zip_file.extract('chromedriver.exe')
    log.warning('removing old driver from documents directory')
    os.remove(r'C:\Users\HASSANIN\Documents\chromedriver_win32\chromedriver.exe')
    log.debug('moving new driver')
    os.rename(r'C:\Users\HASSANIN\Desktop\PythonProj\Local\dirver update\chromedriver.exe',
              r'C:\Users\HASSANIN\Documents\chromedriver_win32\chromedriver.exe')
    log.debug('moved driver to documents folder')


if __name__ == "__main__":
    log.info('Running Update')
    ver = download_new()
    update_version(ver)
    log.info('End of Update\n')
