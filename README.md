### XTBrute
XTBrute is an advanced web directory brute-forcing tool designed to enumerate directories and files on web servers. It uses asynchronous HTTP requests to efficiently scan for valid endpoints based on a provided wordlist, with support for custom headers, proxies, and file extensions.
Features

Asynchronous HTTP requests for high performance
Support for custom User-Agent, headers, and proxies
Configurable HTTP status codes to consider as positive
Optional SSL verification and redirect handling
Verbose output and result logging to a file
Graceful shutdown with animated exit messages
Support for appending slashes and file extensions

Installation

```
Clone the repository:
git clone https://github.com/yourusername/XTBrute.git
cd XTBrute
```

Install dependencies:
```
python3 -m venv XTBrute
source XTBrout/bin/activate
pip install -r requirements.txt
```


Usage
Run the tool with the required arguments (--url and --wordlist):
```
python xtbrute.py -u http://example.com -w wordlist.txt
```
Options
```
-u, --url: Target URL (required, e.g., http://example.com)
-w, --wordlist: Path to wordlist file (required)
-t, --threads: Number of concurrent threads (default: 10)
-o, --output: Output file to save results
-x, --extensions: Comma-separated file extensions (e.g., php,txt,html)
-s, --status-codes: Comma-separated status codes to consider (default: 200,204,301,302,307,401,403)
--timeout: HTTP request timeout in seconds (default: 10)
--user-agent: Custom User-Agent (default: XTBrute/1.0.0)
--headers: Custom headers (format: Key: Value)
--proxy: Proxy URL (e.g., http://localhost:8080)
--no-ssl: Disable SSL verification
--follow-redirects: Follow HTTP redirects
--append-slash: Append slash to each request
-v, --verbose: Show verbose output including errors
```
Example
```
python xtbrute.py -u http://example.com -w wordlist.txt -t 20 -x php,html -o results.txt --verbose
```
Requirements
See requirements.txt for the list of Python dependencies.
License
This project is licensed under the MIT License. See the LICENSE file for details.
Contributing
Contributions are welcome! Please open an issue or submit a pull request on GitHub.
Author

XT903 (Version 1.0.0)

Disclaimer
This tool is intended for ethical security testing and research purposes only. Do not use it on systems without explicit permission from the owner. The author is not responsible for misuse or damage caused by this tool.
