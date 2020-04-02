from bs4 import BeautifulSoup
import re
import requests

num = 107733


def is_Chinese(word):
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False


def getHTMLText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""


def GetCode(html):
    soup = BeautifulSoup(html, "html.parser")
    td = soup.find_all(
        "td", attrs={"class": "blob-code blob-code-inner js-file-line"})
    global num
    filename = "data/" + str(num) + ".txt"
    print("get" + filename)
    instring = ""

    for eachtd in td:
        try:
            string = eachtd.text.strip()
            if len(string) > 0 and string[0] != "/" and string[0] != "*" and not is_Chinese(string):
                instring = instring + string.split("//")[0] + "\n"

        except:
            continue

    if (re.match("package", instring) or re.match("import", instring)):
        with open(filename, "w", encoding="utf-8") as file_object:
            file_object.write(instring)
        num = num + 1


def IncodeSkim(source_url, first_url):
    for i in range(1, 10):
        print("skim", i)
        try:
            now_url = source_url + str(i)
            code_menu = getHTMLText(now_url)
            soup_codemenu = BeautifulSoup(code_menu, "html.parser")
            #div = soup_codemenu.find_all("div", attrs={"class": "f4 text-normal"})
            div_codelist = soup_codemenu.find_all(
                "div", attrs={"class": "code-list"})
            if div_codelist[0].div == None:
                break
            else:
                div = soup_codemenu.find_all("div", attrs={"class": "f4 text-normal"})
                for eachdiv in div:
                    try:
                        url = first_url + str(eachdiv.a["href"])
                        html = ""
                        while html == "":
                            html = getHTMLText(url)
                            if html == "":
                                print("html none!")
                        GetCode(html)
                    except:
                        continue
        except:
            continue


def main():
    first_url = "https://github.com"
    start_url_part1 = "https://github.com/search?l=Java&o=desc&p="
    start_url_part2 = "&q=Java&s=stars&type=Repositories"
    for i in range(100):
        print(str(i)+"\n")
        s = 1
        start_url = start_url_part1 + str(i) + start_url_part2
        start_menu = ""
        while start_menu == "":
            start_menu = getHTMLText(start_url)
            if start_menu == "":
                print("startmenu none!")
        soup_startmenu = BeautifulSoup(start_menu, "html.parser")
        a = soup_startmenu.find_all("a", {"class": "v-align-middle"})
        for eacha in a:
            print(s)
            # if s >= 6:
            source_url = first_url + eacha["href"] + "/search?l=java&p="
            IncodeSkim(source_url, first_url)
            s = s + 1

        print("\n")


main()
