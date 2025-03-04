# Applications & Scripts Portfolio

## Overview

This repository showcases a collection of professional-grade applications and scripts demonstrating expertise in distributed systems, infrastructure automation, data processing, and monitoring solutions. Each project addresses specific technical challenges with robust implementation and best practices.

## What You'll Find in This Repository

### 1. Robot Fleet Management System (Client-Server-API)

A comprehensive distributed system for real-time monitoring and control of robot fleets featuring:

- **Three-tier Architecture**: Client (robot), Server (hub), and RESTful API
- **Robust Communication**: TCP/IP socket programming with heartbeat monitoring
- **Multi-threading**: Concurrent client handling with thread safety
- **Data Persistence**: SQLAlchemy ORM with SQLite backend
- **REST API Integration**: Flask-RESTx with automatic Swagger documentation

### 2. Jenkins AMI Builder (Packer-ansible)

Infrastructure as Code solution for automated Jenkins server deployment using:

- **HashiCorp Packer**: Machine image creation across cloud platforms
- **Ansible Automation**: Configuration management for Jenkins installation
- **AWS Integration**: EC2 image creation optimized for production deployments
- **Immutable Infrastructure**: Standardized, version-controlled machine images
- **Infrastructure as Code**: Declarative configuration for reproducible environments

### 3. Statistics from Logs Exporter

Data processing pipeline for extracting valuable metrics from robot operation logs:

- **Log Processing**: Sophisticated parsing of complex log formats
- **Statistical Analysis**: Extraction of success rates and error patterns
- **Pandas Integration**: Powerful data manipulation and transformation
- **Visualization Preparation**: Output formatting for dashboard integration
- **Containerization**: Dockerized for deployment flexibility

## Technologies Demonstrated

- **Languages**: Python, YAML, HCL
- **Frameworks**: Flask, Flask-RESTx
- **Infrastructure Tools**: Packer, Ansible, AWS
- **Data Processing**: Pandas, NumPy
- **Networking**: Socket Programming, TCP/IP
- **Containerization**: Docker
- **Database**: SQLAlchemy, SQLite
- **Documentation**: Swagger UI

## Project Organization

```
Repository/
├── Client-Server-Api/              # Robot fleet management system
│   ├── Api/                        # RESTful API component
│   ├── Client.py                   # Robot client implementation
│   ├── Server.py                   # Communication hub
│   └── Logs/                       # Logging configuration
│
├── Packer-ansible/                 # Jenkins AMI builder
│   ├── packer/                     # Packer configuration files
│   ├── playbook/                   # Ansible playbooks
│   └── scripts/                    # Instance bootstrap scripts
│
└── statistics-from-logs-exporter/  # Log processing system
    ├── Filters/                    # Log parsing components
    ├── Logs/                       # Sample and output logs
    ├── Util/                       # Utility functions
    └── Dockerfile                  # Container definition
```

## Key Technical Skills Demonstrated

- Distributed Systems Design
- Network Programming & Concurrent Processing
- Infrastructure as Code & Configuration Management
- Cloud Integration & Automation
- Data Processing & Statistical Analysis
- Containerization & Deployment
- Error Handling & Logging
- API Design & Documentation

These projects represent practical solutions to real-world engineering challenges, demonstrating both technical depth and breadth across multiple domains of software and infrastructure engineering.
