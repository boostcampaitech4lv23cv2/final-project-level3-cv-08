from google.cloud import storage
import os

PWD_PATH = "/opt/ml/mmsegmentation/app/DB/"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="firm-lacing-374306-bfbd2d43b6ce.json"

bucket_name = 'rbc-bucket'    # 서비스 계정 생성한 bucket 이름 입력
storage_client = storage.Client()
bucket = storage_client.bucket(bucket_name)

def upload_image(image_path: str):
    source_file_name = PWD_PATH + image_path
    destination_blob_name = image_path
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    return blob.public_url