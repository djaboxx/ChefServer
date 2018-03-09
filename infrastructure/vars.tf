variable "ami" {
	default = "ami-aa2ea6d0"
}

variable "instance_type" {
	default = "m4.large"
}

variable "key_name" {}
variable "server_name" {}

variable "domain" {}

variable "region" {}

variable "subnet_cidr" {}

variable "vpc_cidr" {}

variable "route53_zone_id" {}