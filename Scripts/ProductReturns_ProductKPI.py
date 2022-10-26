# Below codestring is used to display the nuumber of uniue product types returned in a year.

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


def get_uniqueProductReturned():
    logger.info("Calculating number of unique products returned")
    dframe = read_dataset("ProductReturns.csv")
    uniqueProductQuantity = len(dframe['ProductName'].unique())
    metric = {}
    metric['title'] = "No of Unique Products Returned"
    metric['value'] = str(int(uniqueProductQuantity)) + ' unique Products'
    logger.info("Successfully calculated number of unique products returned")
    return metric


kpi_json = get_uniqueProductReturned()
dynamic_outputs = json.dumps(kpi_json)
