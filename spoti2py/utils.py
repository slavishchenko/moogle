from typing import Dict, List, Union

from .exceptions import InvalidItemType


def parse_json(
    item_type: str, json_response: Dict, models: Dict
) -> Union[List[object], object]:
    """
    Maps json response to python classes.

    :param item_type: Specify item type you want to parse.
                      Allowed values: 'tracks', 'albums', 'artists'.
    :param json_response: JSON object to parse.
    :param models: Dictionary of classes you want to initialize with json data.
                   Keys correspond to item_type.
                   For each item_type specify main class and extra (additonal) classes.
    :return: List of objects or a single object.
    :rtype: Object.
    """
    classes = models.get(item_type)
    if not classes:
        raise InvalidItemType(
            "Allowed item_type values are: 'tracks', 'albums', 'artists'."
        )
    if isinstance(json_response, list):
        items = [classes["main"](**obj) for obj in json_response]
        for item in items:
            set_additional_classes(classes=classes, item=item)
        return items
    else:
        item = classes["main"](**json_response)
        set_additional_classes(classes=classes, item=item)
        return item


def set_additional_classes(classes: Dict, item: object) -> object:
    """
    Maps json objects to additional classes specified in MODELS dictionary under the key "extra".

    :param classes: Dictonary of classes needed to parse item_type.
    :param item: A class. E.G Artist, Album, etc.
    :return: Instance of item class.
    :rtype: Object.
    """
    for attr_name, cls in classes["extra"].items():
        if getattr(item, attr_name, "optional") == "optional":
            pass
        elif isinstance(getattr(item, attr_name), list):
            try:
                setattr(
                    item,
                    attr_name,
                    [cls(**instance) for instance in getattr(item, attr_name)],
                )
            except TypeError:
                setattr(item, attr_name, None)
        else:
            try:
                setattr(item, attr_name, cls(**getattr(item, attr_name)))
            except TypeError:
                setattr(item, attr_name, None)
    return item
