import os, shutil
import wget
from NHentai import NHentai
from PIL import Image

# Mozilla/5.0 (X11; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0
# https://i.nhentai.net/galleries/732189/1.jpg

def __get_sacred_number():
    sacred_num = input("Enter the number: ")
    print("--------------------------------------------------------")
    confirm = input("You entered: " + sacred_num + ". Is this correct? (Y/N): ")
    print("--------------------------------------------------------")
    if(confirm == "Y" or confirm == "y" or confirm == "yes" or confirm == "Yes"):
        return sacred_num
    else:
       sacred_num =  __get_sacred_number()
       return sacred_num

def __get_conversion_answer():
    convBool = input("Would you like to convert from JPG to PNG for easier use with certain other software? (Y/N): ")
    print("--------------------------------------------------------")
    if(convBool == "Y" or convBool == "y" or convBool == "yes" or convBool == "Yes"):
        return True
    elif(convBool == "N" or convBool == "n" or convBool == "no" or convBool == "No"):
        return False
    else:
        print("Unable to understand input. Type (Y/y/yes/Yes or N/n/no/No).")
        print("--------------------------------------------------------")
        redo = __get_conversion_answer()
        return redo

def __get_links(sacred_num):
    nhentai = NHentai()
    doujin = nhentai._get_doujin(id=f'{sacred_num}')
    if(doujin == None):
        raise Exception("This sacred number doesn't exist! Sorry!")
    else:
        try:
            links = doujin.images
            return links
        except AttributeError as e:
            print("An unknown error occured, check your numbers! Stacktrace: ")
            print(e)
            print("The program will now exit.")
            exit()

def __create_dir(sacred_num):
    path = os.getcwd()
    try:
        os.mkdir(path + "/out_files")
    except FileExistsError:
        path = path
    path = (path + "/out_files/" + str(sacred_num))
    try:
        os.mkdir(path)
    except FileExistsError:
        shutil.rmtree(path)
        os.mkdir(path)
    return path

def __download_hentai(sacred_num):
    links = __get_links(sacred_num)
    path = __create_dir(sacred_num)
    
    for url in links:
        wget.download(url, path)

def __convert(sacred_num):
    nhentai = NHentai()
    doujin = nhentai._get_doujin(id=f'{sacred_num}')
    try:
            length = doujin.total_pages
    except AttributeError as e:
            print("An unknown error occured, check your numbers! Stacktrace: ")
            print(e)
            print("The program will now exit.")
            exit()
    i = 1
    path = os.getcwd()
    while(i <= length):
        path = (path + "/out_files/" + str(sacred_num) + f"/{i}")
        try:
            img = Image.open((path + ".jpg"))
            img.convert('RGB').save((path + ".png"))
            os.remove((path + ".jpg"))
        except FileNotFoundError as e:
            path = path
        path = os.getcwd()
        i = i + 1

def main():
    LINK_BASE = "https://i.nhentai.net/galleries/"
    print("--------------------------------------------------------")
    print("Hello. Welcome to my shitty nHentai downloader script.")
    print("--------------------------------------------------------")
    sacred_num = __get_sacred_number()
    print("We will now (attempt) to download your hentai!")
    print("--------------------------------------------------------")
    links = __get_links(sacred_num)
    __download_hentai(sacred_num)
    print()
    print("--------------------------------------------------------")
    print("Your hentai downloaded SUCCessfully!")
    print("--------------------------------------------------------")
    convBool = __get_conversion_answer()
    if(convBool):
        __convert(sacred_num)
    print("Your hentai converted SUCCessfully!")

if __name__ == '__main__':
    main()