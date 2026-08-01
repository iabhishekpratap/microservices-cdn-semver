import os
import uuid
import boto3
from botocore.exceptions import NoCredentialsError


def get_s3_client():
    """
    Create and return an S3 client.
    """
    return boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "ap-south-1"),
    )


def upload_video_to_s3(file_obj, original_filename):
    """
    Upload a video file to S3 and return its CloudFront URL.

    Environment Variables Required:
        AWS_ACCESS_KEY_ID
        AWS_SECRET_ACCESS_KEY
        AWS_REGION
        AWS_STORAGE_BUCKET_NAME
        CLOUDFRONT_URL
    """

    s3 = get_s3_client()

    bucket_name = os.getenv("AWS_STORAGE_BUCKET_NAME")
    cloudfront_url = os.getenv("CLOUDFRONT_URL")

    if not bucket_name:
        print("AWS_STORAGE_BUCKET_NAME is not configured.")
        return None

    if not cloudfront_url:
        print("CLOUDFRONT_URL is not configured.")
        return None

    # Generate a unique filename
    extension = original_filename.split(".")[-1]
    object_key = f"videos/{uuid.uuid4().hex}.{extension}"

    try:
        s3.upload_fileobj(
            Fileobj=file_obj,
            Bucket=bucket_name,
            Key=object_key,
            ExtraArgs={
                "ContentType": file_obj.content_type
            },
        )

        # Return the CloudFront URL instead of the S3 URL
        return f"{cloudfront_url.rstrip('/')}/{object_key}"

    except NoCredentialsError:
        print("AWS credentials not available.")
        return None

    except Exception as e:
        print(f"Error uploading video to S3: {e}")
        return None