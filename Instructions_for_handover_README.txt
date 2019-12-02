There are current technical difficulties on AWS's backend which is preventing a
direct s3-s3 transfer that AWS Support and Sean Bailey are currently working a
solution to. In the meantime, Sean has whipped up a python script to be run on
the instance which can perform the file synchronization process.

To access the instance, use the following command:

ssh -i mck-590-s3-transfer-root-keypair.pem ubuntu@ec2-3-209-78-57.compute-1.amazonaws.com

if you cannot connect to the instance, make sure you are on the QB or McK VPN. If
neither of those allow you to connect, please reach out to the cloud team to add that IP
to our whitelist, as they could have rotated from our list of known IPs. Note that we can
Only whitelist IPs from the QB or McK VPNs. You can get your IP by connecting to the VPN
and Googling "what is my IP"

Once connected. perform the following command:

cd ~/copydata && ./runme.sh

You may then close your terminal, as the instance will then begin copying data
in the background between buckets. A log of the finished copy will be visible
at ~/copydata/nohup.out.

Once the S3 to S3 direct transfer with the role juggling is working again from AWS,
this script can be replaced with a direct fix. In the meantime, it is a secure method to
transfer data between the two buckets. (Encrypted in transit, at rest, and limited by
security groups and source IPs to the role allowed to access the client bucket).

Please let Sean Bailey know if there are any questions regarding this process.


UPDATE 16:01 PM NOV 22 2019:

The Python script has been updated to sync between the two buckets by checking
what is currently in the client bucket and then seeing if it's in the nerve bucket
already. If not, the file gets copied over. There is a cronjob on the EC2 machine
now running which checks every 5 minutes for changes to the client bucket.

It does not matter if there are different files in the Nerve bucket than the client bucket,
they will not be deleted, but at the minimum the same files from the client bucket will
be in the nerve bucket.
