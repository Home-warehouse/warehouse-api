import json
import graphene
from models.custom_columns import CustomColumnModel

from middlewares.integrations_apps.evernote import default_note
from models.product import ProductModel, ProductsListFilteredResolver


class raportDataParse:
    def parse_cc(self, cc):
        cc_details = CustomColumnModel.to_json(cc['custom_column'])
        return {"custom_column": json.loads(cc_details), "value": cc['value']}

    def parse_product(self, product):
        cc = list(map(lambda cc: self.parse_cc(cc), product['custom_columns']))
        product['custom_columns'] = cc
        return json.loads(ProductModel.to_json(product))

    def parseData(self, raportData):
        return list(map(lambda doc: self.parse_product(doc), raportData))


class integration:
    def raport(self):
        return self


class EvernoteType(graphene.ObjectType):
    created_note = graphene.Boolean()


class evernote(integration):
    def raport():
        raportData = ProductsListFilteredResolver.resolve_filter_sort_products(
            parent=None,
            info=None,
            show_custom_columns=["60fc0fe0d5849902b88653cb", "60fc29d5d5849902b88653d0"],
            sort_by={"custom_column": "60fc0fe0d5849902b88653cb", "value": "-1"},
            filter_by=[],
            limit=30
        )
        raportData = raportDataParse().parseData(raportData=raportData)
        lines = []
        for parentNode in raportData:
            cc_values = map(
                lambda parentNode: parentNode['custom_column']['name'] + " : " + parentNode['value'] + " | ",
                list(parentNode['custom_columns'])
            )
            product = parentNode['product_name'] + ": "
            for cc_val in cc_values:
                product += cc_val + ' '
            lines.append(product)
        return default_note().create_note(lines)


def resolve_evernote(parent, info):
    if evernote.raport():
        return EvernoteType(created_note=True)
    return EvernoteType(created_note=False)


_evernote = graphene.Field(
    description="Try Evernote",
    type=EvernoteType,
    resolver=resolve_evernote
)


class IntegrationsResolvers(graphene.ObjectType):
    evernote = _evernote
