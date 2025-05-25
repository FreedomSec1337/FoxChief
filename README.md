

🦊 FoxChief - Advanced File Hunter 🦊

FoxChief is an advanced file crawler designed to scan a target URL, identify files of specific types (such as PDFs, Word documents, Excel spreadsheets, etc.), and save the results in an SQLite database. It is built using Python and offers a simple yet powerful tool to gather downloadable files from a web page.


---

Features

Crawls a given URL to find links to downloadable files.

Supports multiple file types (e.g., .pdf, .docx, .xlsx, .csv, .json, etc.).

Saves the URLs, file types, and file sizes (in KB) to an SQLite database.

Uses BeautifulSoup for HTML parsing and requests for making HTTP requests.

Displays rich, styled terminal output using the rich library.

Provides an easy-to-use CLI interface for specifying target URLs.



---

Requirements

Before running FoxChief, make sure you have the following Python libraries installed:

requests

beautifulsoup4

rich

tldextract

sqlite3 (usually included with Python)


You can install the necessary libraries using pip:

pip install requests beautifulsoup4 rich tldextract


---

Installation

1. Clone this repository to your local machine:

git clone [](https://github.com/FreedomSec1337/FoxChief)


2. Navigate to the project directory:

cd foxchief


3. Install the required Python librarie

---

Usage

Command-Line Interface (CLI)

To start crawling, run the following command with the target URL:

python foxchief.py <target-url>

Example:

python foxchief.py https://example.com

This will:

Crawl the given URL.

Find all links to files with the specified extensions (.pdf, .docx, .xlsx, etc.).

Display the found files' URLs and sizes in the terminal.

Save the results in an SQLite database (foxchief_results.db).



---

Example Output

🦊 FoxChief - Advanced File Hunter 🦊
Target: https://example.com

[CRAWL] https://example.com
[FOUND] https://example.com/file1.pdf ([yellow] 45.67 KB[/yellow])
[FOUND] https://example.com/file2.docx ([yellow] 12.34 KB[/yellow])

✅ Total files found: 2 | Time taken: 3.5 seconds
📄 Results saved to: foxchief_results.db


---

Database Schema

The results are saved in an SQLite database (foxchief_results.db) with the following schema:

id (INTEGER PRIMARY KEY): Auto-incrementing ID for each record.

url (TEXT): The URL of the file.

file_type (TEXT): The file extension/type (e.g., .pdf, .docx).

size_kb (REAL): The file size in kilobytes (KB).

timestamp (DATETIME): The time when the file was found.



---

Contribution

If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request!


