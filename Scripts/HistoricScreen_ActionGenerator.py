# Below codestring is used to create action generator that triggers action handler  to display breadcrumbs 
# to show total units of product sale over time.

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


def get_action_generator():
    logger.info(f"Preparing action generator json for Historical screen")
    action_generator = {
        "actions": [{
            "action_type": "get_screen_breadcrumbs",
            "component_type": "text_list",
            "params": {
                "fetch_on_load": True
            },
            "position": {
                "portal": "screen_top_left"
            }
        }]
    }

    logger.info(
        f"Successfully prepared action generator json for Historical screen")
    return action_generator


res = get_action_generator()
dynamic_outputs = json.dumps(res)
