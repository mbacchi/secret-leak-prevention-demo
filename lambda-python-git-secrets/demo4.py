import os
import random
import re
import shutil

from dulwich import porcelain
from gitsecrets import GitSecrets
from string import ascii_uppercase, ascii_lowercase, digits

# For this demo we use Dulwich instead of Git to clone a repository from GitHub.
#
# This is because in an AWS Lambda function we don't want to rely on arbitrary
# binaries such as Git being installed, we would rather use pure Python tools,
# such as Dulwich.
#
# Dulwich is available via pip, or at https://github.com/jelmer/dulwich
#
# We also use python-git-secrets which is available via pip, or at
# https://github.com/mbacchi/python-git-secrets.git
#

class Devnull(object):
    """
    This mimics a stream to write to for dulwich porcelain status output. Since we
    don't want to see the status this is a hack to suppress anything printing on stdout.

    Borrowed from:
    https://stackoverflow.com/questions/2929899/cross-platform-dev-null-in-python
    """
    def write(self, *_): pass

def newfile(path, content):

    with open(path, "w") as f:
        f.write(content + '\n')

def python_git_secrets(event, context):

    # Set the GitHub repository to clone and the directory to clone into for
    # demonstration purposes
    repo = 'https://github.com/mbacchi/python-git-secrets.git'
    target = '/tmp/python-git-secrets'

    # If the target path exists remove it so we don't error out when cloning
    # later
    if os.path.exists(target):
        print("Removing directory \'{}\'...".format(target))
        shutil.rmtree(target)

    print("Cloning repository \'{}\' into \'{}\'...\n".format(repo, target))

    # Perform the clone operation
    nullstream = open(os.devnull, "w")
    newrepo = porcelain.clone(repo, target, errstream=Devnull())

    # Create a random uppercase string that looks like an AWS ACCES_KEY_ID value
    print("Creating file in directory \'{}\' with content that looks like an AWS ACCESS_KEY_ID\n".format(target))
    patterns = [''.join("A3T" + random.choice(ascii_uppercase)), 'AKIA',
                'AGPA', 'AIDA', 'AROA', 'AIPA', 'ANPA', 'ANVA', 'ASIA']
    prefix = random.choice(patterns)
    generated = ''.join(random.choice(ascii_uppercase) for _ in range(16))
    key = prefix + generated
    newfile(target + '/aws-credentials', "aws_access_key_id=" + key)

    # Show the users the string we placed in the file above
    print("Contents of file: \'{}\':".format(target + '/aws-credentials'))
    with open(target + '/aws-credentials', "r") as f:
        blah = f.read().rstrip()
    print("\'{}\'\n".format(blah))

    # Instantiate the GitSecrets class
    gs = GitSecrets()

    # Scan the repository which should find a string because we created a file
    # with a sample AWS_ACCESS_KEY above
    print("Now scanning directory \'{}\' for secrets".format(target))
    if gs.scan_recursively(target):
        print("Found verboten string in path \'{}\'".format(target))
