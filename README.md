# Secret Leak Prevention

This is a demonstration of how to prevent secrets (such as AWS
credentials) from being leaked to Github. It is modeled after the
blog post I wrote [about preventing Github secret exposures.](http://mbacchi.github.io/2017/12/22/3-ways-prevent-secret-leaks-github.html)

The AWS Labs git-secrets tool is available [here](https://github.com/awslabs/git-secrets)

### Installation / Requirements

These demo scripts requires the Python 3 interpreter.

There is no need to install these demo scripts anywhere. Simply clone
this Github repository and run the scripts by hand, such as:

`python3 gitignore/demo1.py`


### Leveraging the `.gitignore` file

The `.gitignore` file allows you to tell Git not to acknowledge files
that you want to exclude from a Git repository. This can be configured
globally for a user, or in a specific directory such as a repository
itself. Run `man gitignore` to get full help. You can still force a file
to be included with `git add` and `git commit` but you have to really
forget about the fact that you have added it to the `.gitignore` file.

Our [demo script
`demo1.py`](https://github.com/mbacchi/secret-leak-prevention-demo/blob/master/gitignore/demo1.py)
will show how to utilize this functionality to prevent a file or directory from
being checked into Git.

### How to use the Git Pre-commit Hook

Git also gives us the ability to use hooks for certain actions. In this
case we will use the pre-commit hook to perform some action just prior
to actually allowing a `git commit` from being executed. Again, use
`man githooks` to learn how to use these tools.

In [our demo script
`demo2.py`](https://github.com/mbacchi/secret-leak-prevention-demo/blob/master/pre-commit/demo2.py),
we will show how do this with a simple test for a file name called `credentials`
which usually contains an AWS key ID/secret key.

FYI, a pre-commit hook script must be executable! If it is not it will
not run and silently allow your commits.

### AWS Labs git-secrets

AWS Labs created a bash tool that will look in a file or recursively
search a directory structure for certain patterns. Obviously the most
common pattern we're thinking about is the AWS key ID/secret key.

In the [script
demo3.py](https://github.com/mbacchi/secret-leak-prevention-demo/blob/master/gitsecrets/demo3.py)
we will set up a pre-commit hook that runs git-secrets and exits if there is an
AWS credential found.

### Running python-git-secrets in an AWS Lambda Function

The [fourth
demo](https://github.com/mbacchi/secret-leak-prevention-demo/tree/master/lambda-python-git-secrets)
uses the library
[python-git-secrets](https://github.com/mbacchi/python-git-secrets) in an AWS
Lambda function to clone a GitHub repository, then scan the repository for
secrets.


#### Meta

Matt Bacchi

Distributed under the BSD (Simplified) license. See LICENSE for more information.