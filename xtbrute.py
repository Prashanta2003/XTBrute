import asyncio
import argparse
import sys
import time
from typing import List, Optional
import aiohttp
from colorama import Fore, Style, init
from art import text2art
import signal
from datetime import datetime
import random

init(autoreset=True)

class XTBrute:
    def __init__(self):
        self.banner = text2art("XT903", font="big")
        self.version = "1.0.0"
        self.author = "XT903"
        self.stop = False
        self.success_count = 0
        self.error_count = 0

    def display_banner(self):
        print(f"{Fore.RED}{Style.BRIGHT}{self.banner}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Created by {self.author} | Version {self.version}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")

    async def fetch(self, session: aiohttp.ClientSession, url: str, args) -> tuple:
        headers = {"User-Agent": args.user_agent}
        if args.headers:
            for header in args.headers:
                key, value = header.split(":", 1)
                headers[key.strip()] = value.strip()

        try:
            async with session.get(
                url,
                timeout=args.timeout,
                ssl=not args.no_ssl,
                proxy=args.proxy,
                allow_redirects=args.follow_redirects
            ) as response:
                status = response.status
                content_length = response.headers.get("Content-Length", "0")
                return status, content_length
        except Exception as e:
            return str(e), 0

    async def worker(self, queue: asyncio.Queue, session: aiohttp.ClientSession, args):
        while not queue.empty() and not self.stop:
            path = await queue.get()
            url = f"{args.url.rstrip('/')}/{path.lstrip('/')}"
            if args.append_slash:
                url += "/"
            
            status, content_length = await self.fetch(session, url, args)
            
            if isinstance(status, int):
                if status in args.status_codes:
                    print(
                        f"{Fore.BLUE}[+] {url} (Status: {status}) [Size: {content_length}]{Style.RESET_ALL}"
                    )
                    self.success_count += 1
                    if args.output:
                        with open(args.output, "a") as f:
                            f.write(f"{url} (Status: {status}) [Size: {content_length}]\n")
            else:
                if args.verbose:
                    print(
                        f"{Fore.YELLOW}[-] {url} (Error: {status}){Style.RESET_ALL}"
                    )
                self.error_count += 1

            queue.task_done()

    async def run(self, args):
        self.display_banner()
        
        # Load wordlist
        try:
            with open(args.wordlist, "r") as f:
                wordlist = [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f"{Fore.RED}Error reading wordlist: {e}{Style.RESET_ALL}")
            return

        # Setup queue
        queue = asyncio.Queue()
        for word in wordlist:
            if args.extensions:
                for ext in args.extensions:
                    await queue.put(f"{word}.{ext}")
            await queue.put(word)

        # Setup aiohttp session
        timeout = aiohttp.ClientTimeout(total=args.timeout)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            tasks = [
                self.worker(queue, session, args)
                for _ in range(args.threads)
            ]
            
            start_time = datetime.now()
            print(f"{Fore.CYAN}Starting brute-force at {start_time}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Target: {args.url} | Threads: {args.threads} | Wordlist size: {len(wordlist)}{Style.RESET_ALL}\n")

            await asyncio.gather(*tasks)
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            print(f"\n{Fore.GREEN}Completed in {duration:.2f} seconds")
            print(f"Successes: {self.success_count} | Errors: {self.error_count}{Style.RESET_ALL}")

    def graceful_shutdown(self):
        self.stop = True
        print(f"\n{Fore.YELLOW}Initiating graceful shutdown...{Style.RESET_ALL}")
        
        # Animated exit message
        messages = [
            "Thank you for using XTBrute!",
            "Shutting down safely...",
            "Hope to see you again!",
            "Stay secure!"
        ]
        
        for msg in messages:
            print(f"{Fore.MAGENTA}{msg}{Style.RESET_ALL}", end="\r")
            time.sleep(0.5)
        print(f"{Fore.MAGENTA}Goodbye!{Style.RESET_ALL}")
        sys.exit(0)

def parse_args():
    parser = argparse.ArgumentParser(
        description="XTBrute - Advanced Web Directory Brute-Forcing Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("-u", "--url", required=True, help="Target URL (e.g., http://example.com)")
    parser.add_argument("-w", "--wordlist", required=True, help="Path to wordlist file")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Number of concurrent threads (default: 10)")
    parser.add_argument("-o", "--output", help="Output file to save results")
    parser.add_argument("-x", "--extensions", help="File extensions to check (e.g., php,txt,html)")
    parser.add_argument("-s", "--status-codes", default="200,204,301,302,307,401,403",
                        help="Comma-separated list of status codes to consider as positive (default: 200,204,301,302,307,401,403)")
    parser.add_argument("--timeout", type=float, default=10.0, help="HTTP request timeout in seconds (default: 10)")
    parser.add_argument("--user-agent", default="XTBrute/1.0.0",
                        help="Custom User-Agent string (default: XTBrute/1.0.0)")
    parser.add_argument("--headers", nargs="*", help="Custom headers (format: 'Key: Value')")
    parser.add_argument("--proxy", help="Proxy URL (e.g., http://localhost:8080)")
    parser.add_argument("--no-ssl", action="store_true", help="Disable SSL verification")
    parser.add_argument("--follow-redirects", action="store_true", help="Follow HTTP redirects")
    parser.add_argument("--append-slash", action="store_true", help="Append slash to each request")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show verbose output including errors")
    
    args = parser.parse_args()
    if args.extensions:
        args.extensions = args.extensions.split(",")
    args.status_codes = [int(code) for code in args.status_codes.split(",")]
    return args

def main():
    xtbrute = XTBrute()
    
    # Handle Ctrl+C
    def signal_handler(sig, frame):
        xtbrute.graceful_shutdown()
    
    signal.signal(signal.SIGINT, signal_handler)
    
    args = parse_args()
    asyncio.run(xtbrute.run(args))

if __name__ == "__main__":
    main()
