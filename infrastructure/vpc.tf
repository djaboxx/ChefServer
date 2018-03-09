resource "aws_vpc" "chef_server_vpc" {
  cidr_block       = "${var.vpc_cidr}"
  tags {
    Name = "ChefServer"
  }
}

resource "aws_subnet" "chef_server_subnet" {
  vpc_id     = "${aws_vpc.chef_server_vpc.id}"
  cidr_block = "${var.subnet_cidr}"
  map_public_ip_on_launch = true
  tags {
    Name = "ChefServer"
  }
}

resource "aws_internet_gateway" "default" {
    vpc_id = "${aws_vpc.chef_server_vpc.id}"
}

resource "aws_route_table" "default" {
    vpc_id = "${aws_vpc.chef_server_vpc.id}"

    route {
        cidr_block = "0.0.0.0/0"
        gateway_id = "${aws_internet_gateway.default.id}"
    }

    tags {
        Name = "ChefServerSubnet"
    }
}

resource "aws_route_table_association" "default" {
    subnet_id = "${aws_subnet.chef_server_subnet.id}"
    route_table_id = "${aws_route_table.default.id}"
}
