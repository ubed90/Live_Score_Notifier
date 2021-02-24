import requests
from bs4 import BeautifulSoup
from win10toast import ToastNotifier
from pynput import keyboard
import time , os


def clear():
    os.system('cls')

class CricketScores:
    def __init__(self):
        self.url = 'https://www.cricbuzz.com'
        request = requests.get(self.url)
        data = request.content
        self.soup = BeautifulSoup(data , 'html.parser')

    def get_ongoing_matches(self):
        self.matches_urls = []
        self.get_matches = self.soup.find_all('li' , {'class' : "cb-col cb-col-25 cb-mtch-blk cb-vid-sml-card-api videos-carousal-item cb-carousal-item-large cb-view-all-ga"})
        header = self.soup.find('h4' , class_ = 'cb-mdl-hdr').text
        clear()
        print(f'------------------{header.upper()}--------------------\n')
        for index , match in enumerate(self.get_matches):
            print(str(index)+". "+match.find('a')['title'])
            self.matches_urls.append(self.url + match.find('a')['href'])
        print(' ')
        self.choice = int(input("ENTER THE NUMBER CORRESPONDING TO THE MATCH TO GET LIVE UPDATES (0 - {}) :: ".format(len(self.matches_urls))))
        if self.choice in range(0 , len(self.matches_urls)):
            return self.choice , self.matches_urls
        else:
            print('INVALID CHOICE !')
            self.get_ongoing_matches()

    def display_live_updates(self , choice , matches_urls):
        global break_program
        url = matches_urls[choice]
        request = requests.get(url)
        data = request.content
        soup = BeautifulSoup(data , 'lxml')
        data = soup.find('div' , class_ = 'cb-col cb-col-67 cb-scrs-wrp')
        status = soup.find('div' , class_ = 'cb-col cb-col-100 cb-min-stts cb-text-complete') or \
            soup.find('div' , class_ = 'cb-text-inprogress') or soup.find('div' , class_ = 'cb-text-stumps') or soup.find('div' , class_ = 'cb-text-lunch') or \
            soup.find('div' , class_ = 'cb-text-tea') or soup.find('div' , class_ = 'cb-text-inningsbreak') or soup.find('div' , class_ = 'cb-text-dinner')
        if status != None:
            for i in status.attrs.values():
                if 'cb-text-inprogress' in i:
                    return self.get_matches[choice].find('a')['title'] , data.text.strip() , status.text.strip()
                else:
                    clear()
                    print("\n"+data.text.strip())
                    print(status.text+"\n")
                    return None , None , None
        else:
            return self.get_matches[choice].find('a')['title'] , None , None




if __name__ == '__main__':
    clear()
    break_program = False
    score = CricketScores()
    choice , matches_urls =  score.get_ongoing_matches()
    title , scores , status = score.display_live_updates(choice , matches_urls)
    if title == None and scores == None and status == None:
        pass   
    elif scores == None and status == None:
        clear()
        print("MATCH HASN'T STARTED YET !!")
    else:
        def on_press(key):
            global break_program
            if key == keyboard.Key.end:
                print ('-------Program is Closing!!!------')
                break_program = True
                return False


        with keyboard.Listener(on_press=on_press) as listener:
            clear()
            print('PRESS END KEY TO CLOSE THE PROGRAM...')
            while break_program == False:
                title , scores , status = score.display_live_updates(choice , matches_urls)
                if title != None and scores != None:
                    notify = ToastNotifier()
                    notify.show_toast(title , scores+'\n'+status , duration = 5 , icon_path = 'Ball.ico')
                time.sleep(10)
            listener.join()



