import csv
import urllib.request as myrequest
import urllib.parse as myparser
import urllib, urllib3
import http.cookiejar
from bs4 import BeautifulSoup
import shutil
import sys
def write_data(file, data, mode="a"):
    """
    this function is used to write data to csv file
    :rtype: object
    :param file: filename to append data
    :param data: array
    :param mode: append mode is default
    :return: no
    """
    # for i in range(0, len(data)):
    #     if data[i] is not None and len(data[i].strip()) == 0:
    #         data[i] = "\\N" #set NULL value
    with open(file, mode) as csvfile:
        writer = csv.writer(csvfile, delimiter=',', lineterminator='\n', quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow(data)


def fetch_data(url):
    user_agent = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'
    content_type = 'Content-Type: text/html; charset=utf-8'
    headers = {'User-Agent': user_agent, 'Content-Type': content_type}
    values = {}
    data = myparser.urlencode(values)
    data = data.encode('ascii')
    try:
        cj = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        req = myrequest.Request(url, data, headers)
        with opener.open(req, timeout=4) as response:
            data = response.read().decode('utf8', "ignore")
        return data
    except:
        return None


def readcsv(file):
    data = []
    reader = csv.reader(open(file, newline=''), delimiter=',')
    for r in reader:
        data.append(r)
    return data


def html_parser(data):
    soup = BeautifulSoup(data, 'html.parser')
    return soup


def download_file(url, directory):

    try:
        filename = url.split("/")[-1]
        fullfilename = directory + filename
        print(fullfilename)
        no_timeout = urllib3.Timeout(connect=None, read=None)
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
        content_type = 'Content-Type:application/pdf'
        headers = {'User-Agent': user_agent, 'Content-Type': content_type}

        http = urllib3.PoolManager(timeout=no_timeout)

        r = http.request("GET", url, preload_content=False, headers=headers)

        with open(fullfilename, 'wb') as out_file:
            shutil.copyfileobj(r, out_file)
        r.release_conn()
    except:
        write_data("errors.log", ["Cannot download file", url])
        write_data("errors.log", ["Unexpected error:", sys.exc_info()[0]])