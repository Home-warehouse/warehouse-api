from enum import Enum
from os import getenv
import json
from models.automatization import AutomatizationModel

if getenv("INTEGRATION_EVERNOTE_TOKEN"):
    from services.integrations.evernote import evernote


class ElementType(str, Enum):
    PRODUCT = 'PRODUCT'
    LOCATION = 'LOCATION'
    CUSTOM_COLUMN = 'CUSTOM_COLUMN'


def automatizations_checker(element: ElementType):
    # Check if there is automation saved in DB
    automatizations = list(AutomatizationModel.objects(elements_monitored=element))
    # IF SO -> execute it
    for automatization in automatizations:
        # Get automatization integrations
        integrated_element = json.loads(automatization.element_integrated.to_json())
        if integrated_element["raport_name"]:
            if automatization["app"] == 'EVERNOTE':
                if getenv("INTEGRATION_EVERNOTE_TOKEN"):
                    evernote(automatization['config']).raport(integrated_element=integrated_element)
