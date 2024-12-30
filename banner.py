# banner.py
from colorama import Fore, Style, Back

def print_banner():
    colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
    banner = f"""
{Fore.CYAN}════════════════════════════════════════════════════════════════════════════════
{colors[0]}███████╗{colors[1]}██╗     {colors[2]}███████╗{colors[3]}██╗  ██╗{colors[4]}██╗  ██╗{colors[5]}         
{colors[0]}██╔════╝{colors[1]}██║     {colors[2]}██╔════╝{colors[3]}╚██╗██╔╝{colors[4]}╚██╗██╔╝{colors[5]}         
{colors[0]}█████╗  {colors[1]}██║     {colors[2]}█████╗   {colors[3]}╚███╔╝  {colors[4]}╚███╔╝ {colors[5]}         
{colors[0]}██╔══╝  {colors[1]}██║     {colors[2]}██╔══╝   {colors[3]}██╔██╗  {colors[4]}██╔██╗ {colors[5]}         
{colors[0]}██║     {colors[1]}███████╗{colors[2]}███████╗{colors[3]}██╔╝ ██╗{colors[4]}██╔╝ ██╗{colors[5]}         
{colors[0]}╚═╝     {colors[1]}╚══════╝{colors[2]}╚══════╝{colors[3]}╚═╝  ╚═╝{colors[4]}╚═╝  ╚═╝{colors[5]}         

{colors[4]}██████╗ {colors[5]}██╗ {colors[0]}██████╗{colors[1]}██╗  ██╗{colors[2]}██╗███████╗
{colors[4]}██╔══██╗{colors[5]}██║{colors[0]}██╔════╝{colors[1]}██║  ██║{colors[2]}██║██╔════╝
{colors[4]}██████╔╝{colors[5]}██║{colors[0]}██║     {colors[1]}███████║{colors[2]}██║█████╗  
{colors[4]}██╔══██╗{colors[5]}██║{colors[0]}██║     {colors[1]}██╔══██║{colors[2]}██║██╔══╝  
{colors[4]}██║  ██║{colors[5]}██║{colors[0]}╚██████╗{colors[1]}██║  ██║{colors[2]}██║███████╗
{colors[4]}╚═╝  ╚═╝{colors[5]}╚═╝{colors[0]} ╚═════╝{colors[1]}╚═╝  ╚═╝{colors[2]}╚═╝╚══════╝
{Fore.CYAN}════════════════════════════════════════════════════════════════════════════════

{Fore.WHITE}             ⚡ {Fore.YELLOW}KardPay Automation Suite v1.0.0{Fore.WHITE} ⚡             
{Fore.CYAN}────────────────────────────────────────────────────────────────────────────────{Style.RESET_ALL}
    """
    print(banner)

def print_footer():
    footer = f"""
{Fore.CYAN}════════════════════════════════════════════════════════════════════════════════
{Fore.WHITE}                     Thank you for using our service!                     
{Fore.CYAN}════════════════════════════════════════════════════════════════════════════════{Style.RESET_ALL}
    """
    print(footer)