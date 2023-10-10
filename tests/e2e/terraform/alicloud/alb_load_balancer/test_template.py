import os

from tests.e2e.terraform.alicloud.testing import _test_template

root = os.path.dirname(os.path.abspath(__file__))
tf_plan_path = os.path.join(root, "main.tfplan")

tpl = {
    "ROSTemplateFormatVersion": "2015-09-01",
    "Resources": {
        "alicloud_alb_load_balancer.default": {
            "Type": "ALIYUN::ALB::LoadBalancer",
            "Properties": {
                "AddressAllocatedMode": "Fixed",
                "AddressType": "Internet",
                "LoadBalancerEdition": "Basic",
                "LoadBalancerName": "tf_example",
                "ResourceGroupId": "rg-acfm2xwmxvrzq6q",
                "Tags": [{"Key": "Created", "Value": "TF"}],
                "VpcId": {"Fn::GetAtt": ["alicloud_vpc.default", "VpcId"]},
                "LoadBalancerBillingConfig": {"PayType": "PayAsYouGo"},
                "ZoneMappings": [
                    {
                        "VSwitchId": {
                            "Fn::GetAtt": ["alicloud_vswitch.default1", "VSwitchId"]
                        },
                        "ZoneId": "cn-beijing-g",
                    },
                    {
                        "VSwitchId": {
                            "Fn::GetAtt": ["alicloud_vswitch.default2", "VSwitchId"]
                        },
                        "ZoneId": "cn-beijing-h",
                    },
                ],
                "ModificationProtectionConfig": {"Status": "NonProtection"},
            },
        },
        "alicloud_vpc.default": {
            "Type": "ALIYUN::ECS::VPC",
            "Properties": {"CidrBlock": "10.4.0.0/16", "VpcName": "tf_example"},
        },
        "alicloud_vswitch.default1": {
            "Type": "ALIYUN::ECS::VSwitch",
            "Properties": {
                "CidrBlock": "10.4.1.0/24",
                "VpcId": {"Fn::GetAtt": ["alicloud_vpc.default", "VpcId"]},
                "VSwitchName": "tf_example_1",
                "ZoneId": "cn-beijing-g",
            },
        },
        "alicloud_vswitch.default2": {
            "Type": "ALIYUN::ECS::VSwitch",
            "Properties": {
                "CidrBlock": "10.4.2.0/24",
                "VpcId": {"Fn::GetAtt": ["alicloud_vpc.default", "VpcId"]},
                "VSwitchName": "tf_example_2",
                "ZoneId": "cn-beijing-h",
            },
        },
    },
}


def test_template():
    t = _test_template(root, tf_plan_path)
    assert t == tpl
