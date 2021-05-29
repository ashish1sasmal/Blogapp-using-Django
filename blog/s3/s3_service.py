# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import boto3
from botocore.client import Config
import os
import io
ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
SECRET_KEY = os.environ.get('AWS_SECRET_KEY')

s3 = boto3.resource('s3',aws_access_key_id= ACCESS_KEY,aws_secret_access_key= SECRET_KEY, config = Config(signature_version = 's3v4', region_name = 'ap-south-1'))
s3client = boto3.client('s3',aws_access_key_id=ACCESS_KEY,aws_secret_access_key= SECRET_KEY, config = Config(signature_version = 's3v4', region_name = 'ap-south-1'))



def upload_file(source_path, dest_path=None, bucket_name='secretblogs'):
    print("inside upload_file")
    print(bucket_name)
    print((source_path,dest_path))
    if dest_path is None:
        dest_path = source_path.split("/")[1]
    try:
        result = s3.Bucket(bucket_name).upload_file(source_path,'%s' %(dest_path))
        print(('result ', result))
        print('upload_file success')
        return 1
    except Exception as e:
        print(("exception:",e))
    return 0

# get all Files
def get_all_files_p(parent_folder,folder_name, bucket_name='secretblogs'):

    #s3=boto3.client('s3',aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
    list1=s3client.list_objects(Bucket=bucket_name)['Contents']
    all_files=[]
    foldername =folder_name
    for element in list1:
        if element['Key'].startswith(parent_folder) and not element['Key'].endswith('/'):
            if folder_name in element['Key']:
                all_files.append(element['Key'])

    return all_files

def upload_file_obj(file, dest_path="", bucket_name='secretblogs'):
    print("inside upload_file_obj")
    try:
        print(f"Dest Path {dest_path}")
        result = s3.Bucket(bucket_name).put_object(Key=dest_path, Body=file,ACL='public-read')
        print(('result ', result))
        print('upload_file success')
        return 1
    except Exception as e:
        print(("exception:",e))
    return 0

def move_file(from_path,dest_path, bucket_name='secretblogs'):
    print("Inside Move/Rename file")
    try:
        copy_source = {
            'Bucket': bucket_name,
            'Key': from_path
        }
        r = s3.meta.client.copy(copy_source, 'secretblogs', dest_path,ExtraArgs={"ACL":'public-read'})
        delete_file(from_path)
        print("Result",r)
        return 1
    except Exception as e:
        print(("exception:",e))
    return 0

def copy_file(from_path,dest_path, bucket_name='secretblogs'):
    print("Inside Copy file")
    try:
        copy_source = {
            'Bucket': bucket_name,
            'Key': from_path
        }
        r = s3.meta.client.copy(copy_source, 'secretblogs', dest_path,ExtraArgs={"ACL":'public-read'})
        print("Result",r)
        return 1
    except Exception as e:
        print(("exception:",e))
    return 0

def delete_file(file_path, bucket_name='secretblogs'):
    print("Inside Delete file")
    try:
        bucket = s3.Bucket(bucket_name)
        filename = file_path.split('/')[-1]
        folder_name_split = file_path.split('/')[:-1]
        folder_name = '/'.join(folder_name_split)
        print(filename,folder_name)
        for obj in bucket.objects.filter(Prefix=folder_name):
            if obj.key == file_path:
                s3.Object(bucket.name,obj.key).delete()
                return 1
    except Exception as e:
        print(("exception:",e))
    return 0


def download_file(file_path, bucket_name = 'secretblogs'):
    try:
        obj = s3.Object(bucket_name, file_path)
        data = io.BytesIO()
        obj.download_fileobj(data)
        return data
    except Exception as e:
        print('Exception:', e)
        return e



def create_temp_url(file_path, expiry_in = 3600, bucket_name = 'secretblogs'):
    return s3client.generate_presigned_url('get_object', Params = {
        "Bucket":bucket_name,
        "Key":file_path
    },ExpiresIn = expiry_in)
