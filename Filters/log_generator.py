import pandas as pd
from Filters.log_comparer import Comparer
import os
from Logs.logger_config import logger

VB_MANAGER_FILTERED_LOG_PATH = "/tmp/fleetlogbuffile.txt"

#DEFINED FOR NOT WORKING API
#ROBOT_ONE_ID = "robotone"
ROBOT_ONE_PATH = "/home/vbmichal2/log/latest/robot.log"
#ROBOT_TWO_ID = "robottwo"
ROBOT_TWO_PATH = "/home/dev/log/latest/robot.log"
#ROBOT_THREE_ID = "robotthree"
ROBOT_THREE_PATH = "/home/laptopdev/log/latest/robot.log"

VB_MANAGER_TEXT_TO_FIND = [["vb_manager.am - info - PFT", "Action completed."], 
                      ["vb_manager.mm - info - PFT", "ActionPoint", "started"],
                      ["vb_manager.am", "Action", "waiting", "help"],
                      ["vb_manager.am", "Action", "aborted"],
                      ["vb_manager.action", "Position correct"],
                      ["vb_manager.action", "error", "Position incorrect because position sensor (tr) is not active"],
                      ["vb_manager.action", "Departing failed"]
                      ]


class LogGenerator:

    """
        IPUT: robotlist
        OUTPUT: all_robots_ap_data 
    """

    @classmethod
    def _log_filter(cls, input_file_path: str):
        # Texts to search for in the file
        # Open the input file, read lines containing the specified texts and save to output file
        try:
            logger.info(f"Input file path: {input_file_path}")
            logger.info(f"Output file path: {VB_MANAGER_FILTERED_LOG_PATH}")
            with open(input_file_path, 'r') as input_file:
                input_file_lines = input_file.readlines()
            with open(VB_MANAGER_FILTERED_LOG_PATH, 'w') as output_file:
                for line in input_file_lines:
                    # Output is there to just explain functionality of the filter function.
                    output_file = cls._filter_lines_for_keywords(VB_MANAGER_TEXT_TO_FIND, line, output_file)
            return VB_MANAGER_FILTERED_LOG_PATH
    
        except FileNotFoundError:
            logger.info("File not found. Please provide valid file paths.")
            return None
        except FileExistsError:
            logger.info("The output file already exists. Please provide a different output file path.")
            return None
        
    @staticmethod
    def _filter_lines_for_keywords(text_to_find, line, output_file):
        try:
            for keywords in text_to_find:
                if all(keyword in line for keyword in keywords):
                    logger.info(line)
                    output_file.write(line)
                    output_file.seek(0, os.SEEK_END)  # Go to the end of the file
                    if output_file.tell() == 0:  # If the current position is 0, the file is empty
                        raise ValueError("Output file is empty after write operation")
            return output_file    
        except FileNotFoundError:
            logger.info("File not found. Please provide valid file paths.")
            return None

    @classmethod
    def _set_paths_to_logs_on_robots(cls, robot_id):
        if robot_id == "robotone":
            path_on_robot_vbmanager = ROBOT_ONE_PATH
        elif robot_id == "robottwo":
            path_on_robot_vbmanager = ROBOT_TWO_PATH
        elif robot_id == "robotthree":
            path_on_robot_vbmanager = ROBOT_THREE_PATH
        else:
            pass
        return path_on_robot_vbmanager
    
    @classmethod
    def generate_log_output(cls, robotlist: list):
        all_robots_ap_data = None
        logger.info(robotlist)
        for robot in robotlist:

            user_home = os.path.expanduser("~")

            path_to_save_vbmanager = f"{user_home}/logo_{robot.id}.txt"

            path_on_robot_vbmanager = cls._set_paths_to_logs_on_robots(robot.id)

            path_to_save_vbmanager = robot.get_container_log_data(path_to_save_vbmanager, path_on_robot_vbmanager)

            VB_MANAGER_FILTERED_LOG_PATH = cls._log_filter(path_to_save_vbmanager)

            logger.info(VB_MANAGER_FILTERED_LOG_PATH)
        
            if all_robots_ap_data is None:
                all_robots_ap_data = Comparer.create_final_robot_all_ap_dataframe(VB_MANAGER_FILTERED_LOG_PATH, robot.id)
                logger.info(type(all_robots_ap_data))

            else:
                all_robots_ap_data = pd.concat([all_robots_ap_data, Comparer.create_final_robot_all_ap_dataframe(VB_MANAGER_FILTERED_LOG_PATH, robot.id)], axis=0)
                logger.info(type(all_robots_ap_data))
            
            all_robots_ap_data.to_csv('Logs/all_ap_dataframe_file.txt', sep='\t', index=False)
        return all_robots_ap_data
            