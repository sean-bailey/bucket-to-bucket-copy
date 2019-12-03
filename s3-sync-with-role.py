import boto3
import os
import sys

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--rolearn", help="ARN of the role to assume (REQUIRED)")
parser.add_argument("--session", help="Session Name of the role to assume (Optional)")
parser.add_argument("--dest", help="Full name of destination bucket (REQUIRED)")
parser.add_argument("--source", help="Full name of source bucket (REQUIRED)")
args = parser.parse_args()
killcode=0
sessionname=""
if not args.rolearn:
    print("Role ARN Required to continue!")
    killcode=1
if not args.session:
    sessionname='python-s3-access'
elif args.session:
    sessionname=args.session
if not args.dest:
    print("Destination bucket required to continue!")
    killcode=1
if not args.source:
    print("Source bucket required to continue!")
    killcode=1

if not killcode == 0:
    exit()


#Step 1 get the sts credentials sorted
try:
    stsclient=boto3.client('sts')
    stsresponse=stsclient.assume_role(
    RoleArn=args.rolearn,
    RoleSessionName=sessionname
    )

    clientaccesskeyid=stsresponse['Credentials']['AccessKeyId']
    clientsecretaccesskey=stsresponse['Credentials']['SecretAccessKey']
    clientsessiontoken=stsresponse['Credentials']['SessionToken']

    #Now we need to connect to the client bucket

    nerves3=boto3.resource('s3')

    clientsession=boto3.Session(
    aws_access_key_id=clientaccesskeyid,
    aws_secret_access_key=clientsecretaccesskey,
    aws_session_token=clientsessiontoken
    )

    clients3=clientsession.resource('s3')
except Exception as e:
    print(e)

nervefiledict={}
try:
    nervebucket= nerves3.Bucket(args.dest)
    clientbucket=clients3.Bucket(args.source)

except Exception as e:
    print(e)

for nerve_object in nervebucket.objects.all():
    nervefiledict[str(nerve_object.key)]=1

for client_object in clientbucket.objects.all():
    try:
        if not str(client_object.key) in nervefiledict.keys():
            print("downloading " + str(client_object.key))
            clientbucket.download_file(str(client_object.key), str(client_object.key))
            print("Uploading " + str(client_object.key))
            nervebucket.upload_file(str(client_object.key),str(client_object.key))
            print("Deleting " + str(client_object.key))
            os.remove(str(client_object.key))
        else:
            nerveresource=boto3.resource('s3')
            nerveobject=nerveresource.Object(args.dest,client_object.key)
            if client_object.last_modified > nerveobject.last_modified:
                print("downloading " + str(client_object.key))
                clientbucket.download_file(str(client_object.key), str(client_object.key))
                print("Uploading " + str(client_object.key))
                nervebucket.upload_file(str(client_object.key),str(client_object.key))
                print("Deleting " + str(client_object.key))
                os.remove(str(client_object.key))
                print("File updated!")

    except Exception as e:
        print("Cannot perform action on " + str(client_object.key))
        print(e)
