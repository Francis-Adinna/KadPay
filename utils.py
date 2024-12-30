# utils.py
import requests
import random
import string
import names
from colorama import Fore, Style, Back
from datetime import datetime
import time

def get_log_prefix(account_num=None, total=None):
    timestamp = datetime.now().strftime('%H:%M:%S')
    if account_num is not None and total is not None:
        return f"{Fore.WHITE}[{Fore.CYAN}{timestamp}{Fore.WHITE}] [{Fore.GREEN}Account {account_num}/{total}{Fore.WHITE}]"
    return f"{Fore.WHITE}[{Fore.CYAN}{timestamp}{Fore.WHITE}]"

def print_step(account_num, total, message, color=Fore.CYAN):
    status_icons = {
        Fore.GREEN: "✓",   # Success
        Fore.RED: "✗",     # Error
        Fore.YELLOW: "⚠",  # Warning
        Fore.CYAN: "→",    # Info
        Fore.MAGENTA: "★"  # Special
    }
    icon = status_icons.get(color, "→")
    print(f"{get_log_prefix(account_num, total)} {color}{icon} {message}{Style.RESET_ALL}")

def print_separator(account_num=None, total=None):
    print(f"{get_log_prefix(account_num, total)} {Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")

def get_random_domain(proxy_dict):
    domains = [
        "aderfg.my.id",
        "glowingsyabrianty.biz",
        "pelor.eu.org",
        "daftarharga.biz.id",
        "nqav95zj0p.kro.kr",
        "cundamonet.my.id",
        "mailbox.in.net",
        "webmail.asia"
    ]
    return random.choice(domains)

def generate_username():
    """Generate a random username using real-looking names."""
    styles = [
        lambda: f"{names.get_first_name().lower()}.{names.get_last_name().lower()}{random.randint(100, 999)}",
        lambda: f"{names.get_first_name().lower()}{random.randint(10, 99)}",
        lambda: f"{names.get_last_name().lower()}{names.get_first_name().lower()}{random.randint(1, 99)}",
        lambda: f"{names.get_first_name().lower()[:1]}{names.get_last_name().lower()}{random.randint(100, 999)}"
    ]
    return random.choice(styles)()

def generate_password(length=12):
    """Generate a strong password that meets common requirements."""
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    symbols = "@#$%^&*!"
    
    # Ensure at least one of each character type
    password = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits),
        random.choice(symbols)
    ]
    
    # Fill the rest randomly
    remaining_length = length - len(password)
    all_chars = lowercase + uppercase + digits + symbols
    password.extend(random.choice(all_chars) for _ in range(remaining_length))
    
    # Shuffle the password
    random.shuffle(password)
    return ''.join(password)

def generate_email(proxy_dict=None):
    """Generate a random email address."""
    domain = get_random_domain(proxy_dict)
    if not domain:
        return None
    username = generate_username()
    return f"{username}@{domain}"

def save_account(email, password, account_num, total):
    """Save account credentials to file with error handling."""
    try:
        with open('accounts.txt', 'a') as f:
            f.write(f"{email}|{password}\n")
        print_step(account_num, total, f"Account credentials saved ➜ accounts.txt", Fore.GREEN)
    except Exception as e:
        print_step(account_num, total, f"Failed to save account: {str(e)}", Fore.RED)

def print_progress(current, total):
    """Display a colorful progress bar."""
    percentage = (current / total) * 100
    bar_length = 30
    filled_length = int(bar_length * current / total)
    bar = ('█' * filled_length) + ('░' * (bar_length - filled_length))
    
    print(f"\r{Fore.CYAN}Progress: {Fore.WHITE}[{Fore.GREEN}{bar}{Fore.WHITE}] {Fore.YELLOW}{percentage:.1f}%{Style.RESET_ALL}", end='')
    if current == total:
        print()  # New line when complete

def print_stats(success_count, total_count, start_time):
    """Display statistics about the automation run."""
    elapsed_time = time.time() - start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    
    print(f"\n{Fore.CYAN}═══════════════ Session Statistics ═══════════════{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Total Attempts: {Fore.CYAN}{total_count}")
    print(f"{Fore.WHITE}Successful: {Fore.GREEN}{success_count}")
    print(f"{Fore.WHITE}Failed: {Fore.RED}{total_count - success_count}")
    print(f"{Fore.WHITE}Success Rate: {Fore.YELLOW}{(success_count/total_count)*100:.1f}%")
    print(f"{Fore.WHITE}Time Elapsed: {Fore.MAGENTA}{minutes}m {seconds}s")
    print(f"{Fore.CYAN}═══════════════════════════════════════════════{Style.RESET_ALL}\n")