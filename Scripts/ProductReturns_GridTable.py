# Below codestring is used to view the product returns details.

import pandas as pd
import json


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


def generate_dynamic_table(dframe, name='Sales', grid_options={"tableSize": "small", "tableMaxHeight": "80vh", "quickSearch": True}, group_headers=[], grid="auto"):
    logger.info("Generate dynamic Grid table json from dframe")
    table_dict = {}
    table_props = {}
    table_dict.update({"grid": grid, "type": "tabularForm",
                      "noGutterBottom": True, 'name': name})
    values_dict = dframe.dropna(axis=1).to_dict("records")
    table_dict.update({"value": values_dict})
    col_def_list = []
    for col in list(dframe.columns):
        col_def_dict = {}
        col_def_dict.update({"headerName": col, "field": col})
        col_def_list.append(col_def_dict)
    table_props["groupHeaders"] = group_headers
    table_props["coldef"] = col_def_list
    table_props["gridOptions"] = grid_options
    table_dict.update({"tableprops": table_props})
    logger.info("Successfully generated dynamic Grid table json from dframe")
    return table_dict


def build_grid_table_json():
    logger.info("Preparing grid table json for Product Returns Screen")
    form_config = {}
    dframe = read_dataset("ProductReturns.csv")
    form_config['fields'] = [generate_dynamic_table(dframe)]
    grid_table_json = {}
    grid_table_json['form_config'] = form_config
    logger.info(
        "Successfully prepared grid table json for Product Returns Screen")
    return grid_table_json


grid_table_json = build_grid_table_json()
dynamic_outputs = json.dumps(grid_table_json)
