from enum import Enum
import json

from models.automatizations import AutomatizationModel
from services.integration_runners.evernote import evernote


class ElementType(str, Enum):
    product = 'product'
    # location = 'location'
    # raport = 'raport'


def automatizations_checker(element: ElementType, **kwargs):
    # Check if there is automation saved in DB
    automatizations = list(AutomatizationModel.objects(elements_monitored=element))
    # IF SO -> execute it
    for automatization in automatizations:
        # Get automatization integrations
        integrated_element = json.loads(automatization.element_integrated.to_json())
        if integrated_element["raport_name"]:
            if automatization["app"] == 'evernote':
                evernote(automatization['config']).raport(
                                kwargs['ProductsListFilteredResolver'],
                                kwargs['parseRaportData'],
                                integrated_element=integrated_element
                                )
