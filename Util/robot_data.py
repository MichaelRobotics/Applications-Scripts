import Util.utils as utils
from Logs.logger_config import logger


class RobotData:
    """
        Class for communication with robot
    """
    def __init__(self, hostname: str, id: str, port: int, username: str, password: str):
        """
            Log data and communication vars
        """
        self.hostname = hostname
        self._id = id
        self.port = port
        self.username = username
        self.password = password

    
    @property
    def id(self):
        return self._id
        
    def _download_log_file_from_robot(self, path_to_save_localy, log_path_on_robot, ssh):
        try:
            sftp = utils.SFTPclient(ssh).sftp
            sftp.get(log_path_on_robot, path_to_save_localy)
            logger.info(f"File '{path_to_save_localy}' downloaded from '{log_path_on_robot}'")
        except FileNotFoundError:
            logger.info(f"Remote file not found")
        except Exception as e:
            logger.info("An error occurred while downloading the file:", str(e))
        finally:
            # Close the SFTP session and the SSH connection
            sftp.close()
        return path_to_save_localy
        
            
    def get_container_log_data(self, path_to_save_localy, log_path_on_robot):
        try:
            ssh = utils.SSHinvoker(self.hostname, self.port, self.username, self.password).ssh
            path_to_save_localy = self._download_log_file_from_robot(path_to_save_localy, log_path_on_robot, ssh)
            return path_to_save_localy       
        finally:
            # Close the SSH connection
            ssh.close()
            