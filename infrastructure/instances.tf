
resource "aws_instance" "chef_server" {
    ami = "${var.ami}"
    instance_type = "${var.instance_type}"
    key_name = "${var.key_name}"
    subnet_id = "${aws_subnet.chef_server_subnet.id}"
    vpc_security_group_ids = ["${aws_security_group.web_traffic.id}"]
    associate_public_ip_address = true
    tags {
        Name = "chef${format("%02d", count.index+1)}"
        role = "chef"
        hostname = "${var.server_name}.${var.domain}"
    }
    provisioner "remote-exec" {
      inline = [
        "sudo apt-get update",
        "sudo apt-get install -y python python-dev python-pip" 
      ]
      connection {
        type     = "ssh"
        user     = "ubuntu"
      }
    }
}

resource "aws_route53_record" "chef_server" {
  zone_id = "${var.route53_zone_id}"
  name    = "${var.server_name}.${var.domain}"
  type    = "A"
  ttl     = "300"
  records = ["${aws_instance.chef_server.public_ip}"]
}