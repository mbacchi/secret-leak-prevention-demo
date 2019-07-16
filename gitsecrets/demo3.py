import os
import shutil
import subprocess


def run_cmd(arr):
    print('\nRunning the command: ', end='')
    print('\'', end='')
    for i in arr:
        print("{} ".format(i), end='')
    print('\'')
    prompt_any_key()
    p = subprocess.Popen(arr, stdout=subprocess.PIPE)
    print()
    print(p.communicate()[0].decode())


def prompt_any_key():
    try:
        input("Press any key to continue... ")
    except SyntaxError:
        pass


def create_pre_commit_hook():

    d = '.git/hooks/pre-commit'
    if not os.path.exists(d):
        print("Creating the file \'{}\'".format(d))
        #
        # with open('gitsecrets/pre-commit.txt', 'r') as infile:
        #     data = infile.read().replace('\n', '')
        # with open(d, 'w') as f:
        #     f.write(data)
        shutil.copyfile('gitsecrets/pre-commit.txt', '.git/hooks/pre-commit')
    else:
        print("pre-commit hook already exists: {}".format(d))


if __name__ == '__main__':

    print("Starting git-secrets demo...\n\n")

    print("Cloning repository \"git@github.com:awslabs/git-secrets.git\"")

    run_cmd(['git', 'clone', 'git@github.com:awslabs/git-secrets.git'])

    print("git-secrets help output:")
    if os.path.exists('git-secrets/git-secrets'):
        run_cmd(['git-secrets/git-secrets', '--help'])
    else:
        print('file git-secrets/git-secrets not found')
        exit(1)

    # register aws patterns
    print("Registering common AWS patterns to git config")
    run_cmd(['git-secrets/git-secrets', '--register-aws'])

    # git config -l | grep secrets
    print("Now run the command (manually in another terminal) "
            "\"git config -l | grep secrets\" to look at the patterns"
            " that have been set future invocations of git-secrets...")
    prompt_any_key()

    # cat .aws/credentials
    run_cmd(['cat', '.aws/credentials'])

    # run git secrets to demonstrate functionality
    run_cmd(['git-secrets/git-secrets', '--scan', '-r', '.'])

    # create pre-commit hook which runs git-secrets
    create_pre_commit_hook()

    print("changing permissions of file \".git/hooks/pre-commit\"")
    run_cmd(['chmod', '744', '.git/hooks/pre-commit'])

    # git add .aws/credentials
    run_cmd(['git', 'add', '.aws/credentials'])

    # git commit (this should generate an error from the pre-commit hook)
    run_cmd(['git', 'commit', '-m', 'blahblah'])

    # remove pre-commit hook
    print("Removing pre-commit hook \'.git/hooks/pre-commit\'")
    os.unlink('.git/hooks/pre-commit')

    # git unstage .aws/credentials
    print("Unstaging file \'.aws/credentials\'")
    run_cmd(['git', 'rm', '--cached', '.aws/credentials'])

    # unregister AWS patterns added above
    # this is not necessary for this demo, it simply adds the aws patterns
    # to the .git/config file in the current repository
    # if you want to do this manually edit that file and remove
    # the providers/patterns/allowed lines.

    # remove git-secrets clone directory
    print("Removing git-secrets clone directory")
    shutil.rmtree('git-secrets')
