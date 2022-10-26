# Below codestring is used to generate json for breadcrumbs to display total number units of sales done over time.

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


def get_quantity_breadcrumbs():
    logger.info(
        f"Preparing action handler json for order quantity in historical screen")
    dframe = read_dataset("ProductSales.csv")
    total_quantity = dframe['OrderQuantity'].sum()
    actions = {
        "list": [
            {
                "text": "Order Quantity: ",
            },
            {
                "text": str(total_quantity),
                "color": "contrast",
                "style": {
                    "fontWeight": 600,
                }
            }
        ]
    }
    logger.info(
        f"Successfully prepared action handler json for order quantity in historical screen")
    return actions


# action_type = "get_screen_breadcrumbs"


if action_type == "get_screen_breadcrumbs":
    res = get_quantity_breadcrumbs()

dynamic_outputs = json.dumps(res)
