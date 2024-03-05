# Secret Leak Prevention

This is a demonstration of how to prevent secrets (such as AWS
credentials) from being leaked to Github. It is modeled after the
blog post I wrote [about preventing Github secret exposures.](https://bacchi.org/posts/3-ways-prevent-secret-leaks-github/)

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

### Using AWS IAM Roles instead of Access Keys

The surest way of avoiding leaking your AWS Access Keys and Secret Access Keys
is to simply not create them in the first place. AWS Access Keys were the
earliest mechanism that AWS provided for authenticating yourself programatically
when performing AWS CLI operations. Today we are not forced to use this method,
and have the ability to define IAM roles to grant authority to perform specific
and granular AWS actions.

One action that can be authenticated via roles, is to allow an EC2 instance to
access specific AWS resources using an [instance
profile](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-ec2_instance-profiles.html).
This allows the EC2 instance to assume the role and gain the authority of that
role. With this you can grant the authority to an EC2 instance to write to an S3
bucket for instance.

Another way your IAM role gives you flexibility is to grant one user in a
specific AWS account the authority to assume a role in another AWS account. Thus
providing cross AWS account authorization to perform actions.

Our [last
demo](https://github.com/mbacchi/secret-leak-prevention-demo/tree/master/aws-role-ec2-assumerole)
is a straightforward example showing an EC2 instance using an AWS role to write to
an S3 bucket.

### AWS CLI credentials, profiles and aws-vault

These demos all talk about handling AWS credentials safely. In addition to the
tools above that perform active verification that you have no secrets in your
Github repositories, there are other tools and best practices that users should
be using to assist in keeping these secrets safe. These are:

#### Using AWS Profiles

You can configure AWS profiles in your home `.aws` directory so that you don't
ever place credentials near your Github repositories. Follow [these
instructions](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-profiles.html)
to setup profiles.

Then you will use these profiles by exporting them on the command line, such as:

```
export AWS_PROFILE=user1 && export AWS_REGION=us-east-2
```

After which you can run AWS CLI commands and the commands will be run using the
profile specified.

#### AWS Vault

Another great tool is [aws-vault](https://github.com/99designs/aws-vault) which
stores credentials in your operating system secure keystore. This is
instrumental in keeping your credentials both safe from accidental release in a
Github repository, but also kept safe from prying eyes who might have access to
view your `.aws` directory in your home directory.

#### Meta

Matt Bacchi

Distributed under the BSD (Simplified) license. See LICENSE for more information.
