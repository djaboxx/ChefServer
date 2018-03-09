resource "aws_key_pair" "chef_server" {
  key_name   = "${var.key_name}"
  public_key = "${file("~/.ssh/${var.key_name}.pub")}"
}