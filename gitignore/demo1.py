import os
import random
from string import ascii_uppercase, ascii_lowercase, digits
import subprocess


def add_dot_aws_to_dot_gitignore():
    print("Adding the directory '.aws/' to the .gitignore file")
    with open(".gitignore", 'w') as f:
        f.write(".aws/" + '\n')
    f.close()


def create_dot_aws_dir_and_credentials():
    d = '.aws'
    if not os.path.exists(d):
        print("Creating the directory .aws")
        os.makedirs(d)
    print("Creating the .aws/credentials file")
    with open('.aws/credentials', 'w') as f:
        key_id = ''.join(random.choice(ascii_uppercase) for _ in range(20))
        chars = ascii_uppercase + ascii_lowercase + digits
        secret_key = ''.join(random.choice(chars) for _ in range(40))
        print("adding aws_access_key_id \"{}\" to .aws/credentials file"
              .format(key_id))
        f.write("aws_access_key_id=" + key_id + '\n')
        print("adding aws_secret_access_key \"{}\" to .aws/credentials file"
              .format(secret_key))
        f.write("aws_secret_access_key=" + secret_key + '\n')
    f.close()


def remove_dot_gitignore():
    print("Removing file \".gitignore\"")
    os.unlink('.gitignore')


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

if __name__ == '__main__':

    print("Starting .gitignore demo...\n\n")

    create_dot_aws_dir_and_credentials()

    run_cmd(['cat', '.aws/credentials'])

    add_dot_aws_to_dot_gitignore()

    print()
    print("Lets look at the .gitignore contents...")
    run_cmd(['cat', '.gitignore'])

    run_cmd(['git', 'check-ignore', '-v', '.aws'])

    run_cmd(['git', 'add', '.aws/credentials'])

    remove_dot_gitignore()
