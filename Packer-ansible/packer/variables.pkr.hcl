variable "ami_name" {
  default = "Jenkins-AMI"
}

variable "source_ami" {
  default = "ami-007c3072df8eb6584"
}

variable "instance_type" {
  default = "t3.medium"
}

variable "region" {
  default = "eu-central-1"
}

variable "ssh_username" {
  default = "ec2-user"
}

variable "security_group_id" {
  default = "sg-02ca1d641251e8c93"
}
