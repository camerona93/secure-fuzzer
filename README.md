# secure-fuzzer
Fuzzer project for SE 331-01

## Running
In order to run this project, you'll need a few python modules installed on your machine. These can be obtained using pip or easy_install if you don't have them. The required modules are:
 - `requests`
 - 'beautifulsoup4'

 The following are also required but should be standard with all Python installs:
 - `argparse`
 - `urllib` (Should be included with all python installations)
 - 'html' (Should be included with all python installations)

To run the program, type `python fuzzer.py` from a terminal prompt in the project directory with your specified arguments. For help, type `python fuzzer.py -h`
A good one to try is: `python fuzzer.py discover http://127.0.0.1/dvwa --custom-auth dvwa --common-words SecLists/Discovery/Web_content/apache.txt`

## SecLists
To promote good development, we decided to make use of some lists compiled specifically for security/fuzzing. A GitHub project consiting of such lists is located at https://github.com/danielmiessler/SecLists. According to the readme,
>SecLists is the security tester's companion. It's a collection of multiple types of lists used during security assessments, collected in one place. List types include usernames, passwords, URLs, sensitive data patterns, fuzzing payloads, web shells, and many more. The goal is to enable a security tester to pull this repo onto a new testing box and have access to every type of list that may be needed.
