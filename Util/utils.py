import requests
import paramiko
from Logs.logger_config import logger

class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = f"Bearer {self.token}"
        return r
    
class SSHinvoker():
    def __init__(self, hostname, port, username, password):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            logger.info("connecting...")
            self.ssh.connect(hostname=self.hostname, port=self.port, username=self.username, password=self.password, timeout=180)
            logger.info("connected")
        except Exception as exc:
            logger.info(exc)

class SFTPclient():
    def __init__(self, ssh):
        try:
            self.sftp = ssh.open_sftp()
        except Exception as sftp_error:
            logger.info(f'Error creating SFTP client: {str(sftp_error)}')

