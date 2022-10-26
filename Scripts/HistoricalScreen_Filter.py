# Below codestring is used to create filters to show different regions data in  product historic screen.

import pandas as pd
import json
from itertools import chain


def getLogger():
    import logging
    logging.basicConfig(filename="UIACLogger.log",
                        format='%(asctime)s %(message)s',
                        filemode='a')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    return logger


logger = getLogger()


def read_dataset(filename):
    # Read dataset from the github.
    logger.info(f"Read dataset file: {filename}")
    try:
        dataset_url = f"https://raw.githubusercontent.com/saipraneeth4/codx_dataset/main/dataset/{filename}"
        dframe = pd.read_csv(dataset_url)
        return dframe
    except Exception as error_msg:
        logger.info(f"Exception occured while reading the dataset: {dataset_url}"
                    f"Error Info is  {error_msg}")


def get_response_filters(current_filter_params, df, default_values_selected, all_filters, multi_select_filters, extra_filters={}):
    logger.info("Preparing filter dictionary")
    # Usage
    # -----
    # >>> filter_df = pd.DataFrame(columns=[....])    # Optional operation
    # >>> filter_df = final_ADS.groupby(......)       # Optional operation
    # >>> default_values_selected = {}    # The default value to be selected for a filter, provide filter_name, filter_values
    # >>> all_option_filters = []         # Filters with an All option
    # >>> multi_select_filters = []       # Filters with an multi_select option
    # >>> more_filters = {}               # Extra filters, provide filter_names, filter_options
    # >>> final_dict_out = get_response_filters(current_filter_params, filter_df, default_values_selected, all_option_filters, multi_select_filters, more_filters)
    # >>> dynamic_outputs = json.dumps(final_dict_out)
    # Returns
    # -------
    # A dict object containing the filters JSON structure

    filters = list(df.columns)
    default_values_possible = {}
    for item in filters:
        default_possible = list(df[item].unique())
        if item in all_filters:
            default_possible = list(chain(['All'], default_possible))
        default_values_possible[item] = default_possible
    if extra_filters:
        filters.extend(list(extra_filters.keys()))
        default_values_possible.update(extra_filters)
    if current_filter_params:
        selected_filters = current_filter_params["selected"]
        # current_filter = current_filter_params["current_filter"]
        # current_index = filters.index(current_filter)
        select_df = df.copy()
    final_dict = {}
    iter_value = 0
    data_values = []
    default_values = {}
    for item in filters:
        filter_dict = {}
        filter_dict["widget_filter_index"] = int(iter_value)
        filter_dict["widget_filter_function"] = False
        filter_dict["widget_filter_function_parameter"] = False
        filter_dict["widget_filter_hierarchy_key"] = False
        filter_dict["widget_filter_isall"] = True if item in all_filters else False
        filter_dict["widget_filter_multiselect"] = True if item in multi_select_filters else False
        filter_dict["widget_tag_key"] = str(item)
        filter_dict["widget_tag_label"] = str(item)
        filter_dict["widget_tag_input_type"] = "select",
        filter_dict["widget_filter_dynamic"] = True
        if current_filter_params:
            if item in df.columns:
                possible_values = list(select_df[item].unique())
                item_default_value = selected_filters[item]
                if item in all_filters:
                    possible_values = list(chain(['All'], possible_values))
                if item in multi_select_filters:
                    for value in selected_filters[item]:
                        if value not in possible_values:
                            if possible_values[0] == "All":
                                item_default_value = possible_values
                            else:
                                item_default_value = [possible_values[0]]
                else:
                    if selected_filters[item] not in possible_values:
                        item_default_value = possible_values[0]
                filter_dict["widget_tag_value"] = possible_values
                if item in multi_select_filters:
                    if 'All' not in item_default_value and selected_filters[item]:
                        select_df = select_df[select_df[item].isin(
                            item_default_value)]
                else:
                    if selected_filters[item] != 'All':
                        select_df = select_df[select_df[item]
                                              == item_default_value]
            else:
                filter_dict["widget_tag_value"] = extra_filters[item]
        else:
            filter_dict["widget_tag_value"] = default_values_possible[item]
            item_default_value = default_values_selected[item]
        data_values.append(filter_dict)
        default_values[item] = item_default_value
        iter_value = iter_value + 1
    final_dict["dataValues"] = data_values
    final_dict["defaultValues"] = default_values
    logger.info("Successfully prepared filter dictionary")
    return final_dict


def prepare_filter_json():
    logger.info(f"Preparing json for Filters in Historical Screen")
    # Preapre Filter json for Region in the Historical View Screen.
    dframe = read_dataset("ProductSales.csv")
    dframe = dframe.groupby(['Region']).sum().reset_index()
    filter_dframe = dframe[['Region']]
    default_values_selected = {"Region": 'Australia'}
    all_filters = []
    multi_select_filters = []
    # current_filter_params = {"selected": default_values_selected}
    final_dict_out = get_response_filters(
        current_filter_params, filter_dframe, default_values_selected, all_filters, multi_select_filters)
    logger.info(f"Successful prepared json for Filters in Historical Screen")
    return json.dumps(final_dict_out)


dynamic_outputs = prepare_filter_json()
