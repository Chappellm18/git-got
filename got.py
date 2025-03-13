import sys
from os import walk
import os
import re
from datetime import datetime
import shutil

def add(command):
    print(f"Executing add command: {command}")
    filenames = []
    
    if command[1] == '*':
        # Get all files in the current directory
        filenames = next(walk(os.getcwd()), (None, None, []))[2]
        if len(filenames) == 0:
            print('No files to commit')
        else:
            print(f"{len(filenames)} file(s) added")
    elif '**' in command[1]:
        # Get all files matching a specific extension
        filenames = next(walk(os.getcwd()), (None, None, []))[2]
        ext_pattern = re.findall(r"\.(\w+)", command[1])
        filenames = [f for f in filenames if os.path.splitext(f)[1][1:] in ext_pattern]
        print(f"{len(filenames)} file(s) added")
    elif os.path.exists(command[1]):
        # If a specific file or folder is provided, ensure it’s added
        if os.path.isdir(command[1]):
            filenames = [os.path.join(command[1], f) for f in os.listdir(command[1])]
        else:
            filenames = [os.path.abspath(command[1])]
        print(f"Added: {filenames}")
    else: 
        print('Error: Check command format')
        
    return filenames

def commit(filenames): 
    return {'files': filenames, 'time': datetime.now()}

def push(commits, commit_history, external_repo):
    # Append commit data to commit history
    with open(commit_history, "a") as file:
        for commit in commits:
            file.write(f"{commit['time']} - {commit['files']}\n")
    
    # Copy files to external repository folder
    for commit in commits:
        for file in commit['files']:
            shutil.copy(file, external_repo)
            print(f"File {file} pushed to {external_repo}")

def main():
    commited = False
    added_filenames = []
    commits = []
    commit_history = './external/commit.txt'
    external_repo = './external'

    if not os.path.exists(external_repo):
        os.makedirs(external_repo)

    while True:
        # Prompt for user input
        command = input("Enter command: ")

        if 'add' in command:
            added_filenames = add(command.split(' '))
        elif 'commit' in command:
            if len(added_filenames) == 0:
                print('No file(s) to commit')
            else:
                commits.append(commit(added_filenames))
                commited = True
        elif 'push' in command:
            if commited:
                push(commits, commit_history, external_repo)
                commits.clear()  # Clear the commit history after pushing
                commited = False  # Reset commit state
            else:
                print("No commit(s) to push")
        elif 'exit' in command:
            print("Exiting the program.")
            break
        else:
            print(f"Unknown command: {command}")

if __name__ == '__main__':
    main()
