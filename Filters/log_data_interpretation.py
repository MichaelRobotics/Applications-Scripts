import pandas as pd
import re
from Filters.log_generator import LogGenerator
from Logs.logger_config import logger

class BaseDataInterpreter:

    @classmethod
    def _extract_id_and_targets_from_brackets(cls, column):
        column_content = []
        column_name = ""

        try:
            match = re.match(r'(\w+)\(([^)]*)\)', column)
            if not match:
                raise ValueError("Invalid format for column. Expected format: 'column_name(content)'")

            column_name = match.group(1)  # Extracting column name
            content = match.group(2)  # Extracting content within brackets

            # Split the content by commas to create a list
            column_content = [item.strip() for item in content.split(',')]
        except re.error as e:
            raise ValueError(f"Regex error: {e}")
        except Exception as ex:
            raise ValueError(f"An error occurred: {ex}")

        return column_content, column_name
    
    @classmethod
    def _create_ap_df_frame(cls,name="initial", succ_rate=0.0, success=0, failure=0, action_error=0, dock_error=0):
        ap_df_frame = {
            'AP_NAME()': name,
            'SUCC_RATE()': succ_rate,
            'SUCCESS()': success,
            'FAILURE()': failure,
            'ACTION_ERROR(ACTION_ERROR, DOCK_CORRECT)': action_error,
            'DOCK_ERROR(DOCK_TRY, UNDOCK_INCORRECT)': dock_error
        }

        ap_df_frame = pd.DataFrame(ap_df_frame, index=[0])
        return ap_df_frame
    
    @classmethod
    def _check_for_positive_task(cls, value, fail):
        if not isinstance(fail, int):
            raise ValueError("The 'fail' argument must be a int value.")
        
        if fail:
            return value  # No increment if fail is True
        else:
            return value + 1
        
    @classmethod
    def _check_for_negative_task(cls, value, fail):
        if not isinstance(fail, int):
            raise ValueError("The 'fail' argument must be a int value.")
        
        if not fail:
            return value  # No increment if fail is False
        else:
            return value + 1
        
    @classmethod
    def _check_for_succes_rate(cls, succ: int, fail: int):
        if succ < 0 or fail < 0 or (succ + fail) == 0:
            raise ValueError("""Success and failure counts should be non-negative integers.  
                             The sum of success and failure counts should be greater than zero.""")
        try:
            succ_rate = round(succ / (succ + fail), 2) * 100
            return succ_rate
        except ZeroDivisionError:
            # Handle the case where the denominator is zero (avoid division by zero)
            return 0  # You can customize this based on your application logic
        except Exception as e:
            logger.info(f"An unexpected error occurred: {e}")
            # Handle other unexpected errors that might occur

    @classmethod
    def _check_for_failed_dock(cls, targets_list, value, single_ap_df):
        try:
            set_failure = 0
            DOCK_TRY_MAX_NUMBER = 3
            UNDOCK_INCORRECT_MAX_NUMBER = 0
            DF_ROW_INDEX = 0

            for col in single_ap_df.columns:
                # Remove the string within brackets including brackets
                cleaned_col_name = re.sub(r'\(.*\)', '', col).strip()

                # Check if the cleaned column name is in column_search_list
                if cleaned_col_name in targets_list:
                    if cleaned_col_name == "DOCK_TRY":
                        if single_ap_df.loc[DF_ROW_INDEX, col] >= DOCK_TRY_MAX_NUMBER:
                            set_failure = 1

                    elif cleaned_col_name == "UNDOCK_INCORRECT":
                        if single_ap_df.loc[DF_ROW_INDEX, col] > UNDOCK_INCORRECT_MAX_NUMBER:
                            set_failure = 1

            value = value + set_failure
            return value, set_failure
        except Exception as e:
            logger.info(f"Error check_for_failed_dock: {e}")

    @classmethod
    def _check_for_failed_action(cls, targets_list, value, single_ap_df):
        try:
            set_failure =  0
            DF_ROW_INDEX = 0
            for col in single_ap_df.columns:
                # Remove the string within brackets including brackets
                cleaned_col_name = re.sub(r'\(.*\)', '', col).strip()

                # Check if the cleaned column name is in column_search_list
                if cleaned_col_name in targets_list:
                    if cleaned_col_name == "ACTION_ERROR":
                        if single_ap_df.loc[DF_ROW_INDEX, col] > 0:
                            set_failure = 1

                    elif cleaned_col_name == "DOCK_CORRECT":
                        if single_ap_df.loc[DF_ROW_INDEX, col] == 0:
                            set_failure = 1

            value = value + set_failure
            return value, set_failure
        except Exception as e:
            logger.info(f"Error check_for_failed_action: {e}")

class AllApDataInterpreter(BaseDataInterpreter):

    @classmethod
    def _get_single_ap_name(cls, single_ap_df):
        try:
            # Check if the 'AP_NAME' column is in the DataFrame
            check_ap_name = single_ap_df['AP_NAME'].unique()
            if len(check_ap_name) == 1:
                return check_ap_name[0]
            else:
                raise ValueError("There is more than one unique value in the 'AP_NAME' column.")
        except KeyError:
            raise KeyError("Column 'AP_NAME' not found in raw data.")
        except Exception as e:
            logger.info(f"Error get_ap_name: {e}")

    @classmethod
    def _insert_ap_frame_into_statistics_df(cls, single_ap_df, all_ap_statistics_df):
        try:
            name_already_exists = False

            ap_name = cls._get_single_ap_name(single_ap_df)

            # If the statistics DataFrame has not yet been modified, modify its default first row and get the index number of the row
            if all_ap_statistics_df.loc[0, 'AP_NAME()'] == "initial":
                new_row_index_number = 0
                all_ap_statistics_df.loc[0, 'AP_NAME()'] = ap_name

            # Check if the AP_NAME is already in the statistics DataFrame
            else:
                # If the AP_NAME is already in statistics Dataframe, get index number of the row inside statistics DataFrame
                for index, row in all_ap_statistics_df.iterrows():
                    if row['AP_NAME()'] in ap_name:
                        logger.info(f"AP FOUND IN STATISTICS DF, NO MERGING NEW AP: \n {all_ap_statistics_df}")
                        new_row_index_number = index
                        name_already_exists = True
                # If not, create a new row and add to the DataFrame
                if name_already_exists == False:
                    # Create a new row to add to the DataFrame
                    new_row = cls._create_ap_df_frame(ap_name)
    
                    # Merge the new row into the DataFrame
                    logger.info(f"BEFORE MERGING NEW DF: \n {all_ap_statistics_df}")
                    all_ap_statistics_df = pd.concat([all_ap_statistics_df, new_row], ignore_index=True)
                    logger.info(f"AFTER MERGING NEW DF: \n {all_ap_statistics_df}")

                    # get the index number of the inserted row in the statistics DataFrame
                    new_row_index_number = index + 1
            return new_row_index_number, all_ap_statistics_df
        except Exception as e:
            logger.info(f"Error generate_all_robot_dataframe: {e}")

    @classmethod
    def _update_dataframe(cls, all_ap_statistics_df: pd.DataFrame, ap_frame_row_num: int, column: str, new_value: int):
        all_ap_statistics_df.loc[ap_frame_row_num, column] = new_value
        return all_ap_statistics_df

    @classmethod
    def _check_for_errors(cls, ap_row_to_fill, single_ap_df, ap_frame_row_num, all_ap_statistics_df):
        error = int()

        # At FIRST check if there are any DOCK_ERROR or ACTION_ERROR
        for column, value in ap_row_to_fill.items():
            targets_list, column_name = cls._extract_id_and_targets_from_brackets(column)
            if column_name == "DOCK_ERROR":
                new_value, err = cls._check_for_failed_dock(targets_list, value, single_ap_df)
                error += err
                all_ap_statistics_df = cls._update_dataframe(all_ap_statistics_df, ap_frame_row_num, column, new_value)
            elif column_name == "ACTION_ERROR":
                new_value, err = cls._check_for_failed_action(targets_list, value, single_ap_df)
                error = err
                all_ap_statistics_df = cls._update_dataframe(all_ap_statistics_df, ap_frame_row_num, column, new_value)
        return error, all_ap_statistics_df
    
    @classmethod
    def _set_succes_or_failure(cls, ap_row_to_fill, ap_frame_row_num, all_ap_statistics_df, error):
        succ, fail= int(), int()
        
        # At SECOND check for SUCCES and FAILURE based on DOCK_ERROR and ACTION_ERROR        
        for column, value in ap_row_to_fill.items():
            targets_list, column_name = cls._extract_id_and_targets_from_brackets(column)
            if column_name == "SUCCESS":
                new_value = cls._check_for_positive_task(value, error)
                all_ap_statistics_df = cls._update_dataframe(all_ap_statistics_df, ap_frame_row_num, column, new_value)
                succ = new_value
            elif column_name == "FAILURE":
                new_value = cls._check_for_negative_task(value, error)
                all_ap_statistics_df = cls._update_dataframe(all_ap_statistics_df, ap_frame_row_num, column, new_value)
                fail = new_value
        return all_ap_statistics_df, succ, fail
    
    @classmethod
    def _set_succes_rate(cls, ap_row_to_fill, ap_frame_row_num, all_ap_statistics_df, succ, fail):
        # At LAST check for SUCC_RATE
        for column, value in ap_row_to_fill.items():
            targets_list, column_name = cls._extract_id_and_targets_from_brackets(column)
            if column_name == "SUCC_RATE":
                new_value = cls._check_for_succes_rate(succ, fail)
                succ_perc = f'{new_value}'
                all_ap_statistics_df.loc[ap_frame_row_num, column] = succ_perc
            elif column_name == "AP_NAME":
                logger.info("AP data updated")
        return all_ap_statistics_df, succ_perc
    
    @classmethod
    def _fill_inserted_ap_frame(cls, single_ap_df: pd.DataFrame, ap_frame_row_num: int, all_ap_statistics_df: pd.DataFrame):

        ap_row_to_fill = all_ap_statistics_df.iloc[ap_frame_row_num]
        try:
            error, all_ap_statistics_df = cls._check_for_errors(ap_row_to_fill, single_ap_df, ap_frame_row_num, all_ap_statistics_df)

            all_ap_statistics_df, succ, fail = cls._set_succes_or_failure(ap_row_to_fill, ap_frame_row_num, all_ap_statistics_df, error)

            all_ap_statistics_df, succ_perc = cls._set_succes_rate(ap_row_to_fill, ap_frame_row_num, all_ap_statistics_df, succ, fail)

        except KeyError as e:
            logger.info(f"Error occurred due to missing data or column at _fill_inserted_ap_frame: {e}")
            # Handle this error case gracefully, log the issue, or take appropriate action
        except ValueError as e:
            logger.info(f"Value error occurred at _fill_inserted_ap_frame: {e}")
            # Handle this error case gracefully, log the issue, or take appropriate action
        except Exception as e:
            logger.info(f"An unexpected error occurred at _fill_inserted_ap_frame: {e}")
            # Handle other unexpected errors that might occur
        return all_ap_statistics_df
    
    @classmethod
    def generate_ap_statistics_dataframe(cls, all_ap_dataframe: LogGenerator):
        try:
            all_ap_statistics_df = cls._create_ap_df_frame()

            for index, row in all_ap_dataframe.iterrows():
                
                single_ap_df = pd.DataFrame([row])

                ap_frame_row_num, all_ap_statistics_df = cls._insert_ap_frame_into_statistics_df(single_ap_df, all_ap_statistics_df)
                all_ap_statistics_df = cls._fill_inserted_ap_frame(single_ap_df, ap_frame_row_num, all_ap_statistics_df)
                
            all_ap_statistics_df.to_csv('Logs/interpreted_data_file.txt', sep='\t', index=False)

            return all_ap_statistics_df
        except Exception as e:
            logger.info(f"Error generate_all_robot_dataframe: {e}")


#####################TESTS#####################################
if __name__ == "__main__":
    pass

