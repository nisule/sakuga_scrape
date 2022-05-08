import requests
from bs4 import BeautifulSoup
import re
import time

all_urls = []
errors = []


def scrape_webpage(url):
    # return source, tags, video URL
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    # find tag
    try:
        tags = soup.find("meta", {"property": "og:title"})
        tags = tags['content']
        str1 = tags.split('|')
        tag = str1[0].strip()
        tag = re.sub(r'[<>:/\|?*"]+', "", tag)  # get rid of windows disallowed characters in file names
        #print(tag)
    except Exception as e:
        errors.append(e)
        errors.append(f'error in scraping webpage tag: {e}\nurl: {url}')

    # find source
    try:
        source = soup.find("div", {"id": "stats"}).find('ul')
        source_changed = False
        potential_sources = source.text.split('\n')
        #print(potential_sources)
        for a_source in potential_sources:  # this logic is dumb
            if 'Source:' in a_source:
                source = a_source
                source_changed = True
                if '#' in source:
                    source_split = source.split('#')
                    source = source_split[1]
                    source_changed = True
                break  # found the source, break out

        if 'Source' in source:
            source = source.replace("Source", "", 1)

        if source_changed == False:
            source = ""

        source = re.sub(r'[<>:/\|?*"]+', "", source)  # get rid of windows disallowed characters in file names
        #print(source)
    except Exception as e:
        errors.append(e)
        errors.append(f'error in scraping webpage source: {e}\nurl: {url}')

    # find video url
    try:
        video_url = soup.find("a", {"class": "original-file-unchanged"})['href']
        #print(video_url)
    except Exception as e:
        errors.append(e)
        errors.append(f'error in scraping webpage video url: {e}\nurl: {url}')

    # get file extension
    try:
        file_ext = video_url.split(".")[-1]
        #print(file_ext)
    except Exception as e:
        errors.append(e)
        errors.append(f'error in getting file extension: {e}\nfile_ext: {file_ext}')

    # all values we want to return in a dict
    return_dict = {'tag': tag, 'source': source, 'video_url': video_url, 'file_ext': file_ext}
    return return_dict


def get_urls_from_file(file_path):
    file = open(file_path, 'r')
    while True:
        line = file.readline()
        if not line:
            break
        all_urls.append(line.strip())
    file.close()


def download_file(url, file_name):
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(file_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                # if chunk:
                f.write(chunk)
    return file_name


def main():
    # CHANGE THIS PART TO BE YOUR PATH
    print("getting URLs from file")
    get_urls_from_file(r"C:\Users\nicks\PycharmProjects\anime_shit\urls.txt")  # creates list of all urls
    all_info = []  # list of dicts eg [{'tag': tag, 'source': source, 'video_url': video_url, 'file_ext': file_ext}]

    print("starting scraping the urls for all the info we want")
    for url in all_urls:
        try:
            values = scrape_webpage(url)  # scrape source, tags, video URL, and file extension
            all_info.append(values)
        except Exception as e:
            errors.append(e)
            errors.append(f'error in scraping webpages: {e}\nurl: {url}')
        time.sleep(1)

    print("done scraping, starting downloads")

    for a_dict in all_info:
        try:
            # create file name
            file_name = f"{a_dict['source']} {a_dict['tag']}.{a_dict['file_ext']}"
            #print(f'file_name: {file_name}')
            #print(f'a_dict: {a_dict}')
            # download the video file
            download_file(a_dict['video_url'], file_name)
        except Exception as e:
            errors.append(f'error in making file name or downloading: {e}\na_dict: {a_dict}')
        time.sleep(1)

    print("done downloading")
    print("ERRORS:")
    print(errors)


if __name__ == "__main__":
    main()

