from bs4 import BeautifulSoup
import requests
import os, sys
from urllib.request import urlretrieve
import zipfile, glob, time
import pyglet
import tkinter as tk
from tkinter import scrolledtext

font_link = 'https://www.wfonts.com/download/data/2016/05/19/serpent/Serpent-Regular.ttf'

monty_links = [
    'http://www.montypython.net/scripts/architec.php',
    'http://www.montypython.net/scripts/petshop.php',
    'http://www.montypython.net/scripts/funniest.php',
    'http://www.montypython.net/scripts/silywalk.php'
]

def connect(link):
    html = requests.get(link).text
    bsoj = BeautifulSoup(html, 'lxml')
    return bsoj

def unzip_font(in_dir, out_dir):
    with zipfile.ZipFile(in_dir, 'r') as zip_ref:
        zip_ref.extractall(out_dir)

def checked():
    epath = os.path.join(os.getcwd(), 'font')
    if os.path.exists(epath) or os.path.exists('serpent_path.txt'):
        return True
    return False

def get_ttfpath():
    fp = 'serpent_path.txt'
    if os.path.exists(fp):
        path = ''
        with open(fp) as file:
            path = file.read().strip()
        return path
    else:
        raise Exception('serpent_path.txt not found')

def download_font():
    if not checked():
        fpath = os.path.join(os.getcwd(), 'font')
        if not os.path.exists(fpath):
            os.mkdir(fpath)
        spath = os.path.join(fpath, 'Serpent-Regular.ttf')
        urlretrieve(font_link, spath)
        print('font downloaded:', spath)
        # epath = os.path.join(fpath, 'serpent')
        # unzip_font(spath, epath)
        # print('font extracted:', epath)
        epath = fpath
        open('serpent_path.txt', 'w').write(epath)
        return epath
    else:
        return get_ttfpath()

def find_ttffile(path):
    files = glob.glob(os.path.join(path, "*.ttf"))
    return files[0]

def clean_content(content):
    content = content.strip()
    red = "Continue to the next sketch"
    red2 = 'Get the ENTIRE sketch in .wav format'
    content = content.split(red)[0]
    content = content.strip()
    content = content.split(red2)[0]
    content = content.strip()
    return content

def crawl_monty(index):
    link = monty_links[index-1]
    bsoj = connect(link)
    div_cont = bsoj.find('div', {'id': 'content'})
    # print(div_cont.text)
    content = clean_content(str(div_cont.text))
    # print(content)
    return content

def display_text(text, font_path, custom_text='', color='black', font_size=12):
    def on_destroy():
        win.destroy()
    ...

    def on_destroy2(event):
        win.destroy()
    ...
    pyglet.font.add_file(font_path)
    font_name = 'Serpent'
    win = tk.Tk() 
    win.state('zoomed')
    win.resizable(True, True)

    win.title("Monty Python")  
    tk.Label(win, text=custom_text).grid(column=1,row=1)  
 
    scrolW=100  
    scrolH=50  

    scr=scrolledtext.ScrolledText(win, width=scrolW, height=scrolH, wrap=tk.WORD, font=(font_name, 12),)
    scr.grid(column=0, columnspan=3)
    scr.insert(tk.END, text)
    fmt = '\n'*20
    scr.insert(tk.END, fmt)
    scr['state'] = tk.DISABLED
    win.protocol('WM_DELETE_WINDOW', on_destroy)
    win.bind('<Escape>', on_destroy2)
    win.mainloop()


def run(index):
    epath = download_font()
    content = crawl_monty(index)
    ttf_file_path = find_ttffile(epath)
    display_text(content, ttf_file_path)

def menu():
    s = "What sketch do you want to convert?\n"
    s += "1. Architect Sketch\n"
    s += "2. Dead Parrot Sketch\n"
    s += "3. Funniest Joke Sketch\n"
    s += "4. Ministry of Silly Walks Sketch\n"
    s += "Enter a choice [1-4]: "
    return s


def main():
    s = menu()
    choice = int(input(s))
    print("Check for the running tkinter window. Close after reading, if you want to do it again.")
    run(choice)
    resp = input("Do you want to do another (y/n): ")
    while resp == 'y':
        choice = int(input(s))
        run(choice)
        resp = input("Do you want to do another (y/n): ")

main()
