# Get Started

This project sets up an event-driven Generative AI Intelligent Document Processing (IDP) application using AWS services.

## Prerequisites

To implement this solution, you need the following:

- An AWS account – You need access to an AWS account with the necessary permissions to deploy and manage the required services. If you don’t have an account, you can sign up for one.
- IAM role – We use AWS Identity and Access Management (IAM) to manage user access and permissions for the various AWS services used in this solution.
3Python environment – You need a Python development environment with the necessary libraries, such as pdfplumber or other PDF parsing tools.
- AWS CLI and Docker installed – Make sure you have the AWS Command Line Interface (AWS CLI) installed and configured, and Docker installed on your local machine.

### Create an ECR repository and push the custom Docker image

Complete the following steps to create your ECR repository and push the custom Docker image. If you don’t have the AWS CLI and Docker installed, we recommend using AWS Cloud9 to check in the Docker image. 

1. Run the following command to create your docker image:
   ```
   cd ./docker && docker build -t <your-local-image>:<tag> .
   ```

2. Create an ECR repository:
   ```
   aws ecr create-repository --repository-name <your-repo-name>
   ```

3. Authenticate Docker to your ECR registry:
   ```
   aws ecr get-login-password --region your-region | docker login --username AWS --password-stdin <your-account-id>.dkr.ecr.<your-region>.amazonaws.com
   ```

4. Tag your Docker image:
   ```
   docker tag <your-local-image>:<tag> <your-account-id>.dkr.ecr.<your-region>.amazonaws.com/<your-repo-name>:<tag>
   ```

5. Push the image to Amazon ECR:
   ```
   docker push <your-account-id>.dkr.ecr.<your-region>.amazonaws.com/<your-repo-name>:<tag>
   ```

6. Note down the ECR image URL for use in the CloudFormation template.

## Deployment

### 1. Deploy the CloudFormation stack

To deploy the solution resources using AWS CloudFormation, complete the following steps:

1.	Choose Launch Stack:

[Cloudformation image goes here]

2.	For Stack name, enter a unique name.
3.	For BedrockModelId, enter the Amazon Bedrock model ID (for example, anthropic.claude-3-sonnet-20240229-v1:0).
4.	For ECRRepositoryUri, enter the ECR image URL you noted earlier.
5.	Review and create the stack.

Stack creation will take a few minutes to complete.

### 2. Upload processing scripts

Complete the following steps to upload the processing scripts to Amazon S3:

1.	Locate the ScriptBucketName value in the CloudFormation stack outputs.
2.	Upload all the scripts and templates from ./src to the script S3 bucket:

   ```
   aws s3 cp ./src s3://your-script-bucket-name/scripts/ --recursive
   ```

### 3. Process PDF Files

Complete the following steps to process the PDF files:

1.	Locate the InputBucketName value in the CloudFormation stack outputs.
2.	Upload a PDF file to the input S3 bucket to invoke processing:

   ```
   aws s3 cp your-file.pdf s3://your-input-bucket-name/
   ```

The system will automatically process the PDF and store the results in the output S3 bucket (OutputBucketName).

## Monitoring and troubleshooting

- Review Amazon CloudWatch Logs for the Lambda function and SageMaker processing job logs.
- Monitor the S3 buckets for input and output files.
- Review CloudFormation stack events for any deployment issues.
- Monitor for Amazon Bedrock model API timeouts with complex PDFs. If a PDF page is too complicated, the generation time per API call for the Amazon Bedrock model may exceed the timeout limit. This can cause the process to fail for that specific file.

## Clean up

To avoid incurring unnecessary charges, remember to delete your resources when you're done:

1. Empty the S3 buckets created by the stack.
2. Delete the CloudFormation stack.
3. Delete the ECR repository if no longer needed.

## Need help?

For issues or questions, please open an issue in the project repository.
