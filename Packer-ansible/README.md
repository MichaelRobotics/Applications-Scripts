# Jenkins AMI Builder with Packer and Ansible

## Project Overview

This project automates the creation of a custom Amazon Machine Image (AMI) with Jenkins pre-installed using HashiCorp Packer and Ansible. The resulting AMI can be used to quickly deploy Jenkins instances in AWS, ensuring consistency and reducing manual configuration.

## Technology Stack

- **HashiCorp Packer**: Infrastructure as Code tool for creating identical machine images
- **Ansible**: Configuration management for automated software installation
- **AWS EC2**: Cloud computing environment
- **Jenkins**: Continuous Integration and Delivery server
- **Shell Scripting**: For post-installation automation

## Project Structure

```
Packer-ansible/
├── packer/
│   ├── jenkins.pkr.hcl       # Main Packer configuration for Jenkins AMI
│   ├── packer.pkr.hcl        # Packer plugin requirements
│   ├── variables.pkr.hcl     # Configuration variables
│   └── packer-manifest.json  # Build output manifest
├── playbook/
│   └── jenkins-playbook.yaml # Ansible playbook for Jenkins installation
└── scripts/
    └── jenkins-start.sh      # Startup script for Jenkins service
```

## Features

- **Infrastructure as Code**: Complete automation of infrastructure creation using declarative configuration
- **Immutable Infrastructure**: Builds standardized, versioned machine images
- **Automation**: Zero-touch installation of Jenkins and its dependencies
- **Reusability**: Parameterized configuration for flexibility across environments
- **Instance Bootstrapping**: Automatic service startup on instance launch

## Implementation Details

### Packer Configuration

The `jenkins.pkr.hcl` file defines an Amazon EBS builder with specific settings for AMI creation:
- Uses Amazon Linux as the base image
- Configures appropriate instance type and region
- Applies custom tagging for resource management
- Incorporates multiple provisioners for complete setup

### Ansible Integration

Packer integrates with Ansible to perform the following tasks:
- Configure Jenkins repository and GPG key
- Install OpenJDK 11 as a dependency
- Install and configure Jenkins server

### Instance Startup Automation

The project includes a shell script that is installed as part of the instance's user data to:
- Enable Jenkins as a system service
- Start Jenkins automatically on instance boot

### Customization

The `variables.pkr.hcl` file allows for customization of:
- Base AMI selection
- Instance type
- AWS region
- Security group configuration
- Default username

## Build Results

A successful build produces:
- Custom AMI (ID: ami-0b52c2f7e79b4a654) in the eu-central-1 region
- Packer manifest with build metadata
- Ready-to-deploy image with Jenkins pre-installed

## DevOps Skills Demonstrated

- **Automation**: Eliminates manual installation and configuration steps
- **Configuration Management**: Uses industry-standard tools for reproducible environments
- **Infrastructure as Code**: Maintains infrastructure definitions in version control
- **Cloud Architecture**: Leverages AWS services for scalable deployments
- **CI/CD Knowledge**: Demonstrates understanding of CI/CD tooling setup

## Benefits

- **Consistency**: Ensures identical environments across deployments
- **Efficiency**: Reduces deployment time from hours to minutes
- **Scalability**: Enables rapid scaling of Jenkins instances
- **Maintainability**: Simplifies updates and changes through code
- **Disaster Recovery**: Facilitates quick recovery in case of failures
