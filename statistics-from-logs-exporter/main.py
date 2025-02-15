#!/usr/bin/env python3
from Filters.log_generator import LogGenerator
from Filters.log_data_interpretation import AllApDataInterpreter
from Logs.logger_config import logger
from Util.api_connection import ApiConnection

def main():
    try:
        # Get Ip from active robots on fleet
        robot_list = ApiConnection.get_robot_objects()
        logger.info(robot_list)

        #Filter log files from robots
        all_ap_dataframe_file = LogGenerator.generate_log_output(robot_list)
        logger.info(all_ap_dataframe_file)
        print(all_ap_dataframe_file)

        ap_statistics_dataframe_file = AllApDataInterpreter.generate_ap_statistics_dataframe(all_ap_dataframe_file)
        logger.info(ap_statistics_dataframe_file)
        print(ap_statistics_dataframe_file)

    except Exception as e:
        logger.info(f"An error occurred when executing main script: {e}")
        # You can also log the exception or take other actions as needed

if __name__ == "__main__":

    main()


    ############## Script Revitalization! ###############
    # 1. Write unit tests one for specific unit test case in script.
    # 2. Write Documentaion with idea of applying it to future projects like robot controll.
    # 3. Structurize it finally dockerize etc, on jira etc.
    ########################################

