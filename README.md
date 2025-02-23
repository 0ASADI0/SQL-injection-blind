
# SQL Injection Exploitation Tool

## Description

This is a Python-based tool designed for **blind SQL injection** attacks, supporting **Boolean-Based** and **Time-Based** techniques. The tool automates the process of extracting valuable data such as **database names**, **table names**, **column names**, and **flag values** from a vulnerable web application.

The tool features **colored output** for easier reading and integrates with **Burp Suite** via a proxy, enhancing penetration testing efforts. It is intended for **educational purposes** and should only be used in environments where you have explicit permission to conduct security testing.

## Features

- **Automated extraction of database-related information**.
- **Supports Boolean-Based and Time-Based SQL injection attacks**.
- **Burp Suite proxy support** for enhanced testing.
- **Detailed, color-coded feedback** to help identify critical data points quickly.
- **User-friendly interface** with action prompts for each stage of the attack.

## Requirements

- Python 3.x
- `requests` library
- `colorama` library
- A working **Burp Suite** proxy (if using for interception)
- SSL certificate handling (optional, depending on the server configuration)

## Installation

### Clone the repository:

```bash
git clone https://github.com/yourusername/sql-injection-exploitation-tool.git
cd sql-injection-exploitation-tool
```

### Install the required libraries:

```bash
pip install -r requirements.txt
```

## Usage

1. **Start Burp Suite** (if using for interception).
2. **Configure Burp Suite Proxy** to `http://127.0.0.1:8080` in the tool.
3. **Run the tool:**

```bash
python booleanblind.py
```

4. **Choose the attack type**:
   - **Boolean-Based Blind SQL Injection**
   - **Time-Based Blind SQL Injection**

5. **Select the action** to retrieve:
   - Get Database Length
   - Get Database Name
   - Get Table Name
   - Get Column Name
   - Get Flag

Follow the on-screen prompts to extract the required data.

## Example Output

```bash
Please Enter Your Lab Link: https://example.com/index.php?id=1
Choose attack type:
1. Boolean-Based Blind SQL Injection
2. Time-Based Blind SQL Injection
Enter choice: 1

Choose an action:
1. Get Database Length
2. Get Database Name
3. Get Table Name
4. Get Column Name
5. Get Flag
Enter choice: 2

[+] Database Length Found: 12
[+] Character found: s at position 1
[+] Character found: q at position 2
...
```

## Disclaimer

This tool is intended for **ethical hacking** and **penetration testing**. It must only be used in environments where you have explicit authorization. Unauthorized use of this tool on live systems is illegal and unethical. Always respect privacy and legal boundaries.


