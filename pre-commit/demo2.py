import os
import subprocess


def run_cmd(arr):
    print('\nRunning the command: ', end='')
    print('\'', end='')
    for i in arr:
        print("{} ".format(i), end='')
    print('\'')
    prompt_any_key()
    p = subprocess.Popen(arr,
                         stdout=subprocess.PIPE)
    print()
    print(p.communicate()[0].decode())


def prompt_any_key():
    try:
        input("Press any key to continue... ")
    except SyntaxError:
        pass


def create_pre_commit_hook():

    script = """#!/bin/bash
#
# A git hook to check whether credentials files exist in the staged files list

RESPONSE=$(git status -s| grep credentials)

if [[ "$RESPONSE" == *"credentials"* ]]; then
    # credential is included in the staged files
    echo "ERROR: [pre-commit hook] Aborting commit because you have the file \"credentials\" staged to be committed."
    echo "Remove it from the repository using \"git rm --cached credentials\""
    echo
    exit 1
else
    # not found
    exit 0
fi"""

    d = '.git/hooks/pre-commit'
    if not os.path.exists(d):
        print("Creating the file \'{}\'".format(d))
        with open(d, 'w') as f:
            f.write(script)


if __name__ == '__main__':

    print("Starting git pre-commit hook demo...\n\n")

    create_pre_commit_hook()

    run_cmd(['cat', '.git/hooks/pre-commit'])

    print("changing permissions of file \".git/hooks/pre-commit\"")
    run_cmd(['chmod', '744', '.git/hooks/pre-commit'])

    run_cmd(['git', 'add', '.aws/credentials'])

    run_cmd(['git', 'status'])

    run_cmd(['git', 'commit', '-m', 'blahblah'])

    # remove pre-commit hook
    print("Removing pre-commit hook \'.git/hooks/pre-commit\'")
    os.unlink('.git/hooks/pre-commit')

    # git unstage .aws/credentials
    print("Unstaging file \'.aws/credentials\'")
    run_cmd(['git', 'rm', '--cached', '.aws/credentials'])
