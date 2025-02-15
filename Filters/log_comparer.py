import pandas as pd
import re
from Logs.logger_config import logger

class Comparer:
        
    robot_dataframe = None  # dataframe of all filtered logs
    robot_id = None

    @classmethod
    def _create_robot_dataframe(cls, vbmanager_logs): 
        """
        Create a dataframe from the VB Manager log.
        """        
        data = []

        try:
            for line in vbmanager_logs.split("\n"):
                if line.strip() != "":
                    try:
                        timestamp = line.split(" - ")[0].strip("'")
                        rest = " - ".join(line.split(" - ")[1:]).strip("'")
                        data.append([timestamp, rest])
                    except IndexError:
                        logger.info("Error while splitting line: ", line)
                        continue

            init_df = pd.DataFrame(data, columns=["Time", "rest"])
            init_df['Time'] = pd.to_datetime(init_df['Time'], format='%Y-%m-%d %H:%M:%S,%f')
            init_df['Time'] = init_df['Time'].dt.strftime('%Y-%m-%d %H:%M:%S')
            logger.info("Initial DataFrame:")
            logger.info(init_df)
            #!! WRITING TO CSV ONLY FOR TESTING !!#
            #init_df.to_csv('_create_robot_dataframe.txt', index=False, sep='\t')
            cls.robot_dataframe = init_df

        except Exception as e:
            logger.info(f"Error in _create_robot_dataframe: {e}")
    
    @classmethod
    def _get_first_single_ap_from_robot_dataframe(cls):
        try:
            """
            Until AP exists, return time frames, cuts and saves them.
            """ 
            search_for_AP = False   
            found_started = False
            found_end = False
            filtered_rows = []
            AP_completed = 0

            # Iterate through each row to search for "Action completed" in the "rest" column and stop if "Action completed" is found
            for index, row in cls.robot_dataframe.iterrows():
                if found_started:
                    filtered_rows.append(row)
                    if "Action completed" in row['rest']:
                        found_end = True # Set flag to stop saving rows
                        break
                    elif "ActionPoint(id:" in row['rest']:
                        AP_completed += 1
                        break
                elif "ActionPoint(id:" in row['rest']:
                    filtered_rows.append(row)
                    AP_completed = 1
                    found_started = True  # Set flag to start saving rows
            if found_started == True and found_end == True and AP_completed == 1: # Define if operation ended successfully
                search_for_AP = True  
            else:
                search_for_AP = False
                filtered_rows = []
            return filtered_rows, search_for_AP
        
        except Exception as e:
            logger.info(f"Error in _get_first_single_ap_from_robot_dataframe: {e}")
            return None
        
    @classmethod
    def _delete_single_ap_raw_dataframe_from_robot_dataframe(cls, action_point_raw_dataframe):
        try:

            logger.info("Dataframe: Data from robot_dataframe to process:")
            logger.info(cls.robot_dataframe)
            # Get indexes that are common to both DataFrames
            common_indexes = cls.robot_dataframe.index.intersection(action_point_raw_dataframe.index)
            # Drop rows from self.robot_dataframe that have the same index as rows in action_point_raw_dataframe
            cls.robot_dataframe.drop(index=common_indexes, inplace=True)
            # Drop rows from self.robot_dataframe that match rows in ap_raw_df
            logger.info("Dataframe: Data after processing")
            logger.info(cls.robot_dataframe)

        except Exception as e:
            logger.info(f"Error in _delete_single_ap_raw_dataframe_from_robot_dataframe: {e}")

    @classmethod
    def _set_actions_single_ap_dataframe(cls, action_point_raw_dataframe, action_point_dataframe):
        try:
            for index, row in action_point_raw_dataframe.iterrows():
                rest_value = row['rest']
                for col in action_point_dataframe.columns[3:]:  # Starting from the 4th column onwards (ommit the first 3 columns AKA 'Robot', 'TIME_START', 'TIME_END')
                    # Extracting values between parentheses using split and strip
                    values_inside_parentheses = col.split('(')[-1].split(')')[0].strip()
                    # Creating a list by splitting the extracted values using comma as a delimiter
                    result_list = [value.strip() for value in values_inside_parentheses.split(',')]
                    if any(string in rest_value for string in result_list):
                        action_point_dataframe.at[0, col] = action_point_dataframe.at[0, col] + 1
        except Exception as e:
            logger.info(f"Error in _set_actions_single_ap_dataframe: {e}")

    @classmethod
    def _extract_text_within_quotes(cls, text):
        """
        Extract text within quotes from a string.
        """
        try:
            matches = re.findall(r"'(.*?)'", text)
            return matches[0] if matches else ''
        except Exception as e:
            logger.info(f"Error in _extract_text_within_quotes: {e}")
            return ''

    @classmethod
    def _extract_text_within_parentheses_and_quotes(cls, text):
        """
        Extract text within parentheses and then within quotes from a string.
        """
        try:
            matches = re.findall(r'\((.*?)\)', text)
            if matches:
                text_within_parentheses = matches[0]
                return cls._extract_text_within_quotes(text_within_parentheses)
            else:
                return ''
        except Exception as e:
            logger.info(f"Error in _extract_text_within_parentheses_and_quotes: {e}")
            return ''

    @classmethod    
    def _set_name_single_ap_dataframe(cls, action_point_raw_dataframe, action_point_dataframe):
        try:
            """
            Iterate through the DataFrame and set the AP_NAME column based on the 'rest' column.
            """
            for index, row in action_point_raw_dataframe.iterrows():
                if "started." in row['rest']:
                    rest_value = row['rest']
                    print(f"Rest Second value \n {rest_value}")
                    extracted_text = cls._extract_text_within_parentheses_and_quotes(rest_value)
                    action_point_dataframe.at[0, "AP_NAME"] = extracted_text
        except Exception as e:
            logger.info(f"Error in _set_name_single_ap_dataframe: {e}")

    @classmethod
    def _set_time_single_ap_dataframe(cls, action_point_raw_dataframe, action_point_dataframe):
        try:
            start_date = "initial"
            end_date = "initial"

            # Iterate through each row in the DataFrame
            for index, row in action_point_raw_dataframe.iterrows():
                if "started" in row['rest']:
                    start_date = row['Time']
                elif "Action completed" in row['rest']:
                    end_date = row['Time']

            # Set the start and end times in the ap_df DataFrame
            action_point_dataframe.at[0, 'TIME_START'] = start_date
            action_point_dataframe.at[0, 'TIME_END'] = end_date
        except Exception as e:
            logger.info(f"Error in _set_time_single_ap_dataframe: {e}")

    @classmethod
    def _create_single_ap_dataframe_template(cls): 
        try:
            action_point_dataframe = pd.DataFrame({
                'Robot': [cls.robot_id],
                'TIME_START': ["Initial"],
                'TIME_END': ["Initial"],
                'AP_NAME': ["None"],
                'ACTION_ERROR(waiting, aborted)': [0],
                'DOCK_TRY(Position incorrect)': [0],
                'DOCK_CORRECT(Position correct)': [0],
                'UNDOCK_INCORRECT(Departing failed)': [0]
            })
            return action_point_dataframe
        except Exception as e:
            logger.info(f"Error _create_single_ap_dataframe_template: {e}")

    @classmethod
    def _create_final_single_ap_dataframe(cls, filtered_rows):   
        try:
            if filtered_rows:
                action_point_raw_dataframe = pd.DataFrame(filtered_rows)
                logger.info("Dataframe: AP data found in dataframe:")
            else:
                raise Exception("String 'ActionPoint(id:' was not found in any row before 'Action completed' in the 'rest' column.")
            
            action_point_dataframe = cls._create_single_ap_dataframe_template()
            cls._set_actions_single_ap_dataframe(action_point_raw_dataframe, action_point_dataframe)
            cls._set_name_single_ap_dataframe(action_point_raw_dataframe, action_point_dataframe)
            cls._set_time_single_ap_dataframe(action_point_raw_dataframe, action_point_dataframe)
            cls._delete_single_ap_raw_dataframe_from_robot_dataframe(action_point_raw_dataframe)
            #!! WRITING TO CSV ONLY FOR TESTING !!#
            #action_point_dataframe.to_csv('_create_final_single_ap_dataframe.txt', sep='\t', index=False)
            return action_point_dataframe
        except Exception as e:
            logger.info(f"Error _create_final_single_ap_dataframe: {e}")

    @classmethod
    def create_final_robot_all_ap_dataframe(cls, vb_manager_filtered_log_path: str, robot_id: str) -> pd.DataFrame:
        try:
            # reset class variables
            final_all_ap_dataframe = None
            cls.robot_id = robot_id
            
            with open(vb_manager_filtered_log_path, 'r') as file:
                vbmanager_logs = file.read()
            if not vbmanager_logs:
                vbmanager_logs = ""
                raise ValueError("File is empty")
            cls._create_robot_dataframe(vbmanager_logs)

            while True:
                filtered_rows, search_for_AP = cls._get_first_single_ap_from_robot_dataframe()
                if len(filtered_rows) == 0 or search_for_AP == False:
                    if cls.robot_dataframe.empty:
                        logger.info(f"""
                        No more AP found
                        Is robot dataframe empty: {cls.robot_dataframe.empty}
                        !!!ALL AP HAVE BEEN FOUND!!!.
                        """)

                    elif not cls.robot_dataframe.empty:
                        logger.info(f"""
                        Malformed input data.
                        Is robot dataframe empty: {cls.robot_dataframe.empty}
                        !!!CANNOT FIND AP - robot_dataframe DATA MALFORMED!!!.
                        """)
                    break
                else:
                    action_point_dataframe = cls._create_final_single_ap_dataframe(filtered_rows)
                    if final_all_ap_dataframe is None:
                        final_all_ap_dataframe = action_point_dataframe
                        logger.info(final_all_ap_dataframe)

                    else:
                        if set(final_all_ap_dataframe.columns) == set(action_point_dataframe.columns):
                            final_all_ap_dataframe = pd.concat([final_all_ap_dataframe, action_point_dataframe], axis=0)
                            logger.info("Dataframe: AP data extracted from dataframe:")
                            logger.info(final_all_ap_dataframe)
                        else:
                            raise Exception("Column structures are not identical. Cannot append.")
            return final_all_ap_dataframe
        except FileNotFoundError:
            logger.info(f"File not found: {vb_manager_filtered_log_path}")
        except Exception as e:
            logger.info(f"create_final_robot_ap_dataframe {e}")


if __name__ == "__main__":
    pass
