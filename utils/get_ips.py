import boto3


def get_ips():
    autoscaling_client = boto3.client(
            "autoscaling",
            region_name="eu-central-1")

    ec2_client = boto3.client(
            "ec2",
            region_name="eu-central-1")

    autoscaling_group_name = "hs.asg.coffee"
    response = autoscaling_client.describe_auto_scaling_groups(
            AutoScalingGroupNames=[autoscaling_group_name]
            )

    ip_list = []
    for instance in response["AutoScalingGroups"][0]["Instances"]:
        instance_id = instance["InstanceId"]

        instance_info = ec2_client.describe_instances(
                InstanceIds=[instance_id])

        instance_ = instance_info["Reservations"][0]["Instances"][0]
        public_ip = instance_["PublicIpAddress"]

        ip_list.append(public_ip)

    return ip_list, 8080
