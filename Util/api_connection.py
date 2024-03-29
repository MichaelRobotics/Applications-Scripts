from Util.robot_data import RobotData
import requests
import json
from Util.utils import BearerAuth
from os import getenv
from urllib3.exceptions import InsecureRequestWarning
from Logs.logger_config import logger

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# Fleet Address
FLEET_PORT = ":443"
FLEET_IP = "192.168.1.78"
# Robot ID's
ROBOT_ONE_ID = "robotone"
ROBOT_TWO_ID = "robottwo"
ROBOT_THREE_ID = "robotthree"
# Robot IP's
ROBOT_ONE_IP = "robotone"
ROBOT_TWO_IP = "robotone"
ROBOT_THREE_IP = "robotone"
# Robot Usernames
ROBOT_ONE_USERNAME = "vbmichal2"
ROBOT_TWO_USERNAME = "dev"
ROBOT_THREE_USERNAME = "vb"
# Robot Passwords
ROBOT_ONE_PASSWORD = ""
ROBOT_TWO_PASSWORD = ""
ROBOT_THREE_PASSWORD = ""
# JWT API Key
JWT_API_KEY = ''

class ApiConnection:

    @classmethod
    def _connect_to_all_active_robots(cls, ip_values, id_values, username_values, password_values):

        objects_list = []
        logger.debug(f"{ip_values}\n{id_values}\n{username_values}\n{password_values}")

        # Create objects that communicate to PC's with robots onboard
        for ip_val, id_val, username_values, password_values in zip(ip_values, id_values, username_values, password_values):
            try:
                robot_obj = RobotData(ip_val, id_val, 22, username_values, password_values)
                objects_list.append(robot_obj)
                logger.info(objects_list)
            except Exception as e:
                logger.info(f"An error occurred when creating RobotData object for robot '{ip_val}': {e}")

        # logging PC's identification
        for obj in objects_list:
            logger.info(f"ip_val: {obj.hostname}, user: {obj.username}")
        return objects_list
    
    @classmethod
    def _connect_to_fleet(cls):
        try:
            auth_bearer = BearerAuth(getenv('JWT_API_KEY',
                                         JWT_API_KEY))
            response = requests.get(
                f'https://{FLEET_IP}{FLEET_PORT}/api/v1/fleet/robot-info',
                auth=auth_bearer, verify=False, timeout=50)
            response.raise_for_status()  # Raise an exception if the HTTP response status code is not in the 200-299 range
            return response
        except requests.exceptions.RequestException as e:
            # Handle network-related exceptions (e.g., connection errors, timeouts)
            logger.info(f"RequestException: {e}")
            return  None
        
    @classmethod
    def _get_data_about_active_robots_from_fleet(cls, response: requests.Response):
        try:
        ##############COMMENTED FOR NOT WORKING FLEET API###############
        #    workers = response.json()  # Parse the JSON response
        #    ip_values = [item['robotSpec']['ip'] for item in workers]
        #    id_values = [item['robotSpec']['id'] for item in workers]
        #    online_values = [item['online'] for item in workers]
        #    merged_ip_online = {ip: online for ip, online in zip(ip_values, online_values)}
        #    merged_id_online = {id: online for id, online in zip(id_values, online_values)}
        #    active_robot_ip_list = [key for key, val in merged_ip_online.items() if val == True]
        #    active_robot_id_list = [key for key, val in merged_id_online.items() if val == True]
        #    print(active_robot_ip_list)
        #    print(active_robot_id_list)
        ########################################################
            active_pc_username_list = ["vbmichal2", "dev", "laptopdev"]
            active_robot_ip_list = ["192.168.1.78", "192.168.1.73", "192.168.1.21"]
            active_robot_id_list = ["robotone", "robottwo", "robotthree"]
            actual_password_list = ["vbrobot123", "vbrobot123", "vbrobot123"]
            return active_robot_ip_list, active_robot_id_list, active_pc_username_list, actual_password_list
        except json.JSONDecodeError as e:
            # Handle JSON parsing errors
            logger.info(f"JSONDecodeError: {e}")
            return  None

    @classmethod
    def get_robot_objects(cls):
        try:
            # Get Ip from active robots on fleet
            response = cls._connect_to_fleet()
            ip_values, id_values, active_pc_username_list, actual_password_list = cls._get_data_about_active_robots_from_fleet(response)
            robot_list = cls._connect_to_all_active_robots(ip_values, id_values, active_pc_username_list, actual_password_list)
            logger.info(robot_list)
            return robot_list
        except Exception as e:
            logger.info(f"An error occurred when executing main script: {e}")
            return None