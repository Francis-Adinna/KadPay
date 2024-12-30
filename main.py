# main.py
import time
import random
import sys
from colorama import init, Fore, Style
from utils import *
from banner import print_banner, print_footer
import requests
import json

def send_otp(email, password, proxy_dict, account_num, total):
    """Handle registration process with Firebase authentication."""
    url = "https://identitytoolkit.googleapis.com/v1/accounts:signUp"
    params = {
        'key': "AIzaSyDmqZpkteihdMSDV5-VkNjgGBeLbFjGRCg"
    }
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Origin': 'https://www.kardpay.app',
        'Referer': 'https://www.kardpay.app/'
    }

    try:
        response = requests.post(url, params=params, json=payload,
                               headers=headers, proxies=proxy_dict, timeout=60)
        result = response.json()

        if response.status_code == 200:
            print_step(account_num, total, "Registration successful!", Fore.GREEN)
            return result
        else:
            error_message = result.get('error', {}).get('message', 'Unknown error')
            print_step(account_num, total, f"Registration failed: {error_message}", Fore.RED)
            return None
    except requests.RequestException as e:
        print_step(account_num, total, f"Network error during registration: {str(e)}", Fore.RED)
        return None

def login(id_token, proxy_dict, account_num, total):
    """Handle login process with KardPay API."""
    url = "https://api.kardpay.app/waitinglist/users/user/login"
    headers = {
        'Authorization': f"Bearer {id_token}",
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Origin': 'https://www.kardpay.app',
        'Referer': 'https://www.kardpay.app/'
    }

    try:
        response = requests.post(url, headers=headers, proxies=proxy_dict, timeout=60)
        response.raise_for_status()
        print_step(account_num, total, "Login successful!", Fore.GREEN)
        return response.json()
    except requests.exceptions.RequestException as e:
        print_step(account_num, total, f"Login error: {str(e)}", Fore.RED)
        return None

def set_reff(referral_code, token, proxy_dict, account_num, total):
    """Apply referral code to the account."""
    url = "https://api.kardpay.app/waitinglist/users/user/sponsor"
    payload = {"referralCode": referral_code}
    headers = {
        'Authorization': f"Bearer {token}",
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Origin': 'https://www.kardpay.app',
        'Referer': 'https://www.kardpay.app/'
    }

    try:
        response = requests.post(url, headers=headers, json=payload, proxies=proxy_dict, timeout=60)
        if response.status_code == 200:
            print_step(account_num, total, "Referral code applied successfully!", Fore.GREEN)
            return True
        else:
            print_step(account_num, total, f"Failed to apply referral code: {response.text}", Fore.RED)
            return False
    except requests.exceptions.RequestException as e:
        print_step(account_num, total, f"Error applying referral code: {str(e)}", Fore.RED)
        return False

def process_single_registration(proxies, referral_code, account_num, total_referrals):
    """Process a single account registration with retries."""
    max_retries = 3
    for retry in range(max_retries):
        if retry > 0:
            print_step(account_num, total_referrals, f"Retry attempt {retry}/{max_retries-1}", Fore.YELLOW)
            time.sleep(random.uniform(2, 5))

        proxy_dict = None
        if proxies:
            proxy = random.choice(proxies)
            proxy_dict = {"http": proxy, "https": proxy}
            print_step(account_num, total_referrals, f"Using proxy: {proxy}", Fore.CYAN)
        
        email = generate_email(proxy_dict)
        if not email:
            print_step(account_num, total_referrals, "Failed to generate email", Fore.RED)
            continue

        password = generate_password()
        print_step(account_num, total_referrals, f"Generated credentials:", Fore.CYAN)
        print_step(account_num, total_referrals, f"Email: {email}", Fore.WHITE)
        print_step(account_num, total_referrals, f"Password: {password}", Fore.WHITE)

        otp_result = send_otp(email, password, proxy_dict, account_num, total_referrals)
        if not otp_result:
            continue

        id_token = otp_result.get("idToken")
        if not id_token:
            print_step(account_num, total_referrals, "No ID token received", Fore.RED)
            continue

        login_result = login(id_token, proxy_dict, account_num, total_referrals)
        if not login_result:
            continue

        if referral_code.strip():
            if not set_reff(referral_code, id_token, proxy_dict, account_num, total_referrals):
                continue

        save_account(email, password, account_num, total_referrals)
        return True
    
    return False

def load_proxies():
    """Load proxies from file."""
    try:
        with open('proxies.txt', 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return None

def main():
    """Main function to run the automation."""
    init(autoreset=True)
    print_banner()
    
    print(f"{Fore.RED}DISCLAIMER: Use this script at your own risk!{Style.RESET_ALL}\n")
    
    # Get referral code
    referral_code = ""
    while not referral_code.strip():
        referral_code = input(f"{Fore.MAGENTA}Enter referral code: {Style.RESET_ALL}")
        if not referral_code.strip():
            print(f"{Fore.RED}Referral code is required!{Style.RESET_ALL}")
    
    # Get number of referrals
    total_referrals = 0
    while total_referrals <= 0:
        try:
            total_referrals = int(input(f"{Fore.MAGENTA}Enter number of referrals to generate: {Style.RESET_ALL}"))
            if total_referrals <= 0:
                print(f"{Fore.RED}Please enter a positive number!{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Please enter a valid number!{Style.RESET_ALL}")
    
    # Load proxies
    proxies = load_proxies()
    if proxies:
        print(f"{Fore.GREEN}Loaded {len(proxies)} proxies{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}No proxies loaded - running without proxies{Style.RESET_ALL}")
    
    print("\n")
    start_time = time.time()
    success_count = 0
    current_account = 1
    
    try:
        while current_account <= total_referrals:
            print_separator(current_account, total_referrals)
            print_step(current_account, total_referrals, "Starting new registration", Fore.MAGENTA)
            
            if process_single_registration(proxies, referral_code, current_account, total_referrals):
                success_count += 1
                current_account += 1
                print_progress(success_count, total_referrals)
            
            time.sleep(random.uniform(2, 5))
        
        print_stats(success_count, total_referrals, start_time)
        print_footer()
        
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Program terminated by user{Style.RESET_ALL}")
        print_stats(success_count, total_referrals, start_time)
        print_footer()
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}Unexpected error: {str(e)}{Style.RESET_ALL}")
        print_stats(success_count, total_referrals, start_time)
        print_footer()
        sys.exit(1)

if __name__ == "__main__":
    main()