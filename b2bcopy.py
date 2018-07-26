#!/usr/bin/python3

import boto3
import os
import re
import sys

s3client = boto3.client("s3")


def get_files_in_bucket_folder(sourcebucket, folderprefix):
    filenamearray = []
    try:
        print("listing contents of bucket %s in folder %s" % (sourcebucket,
                                                              folderprefix))
        objectsinbucket = s3client.list_objects_v2(
            Bucket=sourcebucket,
            Delimiter=',',
            Prefix=folderprefix
        )
        if 'Contents' in objectsinbucket.keys():
            for object in objectsinbucket['Contents']:
                filenamearray.append[str(object['Key'])]
        else:
            print("No objects in folder %s!" % folderprefix)
            filenamearray = None
        return filenamearray
    except Exception as e:
        print(" error message for getting files in folder is %s" % str(e))
        return None


def download_file_to_memory(sourcebucket, folderprefix, file):
    try:
        print("putting file %s%s into memory for transfer..." % (folderprefix,
                                                                 file))
        fullfilename = folderprefix + "/"+file
        filetomemory = s3client.get_object(Bucket=sourcebucket,
                                           Key=fullfilename)['Body'].read()
        return filetomemory
    except Exception as e:
        print("error message for getting file to memory is %s" % str(e))
        return None


def upload_file_to_dest_bucket(destbucket, folderprefix, fileobject, filename):
    try:
        fullfilename = folderprefix+'/'+filename
        print("uploading %s to dest bucket %s" % s(fullfilename, destbucket))
        response = s3client.put_object(
            body=fileobject,
            Bucket=destbucket,
            Key=fullfilename
        )
        return response
    except Exception as e:
        print(" Error for file upload is %s" % str(e))
        return None


def main():
    sourcebucket = sys.argv[1]
    destbucket = sys.argv[2]
    folderprefix = sys.argv[3]
    list_of_files = get_files_in_bucket_folder(sourcebucket, folderprefix)
    if list_of_files is not None:
        for filename in list_of_files:
            downloadedfile = download_file_to_memory(sourcebucket,
                                                     folderprefix, filename)
            if downloadedfile is not None:
                success = upload_file_to_dest_bucket(destbucket,
                                                     folderprefix,
                                                     downloadedfile,
                                                     filename)
                if success is not None:
                    print("%s transferred successfully to destination "
                          % filename)
            else:
                print("File %s didn't load in to memory. Debugging needed")
                break()
    else:
        print("List_of_files was empty, debugging needed.")


if __name__ == "__main__":
    main()
