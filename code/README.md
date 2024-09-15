# Get Started


This project sets up an event-driven Generative AI Intelligent Document Processing (IDP) application using AWS services.

## Prerequisites

Before starting the main deployment, ensure you have:

1. [AWS CLI installed](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) and configured with [appropriate permissions](https://docs.aws.amazon.com/AmazonECR/latest/userguide/image-push-iam.html).
2. [Docker installed](https://docs.docker.com/engine/install/) on your local machine.
3. A Docker image prepared with your processing code.
4. Amazon Bedrock [model access enabled](https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html).

### Pushing Docker Image to ECR

1. Create an ECR repository (if not already created):
   ```
   cd ./docker && docker build -t <your-local-image>:<tag> .
   ```

2. Create an ECR repository (if not already created):
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

5. Push the image to ECR:
   ```
   docker push <your-account-id>.dkr.ecr.<your-region>.amazonaws.com/<your-repo-name>:<tag>
   ```

6. Note down the ECR image URL for use in the CloudFormation template.

## Deployment Steps

### 1. Deploy CloudFormation Stack

1. Navigate to the AWS CloudFormation console.
2. Choose "Create stack" and upload `./cloudformation-template.yaml` template.
3. Fill in the stack details:
   - Stack name: Choose a unique name
   - Parameters:
     - BedrockModelId: Enter the desired Bedrock model ID (e.g., `anthropic.claude-3-sonnet-20240229-v1:0`)
     - ECRRepositoryUri: Paste the ECR image URL noted earlier
4. Review and create the stack.
5. Wait for the stack creation to complete.

### 2. Upload Processing Scripts

1. Locate the ScriptBucketName in the CloudFormation stack outputs.
2. Upload the scripts from `./src` to the ScriptBucketName:
   ```
   aws s3 cp ./src s3://your-script-bucket-name/scripts/ --recursive
   ```

### 3. Process PDF Files

1. Find the `InputBucketName` in the CloudFormation stack outputs.
2. Upload a PDF file to the `InputBucketName` to trigger processing:
   ```
   aws s3 cp your-file.pdf s3://your-input-bucket-name/
   ```

3. The system will automatically process the PDF and store the results in the `OutputBucketName`.

## Monitoring and Troubleshooting

- Check CloudWatch Logs for Lambda function and SageMaker processing job logs.
- Monitor the S3 buckets for input and output files.
- Review CloudFormation stack events for any deployment issues.
- Watch for Bedrock model API timeouts with complex PDFs: If a PDF page is too complicated, the generation time per API call for the Bedrock model may exceed the timeout limit. This can cause the IDP process to fail for that specific file.

## Clean Up

To avoid incurring unnecessary charges, remember to delete your resources when you're done:

1. Empty the S3 buckets created by the stack.
2. Delete the CloudFormation stack.
3. Delete the ECR repository if no longer needed.

## Need Help?

For issues or questions, please open an issue in the project repository.