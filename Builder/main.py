import re
import time
import requests
from urllib.parse import urlparse
import os
from colorama import Fore, init

init(convert=True)


def GetURLs(url: str):
    urls = []
    r = requests.get(url=url)
    data = re.findall("(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-&?=%.]+", r.text)
    for d in data:
        s = str(d).removeprefix('http://')
        s2 = str(d).removeprefix('https://')
        if s != d or s2 != d:
            if d != url:
                if d not in urls:
                    urls.append(d)
    return (urls)


def ScanURL(url, max_deep):
    urls = []

    def rur(urlp, deep, first):
        if first is True:
            deep = deep + 2
            first = False
        urlsp = []
        skip = False
        if deep <= max_deep:
            try:
                urlsp = GetURLs(url=urlp)
            except requests.exceptions.ConnectionError:
                print(f'{Fore.RED + "[-]"} {Fore.BLUE + urlp} {Fore.WHITE + "is Offline"}')
                skip = True
            for urld in urlsp:
                if skip is True:
                    skip = False
                    continue
                if urld in urls:
                    continue
                if deep > max_deep:
                    continue
                urls.append({"url": urld, "from": urlp, "deep": deep})
                print(f'{Fore.GREEN + "[+]"} {Fore.WHITE + "Scanning"} {Fore.BLUE + urld} {Fore.MAGENTA + f"[{deep}]"}')
                rur(urld, deep + 1, False)

    rur(urlp=url, deep=0, first=True)
    return (urls)


def Reverse(lst):
    new_lst = lst[::-1]
    return new_lst


def URLFrom(url):
    for urlu in fullurls:
        if urlu['url'] == url:
            urlf = urlu['from']
            break
    return (urlf)

def start():
    os.system('cls')
    global fullurls
    global main
    global md
    main = input(Fore.WHITE + "URL: ")
    md = int(input("Max_Deep: "))
    fullurls = ScanURL(url=main, max_deep=md)
    print("DONE, PRESS ENTER...")
    input()
    os.system('cls')

start()

while True:
    command = input(Fore.CYAN + "[View]: Lists all URLs, Optional Query | [Tree]: 1 paramater, gives a tree on how the url was found | [ReDo] Restarts the file\n>>> ")
    commands = command.split()
    print(command)
    if command == '':
        os.system('cls')
        continue
    if len(commands) > 1:
        if commands[0].lower() == "tree":
            tree = []
            urln = commands[1]
            while True:
                froms = URLFrom(urln)
                if froms != main:
                    tree.append(urlparse(froms).netloc)
                    urln = froms
                else:
                    break
            if len(tree) > 2:
                print(f"{' >>> '.join(Reverse(tree))} >>> {commands[1]}")
            else:
                print(f"{main} >>> {commands[1]}")
            input()

    if commands[0] == "view":
        if len(commands) == 1:
            for url in fullurls:
                deep = url['deep']
                print(f"{Fore.GREEN + '[+]'} {Fore.BLUE + url['url']} {Fore.MAGENTA + f'[{deep}]'}")
            input()
        else:
            for url in fullurls:
                deep = url['deep']
                if commands[1] in url['url']:
                    print(f"{Fore.GREEN + '[+]'} {Fore.BLUE + url['url']} {Fore.MAGENTA + f'[{deep}]'}")
            input()
    os.system('cls')
    if command.lower() == "redo":
        start()
