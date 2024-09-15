import boto3
import os

def get_files_without_extension(bucket_name, prefix=''):
    s3_client = boto3.client('s3')
    files = set()
    paginator = s3_client.get_paginator('list_objects_v2')
    
    for page in paginator.paginate(Bucket=bucket_name, Prefix=prefix):
        if 'Contents' in page:
            for obj in page['Contents']:
                file_name = os.path.splitext(os.path.basename(obj['Key']))[0]
                files.add(file_name)
    
    return files

def delete_processed_files(input_bucket, output_bucket, input_prefix='', output_prefix=''):
    s3_client = boto3.client('s3')
    
    # Get files from output bucket
    processed_files = get_files_without_extension(output_bucket, output_prefix)
    print(processed_files)
    
    # List and delete files from input bucket
    paginator = s3_client.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=input_bucket, Prefix=input_prefix):
        if 'Contents' in page:
            for obj in page['Contents']:
                file_name = os.path.splitext(os.path.basename(obj['Key']))[0]
                if file_name+'_output' in processed_files:
                    print(f"Deleting {obj['Key']} from input bucket")
                    s3_client.delete_object(Bucket=input_bucket, Key=obj['Key'])

def main():
    # Configuration
    input_bucket_name = 'your input bucket'
    output_bucket_name = 'your output bucket'
    input_prefix = ''  # Use if your files are in a specific folder
    output_prefix = ''  # Use if your output files are in a specific folder

    # Execute the cleanup process
    delete_processed_files(input_bucket_name, output_bucket_name, input_prefix, output_prefix)

if __name__ == "__main__":
    main()