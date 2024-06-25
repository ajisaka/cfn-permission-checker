# Setup

## Install SAM Client

To enable CloudTrail, you need to deploy an AWS SAM stack. Please refer to the [official documentation](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html) for installation instructions.

## Deploy the Stack

```sh
$ cd sam
$ make
```

## Install Rye

First, install Rye by following the [official installation guide](https://github.com/astral-sh/rye?tab=readme-ov-file#installation).

## Install cfn-permission-checker

Once Rye is installed, you can install `cfn-permission-checker` using the following command:

```sh
$ rye tools install --git 'https://github.com/ajisaka/cfn-permission-checker#subdirectory=app/' cfn-permission-checker
```

This will install the `cfn-permission-checker` command-line tool.
