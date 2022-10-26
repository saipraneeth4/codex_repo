# Below codestring is used to perform detailed analysis of Product stock available over time.

import plotly.express as px
import pandas as pd
import json
import plotly.io as io


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


def getGraph(dframe, filters):
    logger.info(
        "Preparing bar graph json to understand products in stock available over time")
    for item in filters:
        if 'All' in filters[item]:
            continue
        elif isinstance(filters[item], list):
            dframe = dframe[dframe[item].isin(filters[item])]
        else:
            dframe = dframe[dframe[item] == filters[item]]
    fig = px.bar(dframe, x='StockDate', y='OrderQuantity', color='ProductName')
    # fig.show()
    logger.info(
        "Successfully prepared bar graph json to understand products in stock available over time")
    return io.to_json(fig)


selected_filters = {"Region": 'Australia'}
dframe = read_dataset("ProductSales.csv")
dynamic_outputs = getGraph(dframe, selected_filters)
