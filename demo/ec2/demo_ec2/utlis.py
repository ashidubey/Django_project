import logging
import boto3
import os
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)
ec2 = boto3.resource('ec2',aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),  aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY'),region_name="ap-south-1")


# 
# group_name=input("Enter Security_group_name:")
# group_description=input("Enter group description:")
# 
# image_id=input("Enter image-id:")
# instance_type=input("Enter instance type:")
# key_name=input("Enter KeyName:")



def setup_security_group(group_name, group_description, ssh_ingress_ip=None):
    try:
        default_vpc = list(ec2.vpcs.filter(
            Filters=[{'Name': 'isDefault', 'Values': ['true']}]))[0]
        logger.info("Got default VPC %s.", default_vpc.id)
    except ClientError:
        logger.exception("Couldn't get VPCs.")
        raise
    except IndexError:
        logger.exception("No default VPC in the list.")
        raise

    try:
        security_group = default_vpc.create_security_group(
            GroupName=group_name, Description=group_description)
        logger.info(
            "Created security group %s in VPC %s.", group_name, default_vpc.id)
    except ClientError:
        logger.exception("Couldn't create security group %s.", group_name)
        raise

    try:
        ip_permissions = [{
            # HTTP ingress open to anyone
            'IpProtocol': 'tcp', 'FromPort': 80, 'ToPort': 80,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
        }, {
            # HTTPS ingress open to anyone
            'IpProtocol': 'tcp', 'FromPort': 443, 'ToPort': 443,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
        }]
        if ssh_ingress_ip is not None:
            ip_permissions.append({
                # SSH ingress open to only the specified IP address
                'IpProtocol': 'tcp', 'FromPort': 22, 'ToPort': 22,
                'IpRanges': [{'CidrIp': f'{ssh_ingress_ip}/32'}]})
        security_group.authorize_ingress(IpPermissions=ip_permissions)
        logger.info("Set inbound rules for %s to allow all inbound HTTP and HTTPS "
                    "but only %s for SSH.", security_group.id, ssh_ingress_ip)
    except ClientError:
        logger.exception("Couldnt authorize inbound rules for %s.", group_name)
        raise
    else:
        return security_group


def create_instance(
        image_id, instance_type, key_name, security_group_names=None):
    try:
        instance_params = {
            'ImageId': image_id, 'InstanceType': instance_type, 'KeyName': key_name
        }
        if security_group_names is not None:
            instance_params['SecurityGroups'] = security_group_names
        instance = ec2.create_instances(**instance_params, MinCount=1, MaxCount=1,IamInstanceProfile={
        'Arn': 'arn:aws:iam::841911212238:instance-profile/demo',
       
        })[0]
        logger.info("Created instance %s.", instance.id)
    except ClientError:
        logging.exception(
            "Couldn't create instance with image %s, instance type %s, and key %s.",
            image_id, instance_type, key_name)
        raise
    else:
        return instance

        group_name

# setup_security_group(group_name,group_description)
# create_instance(image_id,instance_type,key_name,[group_name])

