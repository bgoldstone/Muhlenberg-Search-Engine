import os
import re
from queue import LifoQueue
from typing import List, Union

import requests

# contants
# regex for link and anchor tags. group 0 is href.
LINK = re.compile(
    r'<a[^>]*href=["\']([A-Za-z\d/_#-;=@]*)["\']')
ROOT_URL = re.compile(r'https?://w*\.?[\w]+\.[.\w]+\/?')
TEXT = re.compile(r'>([\w \-&\']+)<\/')
TITLE = re.compile(r'<title>([^<]+)<\/title>')


def add_forward_slash(url: str) -> str:
    """
        add_forward_slash Adds a forward slash to url if not already present.

        Args:
            url (str): URL to check

        Returns:
            str: url with forward slash
        """
    return url if url[-1] == '/' else f'{url}/'


def scrape_data(first_url: str, num_of_urls: int, path: str) -> None:
    """
    scrape_data Scrapes the first 500 urls.

    Args:
        first_url (str): The url to start the web scrape from
        num_of_urls (int): Number of urls to scrape.
        path (str): file path to dump web scrape contents.
    """
    # keeps track of visited urls.
    visited = set()
    not_visitable = set()
    # stack for DFS of urls.
    stack = []
    # first url to start the web scrape from.
    first_url = add_forward_slash(first_url)
    # gets domain and top level domain of url. Ex. 'example.com'
    domain = re.findall(r'https?:\/\/w*\.?([\w]+\.[.\w]+)\/?', first_url)[0]
    # For Subdomains
    # URL_TO_MATCH = re.compile(
    #     r'^https?:\/\/[a-zA-Z0-9]*\.?w*\.?{}\/'.format(domain))
    # For Domain
    URL_TO_MATCH = re.compile(
        r'^[htps:/]*w*\.?{}\/'.format(domain))
    # gets full root url Ex. 'http://www.example.com/'
    root_url = f'{re.findall(ROOT_URL, first_url)[0]}'
    root_url = add_forward_slash(root_url)
    print(root_url)
    # puts first url in stack to start.
    # gets robots.txt file
    robots = get_robots_txt(root_url)
    # time.sleep(2)
    stack.append(first_url)
    # scrape until 500 urls are scraped and more links to parse...
    while(len(visited) < num_of_urls and len(stack) != 0):
        stack_url = stack.pop()
        # prevent duplicate http/https links
        if stack_url.startswith("http://"):
            stack_url = re.sub(r'^http://', 'https://', stack_url)
        # gets the url scraping.
        current_root_url = re.findall(
            r'^https:\/\/w?w?w?\.?[a-zA-Z0-9.]+\/', stack_url)[0]
        # if url has one of these extensions, skip it.
        if len(re.findall(r'\.jpg$|\.jpeg$|\.tif$|\.png$|\.pdf$', stack_url.lower())) > 0:
            print(
                f'404 Not Found or Not Visitable! Stack: {len(stack)} URL: {stack_url}')
            not_visitable.add(stack_url)
            continue
        current_url = get_url(stack_url, current_root_url[:-1])
        HTML_PATH = os.path.join(path, 'HTML')
        if not os.path.exists(HTML_PATH):
            os.makedirs(HTML_PATH)
        # checks if urls was successfully visited.
        if not current_url:
            print(
                f'404 Not Found or Not Visitable! Stack: {len(stack)} URL: {stack_url}')
            not_visitable.add(stack_url)
            continue
        if current_url[0] in visited:
            print(
                f'URL Already Visited! Stack: {len(stack)} URL: {stack_url}')
            continue
        # writes url and text to file
        print(
            f'Visited: {len(visited)} {current_url[0]} Stack: {len(stack)}')
        if not os.path.exists(path):
            os.makedirs(path)
        os.chdir(path)
        with open(f'URL_{len(visited)}.txt', 'w', errors='ignore') as f:
            # url, number of relative links, number of anchor links, html contents, list of links.
            f.write(f'{current_url[0]}\n')
            # one token per space
            f.write(re.sub(r'[\s]{2,}', ' ', current_url[2]))
            f.write(f'\n{current_url[4]}')
        os.chdir(HTML_PATH)
        # writes html to file
        with open(f'HTML_{len(visited)}.txt', 'w', errors='ignore') as h:
            h.write(current_url[3])
        visited.add(stack_url)
        # for all of the absolute links, add them to the stack.
        for url in current_url[1]:
            # makes sure urls is not visited, the url is part of current domain, url is a absolute url, and is not disallowable by robots.txt.
            if re.findall(URL_TO_MATCH, url) and url not in not_visitable and url not in visited and url not in stack:
                # if robots is found, check against that.
                if robots:
                    if len(re.findall(robots, url)) == 0:
                        stack.append(url)
                else:
                    stack.append(url)
    os.chdir(path)
    with open(f'not_visitable.txt', 'w', errors='ignore') as n:
        n.write('\n'.join(not_visitable))


def get_url(base_url: str, root_url: str) -> Union[List, bool]:
    """
    get_url Scrapes teh url and returns a list of its findings.

    Args:
        base_url (str): URL to check.
        root_url (str): Root url of the domain.

    Returns:
        Union[List, bool]: URL findings in the format of [url, # relative links(<link>), # anchor links(<a>), html contents, [**absolute links]]. Returns False if url not successfully reachable.
    """
    # if url fails to resolve, return False.
    try:
        # added headers because some websites require them.
        url = requests.get(base_url, headers={"User-Agent": "*"})
    except requests.exceptions.ConnectionError:
        print('site is not reachable', base_url)
        return False
    # only take html pages
    if 'text/html' not in url.headers.get('content-type', 'text/html') or url.status_code != 200:
        return False
    # base url, links, text
    return_val = [base_url, [], '']
    # if url is successfully retrieved, get matches from regular expressions.
    for match in LINK.findall(url.text):
        # if relative link.
        current_match = match[:match.find(
            '#')] if '#' in match else match
        if current_match.startswith('/'):
            return_val[1].append(f'{root_url}{current_match}')
        # if absolute link.
        elif current_match.startswith('http'):
            # add to list of links if not relative link, or blank, else return root_url + (blank or relative url)
            return_val[1].append(current_match)

    # gets all text from webpage.
    return_val[2] = ' '.join(re.findall(TEXT, url.text))
    return_val.append(url.text)

    # gets URL Title
    try:
        return_val.append(re.findall(TITLE, url.text)[0])
    except IndexError:
        return_val.append('No Title')
    # returns return_val if successful request.
    return return_val


def get_robots_txt(domain: re.Pattern) -> Union[re.Pattern, None]:
    """
    get_robots_txt gets robots.txt from the domain.

    Args:
        domain (str): domain of website.

    Returns:
       Union[re.Pattern, None]: regex for disallowed links. None if user_agent does not exist.
    """
    # keeps list of not visitable links.
    not_visitable = []
    # finds user agent.
    find_by = 'user-agent: *'
    # request robots.txt
    request = requests.get(f'{domain}robots.txt')
    # all lines split by new line or carriage return.
    lines = [line.lower() for line in re.split(r'\n|\r', request.text)]
    # if no user agent is found, return None.
    try:
        index = lines.index(find_by)
    except ValueError:
        return None
    blank_lines = 0
    # for each line starting at 'User-Agent: *'
    for line in lines[index:]:
        if line == '':
            blank_lines += 1
            if blank_lines >= 2:
                # parsees into one string to compile in regex
                return_val = '|'.join(not_visitable)
                return re.compile(return_val) if return_val else None

        else:
            blank_lines = 0
        # if not allowed to visit page, append to not_visitable list.
        if line.startswith('disallow'):
            not_visitable.append(line[line.index(':')+2:])
