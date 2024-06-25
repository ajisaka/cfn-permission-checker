# cfn-permission-checker

`cfn-permission-checker` is a command-line tool that extracts CloudFormation events from CloudTrail logs to verify the permissions required for deployment.

## Features

- Extract and analyze CloudFormation deployment events from CloudTrail logs
- Filter events by time range
- Display specific properties of events
- Help troubleshoot permission issues and audit CloudFormation deployments

## Usage

### Displaying Events

To display events from 2 hours ago:

```sh
cfn-permission-checker filter --from '2h'
```

To display specific properties of events:

```sh
cfn-permission-checker filter --from '2h' -p 'requestParameters'
```

## Setup

### Prerequisites

1. AWS SAM CLI - Required to deploy the CloudTrail stack
2. Rye - Package manager for Python projects

### Install AWS SAM CLI

To enable CloudTrail, you need to deploy an AWS SAM stack. Please refer to the [official AWS SAM CLI documentation](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html) for installation instructions.

### Deploy the CloudTrail Stack

```sh
cd sam
make
```

### Install Rye

Install Rye by following the [official Rye installation guide](https://github.com/astral-sh/rye?tab=readme-ov-file#installation).

### Install cfn-permission-checker

Once Rye is installed, you can install `cfn-permission-checker` using the following command:

```sh
rye tools install --git 'https://github.com/ajisaka/cfn-permission-checker#subdirectory=app/' cfn-permission-checker
```

This will install the `cfn-permission-checker` command-line tool.

## Examples

Here are some additional examples of how to use cfn-permission-checker:

```sh
# Filter events from the last 24 hours
cfn-permission-checker filter --from '24h'

# Display only the 'eventName' and 'userIdentity' properties
cfn-permission-checker filter --from '1d' -p 'eventName' -p 'userIdentity'

# Save output to a JSON file
cfn-permission-checker filter --from '1w' > cfn_events.json
```

## Troubleshooting

If you encounter any issues during installation or usage, please check the following:

1. Ensure you have the latest versions of AWS SAM CLI and Rye installed.
2. Verify that your AWS credentials are properly configured.
3. Check the CloudTrail logs to ensure events are being recorded correctly.

For more detailed information, please refer to the project's GitHub repository or open an issue if you encounter any problems.
