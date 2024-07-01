# Comprehensive Network Security Management System

This repository contains the code for a comprehensive network security management system leveraging various AWS services. It includes real-time monitoring, threat detection, incident response, and compliance management.

## Features

- Real-Time Monitoring (Amazon Kinesis, AWS Lambda)
- Anomaly Detection (Machine Learning Models)
- Threat Intelligence (AWS Lambda)
- Incident Response (AWS Lambda, AWS SNS)
- Compliance Management (AWS Config, AWS Lambda)
- Logging and Monitoring (AWS CloudTrail, Amazon S3)
- Infrastructure as Code (Serverless Framework, Python)

## Getting Started

### Prerequisites

- Python 3.8+
- AWS CLI
- Serverless Framework
- Docker
- Docker Compose

### Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/network-security-management.git
    cd network-security-management
    ```

2. Install dependencies:
    ```bash
    pip install -r infrastructure/requirements.txt
    ```

3. Deploy the infrastructure:
    ```bash
    serverless deploy
    ```

4. Set up AWS resources:
    ```bash
    python backend/infrastructure/setup_infrastructure.py
    ```

5. Train and evaluate models:
    ```bash
    python models/train_anomaly_model.py
    python models/evaluate_anomaly_model.py
    ```

6. Run the system:
    ```bash
    python backend/threat_detection/real_time_monitoring.py
    ```

## License

This project is licensed under the MIT License.
