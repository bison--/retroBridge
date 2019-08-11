import modules.BaseModule
import urllib.request
import requests
from bs4 import BeautifulSoup
# TODO: https://www.freecodecamp.org/news/how-to-scrape-websites-with-python-and-beautifulsoup-5946935d93fe/

class Browsi(modules.BaseModule.BaseModule):

    def __init__(self):
        super().__init__()
        self.page_rows = []
        self.chars_per_row = 80
        self.rows_per_page = 24
        self.page_index = 0

    def getPage(self, url):
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')

        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.decompose()  # rip it out

        # get text
        text = soup.get_text()

        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())

        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))

        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)

        return text

    def command(self, user_command):
        commands = self.getDictFromCommand(user_command)
        #print(commands)
        if 'br_help' in commands:
            self.commandCatched()
            self.writeLine('')
            self.writeLine('################')
            self.writeLine('# URL COMMANDS #')
            self.writeLine('################')
            self.writeLine('')
            self.writeLine('url=https://wiki.chaosdorf.de')

        elif 'url' in commands:
            self.commandCatched()

            self.page_rows.clear()
            full_page = self.getPage(commands['url'])

            cnt = 0
            row = ''
            for _char in full_page:
                row += _char
                cnt += 1
                if cnt >= self.chars_per_row or _char == "\n":
                    self.page_rows.append(row.strip())
                    row = ''
                    cnt = 0
            self.page_rows.append('# END OF PAGE #')
            self.getNextPage()

        elif 'urln' in commands:
            self.commandCatched()
            self.getNextPage()

        elif 'urlf' in commands:
            self.commandCatched()
            self.writeLine('# RESTARTING PAGE OUTPUT #')
            self.page_index = 0
            self.getNextPage()

    def getNextPage(self):
        last_row = ''
        for i in range(self.page_index * self.rows_per_page, self.page_index * self.rows_per_page + self.rows_per_page):
            if (i >= len(self.page_rows)):
                break
            last_row = self.page_rows[i]
            self.writeLine(self.page_rows[i])

        if last_row == '# END OF PAGE #':
            return
        #if self.page_index * self.rows_per_page + self.rows_per_page >= len(self.page_rows):
            #self.writeLine(self.page_rows[i])
            #print('END OF PAGE')
        self.page_index += 1
