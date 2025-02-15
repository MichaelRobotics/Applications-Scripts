source "amazon-ebs" "jenkins" {
  ami_name          = var.ami_name
  instance_type     = var.instance_type
  region            = var.region
  source_ami        = var.source_ami
  ssh_username      = var.ssh_username
  security_group_id = var.security_group_id



  tags = {
    "Name" = "Jenkins-Ansible"
  }
}

build {

  sources = ["source.amazon-ebs.jenkins"]

  provisioner "ansible" {

    playbook_file = "../playbook/jenkins-playbook.yaml"

  }

  provisioner "file" {
    source = "../scripts/jenkins-start.sh"

    destination = "/tmp/jenkins-start.sh"

  }

  provisioner "shell" {

    inline = [
      "sudo chmod +x /tmp/jenkins-start.sh",
      "sudo mv /tmp/jenkins-start.sh   /var/lib/cloud/scripts/per-instance/",
    ]

  }

  post-processor "manifest" {}

}