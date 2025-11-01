#!/usr/bin/env python3
"""
Website Information Scanner Tool
Developed by ChowdhuryVai
"""

import socket
import ssl
import requests
import whois
import dns.resolver
from datetime import datetime
import urllib.parse
import time
import concurrent.futures
import os
import platform
import sys

class Colors:
    PRIMARY = '\033[94m'
    SECONDARY = '\033[95m'
    SUCCESS = '\033[92m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    INFO = '\033[96m'
    TEXT = '\033[97m'
    HIGHLIGHT = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    
    banner = f"""
{Colors.PRIMARY}{Colors.BOLD}
 ██████╗██╗  ██╗ ██████╗ ██╗    ██╗██████╗ ██╗   ██╗██████╗ ██╗   ██╗██╗   ██╗
██╔════╝██║  ██║██╔═══██╗██║    ██║██╔══██╗██║   ██║██╔══██╗╚██╗ ██╔╝██║   ██║
██║     ███████║██║   ██║██║ █╗ ██║██║  ██║██║   ██║██████╔╝ ╚████╔╝ ██║   ██║
██║     ██╔══██║██║   ██║██║███╗██║██║  ██║██║   ██║██╔══██╗  ╚██╔╝  ██║   ██║
╚██████╗██║  ██║╚██████╔╝╚███╔███╔╝██████╔╝╚██████╔╝██║  ██║   ██║   ╚██████╔╝
 ╚═════╝╚═╝  ╚═╝ ╚═════╝  ╚══╝╚══╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝ 
                                                                                
{Colors.END}
{Colors.SECONDARY}╔══════════════════════════════════════════════════════════════════════════════╗
║                        WEBSITE INFORMATION SCANNER                        ║
║                    Developed by: ChowdhuryVai                            ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ Telegram: https://t.me/darkvaiadmin                                        ║
║ Channel:  https://t.me/windowspremiumkey                                   ║
║ Website:  https://crackyworld.com/                                         ║
╚══════════════════════════════════════════════════════════════════════════════╝{Colors.END}
"""
    print(banner)

def print_colored(text, color, end="\n"):
    print(f"{color}{text}{Colors.END}", end=end)

def loading_animation(message, duration=2):
    symbols = ['⣾', '⣷', '⣯', '⣟', '⡿', '⢿', '⣻', '⣽']
    start_time = time.time()
    i = 0
    
    while time.time() - start_time < duration:
        print_colored(f"\r{message} {symbols[i % len(symbols)]}", Colors.INFO, end="")
        time.sleep(0.1)
        i += 1
    
    print_colored(f"\r{message} ✓", Colors.SUCCESS)

def clean_url(url):
    url = url.strip().lower()
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return url

def get_domain(url):
    parsed = urllib.parse.urlparse(url)
    return parsed.netloc

def format_date(date_str):
    if not date_str:
        return "Not Available"
    try:
        if isinstance(date_str, str):
            date_obj = datetime.strptime(date_str, "%b %d %H:%M:%S %Y GMT")
        else:
            date_obj = date_str
        return date_obj.strftime("%d %B %Y")
    except Exception:
        return str(date_str)

def get_security_headers(headers):
    security_headers = {
        'Strict-Transport-Security': 'HSTS',
        'Content-Security-Policy': 'CSP',
        'X-Frame-Options': 'X-Frame',
        'X-Content-Type-Options': 'X-Content-Type',
        'X-XSS-Protection': 'XSS Protection',
        'Referrer-Policy': 'Referrer Policy',
        'Feature-Policy': 'Feature Policy'
    }
    return {new_name: headers.get(header, 'Not Available') 
            for header, new_name in security_headers.items()}

def check_admin_panel(url, timeout=3):
    admin_paths = ['/admin', '/administrator', '/wp-admin', '/login', 
                  '/panel', '/admin.php', '/admin/login', '/cp']
    found_paths = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        def check_path(path):
            try:
                test_url = url.rstrip('/') + path
                response = requests.get(test_url, timeout=timeout, allow_redirects=False)
                if response.status_code in [200, 301, 302, 403]:
                    return test_url
            except:
                pass
            return None
        
        futures = [executor.submit(check_path, path) for path in admin_paths]
        for future in concurrent.futures.as_completed(futures):
            if future.result():
                found_paths.append(future.result())
    
    return found_paths

def grab_banner(url, timeout=5):
    try:
        response = requests.get(url, timeout=timeout)
        server = response.headers.get('Server', 'Not Available')
        x_powered_by = response.headers.get('X-Powered-By', 'Not Available')
        return server, x_powered_by
    except Exception as e:
        return f'Error: {str(e)}', 'Not Available'

def get_server_location(url):
    try:
        response = requests.get(url)
        server_ip = socket.gethostbyname(get_domain(url))
        try:
            location = requests.get(f"https://ipinfo.io/{server_ip}/json").json()
            return location.get("city", "Not Available"), location.get("country", "Not Available")
        except:
            return "Not Available", "Not Available"
    except:
        return "Not Available", "Not Available"

def print_section_header(title):
    print_colored(f"\n╔{'═' * 60}╗", Colors.SECONDARY)
    print_colored(f"║ {title:^58} ║", Colors.SECONDARY)
    print_colored(f"╚{'═' * 60}╝", Colors.SECONDARY)

def print_info(category, details, color=Colors.TEXT):
    print_colored(f"  {category:<25}: {color}{details}{Colors.END}", Colors.INFO)

def scan_website(url):
    try:
        url = clean_url(url)
        domain = get_domain(url)
        
        print_section_header("SCANNING IN PROGRESS")
        
        # Network Information
        loading_animation("Checking IP and DNS information", 1)
        try:
            ip = socket.gethostbyname(domain)
            print_info("IP Address", ip)
            
            dns_records = dns.resolver.resolve(domain, 'A')
            dns_ips = [str(record) for record in dns_records]
            if dns_ips:
                print_info("DNS Records", ", ".join(dns_ips))
        except Exception as e:
            print_info("Network Info", f"Error: {str(e)}", Colors.ERROR)

        # SSL Information
        loading_animation("Checking SSL certificate", 1)
        try:
            context = ssl.create_default_context()
            with socket.create_connection((domain, 443), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    print_info("SSL Valid From", format_date(cert['notBefore']))
                    print_info("SSL Valid Until", format_date(cert['notAfter']))
        except Exception as e:
            print_info("SSL Status", f"Error: {str(e)}", Colors.ERROR)

        # HTTP Headers
        loading_animation("Checking HTTP headers and security", 1)
        try:
            response = requests.get(url, timeout=5)
            status_color = Colors.SUCCESS if response.status_code == 200 else Colors.WARNING
            print_info("HTTP Status", f"{response.status_code} ({response.reason})", status_color)

            security_headers = get_security_headers(response.headers)
            for header, value in security_headers.items():
                status_color = Colors.SUCCESS if value != 'Not Available' else Colors.WARNING
                print_info(header, value, status_color)
        except Exception as e:
            print_info("HTTP Status", f"Error: {str(e)}", Colors.ERROR)

        # WHOIS Information
        loading_animation("Fetching WHOIS domain information", 1)
        try:
            domain_info = whois.whois(domain)
            if domain_info.creation_date:
                creation_date = domain_info.creation_date[0] if isinstance(domain_info.creation_date, list) else domain_info.creation_date
                print_info("Domain Created", format_date(creation_date))
            if domain_info.expiration_date:
                expiration_date = domain_info.expiration_date[0] if isinstance(domain_info.expiration_date, list) else domain_info.expiration_date
                print_info("Domain Expiry", format_date(expiration_date))
        except Exception as e:
            print_info("WHOIS Info", f"Error: {str(e)}", Colors.ERROR)

        # Admin Panel Detection
        loading_animation("Scanning for admin panels", 1)
        admin_panels = check_admin_panel(url)
        if admin_panels:
            for panel in admin_panels:
                print_info("Admin Panel Found", panel, Colors.WARNING)
        else:
            print_info("Admin Panel", "Not Found", Colors.SUCCESS)

        # Server Information
        loading_animation("Gathering server information", 1)
        server, x_powered_by = grab_banner(url)
        print_info("Server", server)
        print_info("X-Powered-By", x_powered_by)

        # Server Location
        loading_animation("Detecting server location", 1)
        city, country = get_server_location(url)
        print_info("Server Location", f"{city}, {country}")

        print_section_header("SCAN COMPLETED")
        print_colored(f"\n{Colors.SUCCESS}✓ Website scan completed successfully!{Colors.END}", Colors.SUCCESS)
        
    except Exception as e:
        print_colred(f"\n{Colors.ERROR}✗ Scan Error: {str(e)}{Colors.END}", Colors.ERROR)

def main():
    print_banner()
    
    try:
        print_colored(f"\n{Colors.PRIMARY}Enter website URL (e.g., example.com): {Colors.END}", Colors.PRIMARY, end="")
        url_input = input().strip()
        
        if not url_input:
            print_colored("URL cannot be empty!", Colors.ERROR)
            return
        
        print_section_header("STARTING SCAN")
        print_colored(f"Target: {url_input}", Colors.INFO)
        print_colored(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", Colors.INFO)
        
        scan_website(url_input)
        
        print_colored(f"\n{Colors.SECONDARY}Thank you for using ChowdhuryVai Website Scanner!{Colors.END}", Colors.SECONDARY)
        
    except KeyboardInterrupt:
        print_colored(f"\n\n{Colors.WARNING}Scan canceled by user.{Colors.END}", Colors.WARNING)
    except Exception as e:
        print_colored(f"\n{Colors.ERROR}Unexpected error: {str(e)}{Colors.END}", Colors.ERROR)

if __name__ == "__main__":
    main()
