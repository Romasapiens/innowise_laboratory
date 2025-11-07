from colorama import init, Fore, Back, Style

init()

print(f"{Fore.RED}{Back.YELLOW}Hello World! {Style.RESET_ALL}")
print(f"{Fore.GREEN}Hello World in Green! {Style.RESET_ALL}")
print(f"{Fore.BLUE}{Style.BRIGHT}Hello World in BrightBlue! {Style.RESET_ALL}")
print(f"{Fore.MAGENTA}{Back.CYAN}Hello World with Magenta text and Cyanbackground! {Style.RESET_ALL}")