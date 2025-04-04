import sys
from os import walk
import os
import re
from datetime import datetime
import shutil
import hashlib

global currentBranch

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
    hasFiles(external_repo)

    # Append commit data to commit history
    with open(commit_history, "a") as file:
        for commit in commits:
            file.write(f"{commit['time']} - {commit['files']}\n")
    
    # Copy files to external repository folder
    for commit in commits:
        for file in commit['files']:
            shutil.copy(file, external_repo)
            print(f"File {file} pushed to {external_repo}")

def branch(name):
    os.mkdir('./external/'+name)
    files = os.listdir(currentBranch)
    for file in files:
        shtil.copyfile(currentBranch + '/' + file, './external/'+name+'/'+file)
    currentBranch = './external/'+name

def listBranches():
    branches = os.listdir('./external')
    for branch in branches:
        print(branch +'\n')

def switchBranches(newBranch):
    # clear working dir
    # get the new .gotfiles
    readHash(newBranch)


def hashFiles(branch):
    # take the current branch, hash the files, store in .gotfiles
    BUF_SIZE = 65536

    files = os.listdir(branch)
    with open(branch+'/.gotfiles', 'w') as gf:    
        for file in files:
            with open(branch+'/'+file) as f:
                sha1 = hashlib.sha1()
                while True:
                    data = f.read(BUF_SIZE)
                    if not data:
                        break
                    sha1.update(data)
                gf.write(sha1 +'\n')

def readHash(branch):
    # take the current branch, read the hash and populate the workingDir
    print('')

def main():
    commited = False
    added_filenames = []
    commits = []
    external_repo = './external/main'
    currentBranch = external_repo

    commit_history = currentBranch + '/commit.txt'
    workingDir = './'

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
                push(commits, commit_history, currentBranch)
                commits.clear()  # Clear the commit history after pushing
                commited = False  # Reset commit state
            else:
                print("No commit(s) to push")
        elif 'branch' in command:
            cmmd = command.split(' ')
            branch(cmmd[1])
        elif 'list' in command:
            listBranches()
        elif 'exit' in command:
            print("Exiting the program.")
            break
        else:
            print(f"Unknown command: {command}")

if __name__ == '__main__':
    main()
