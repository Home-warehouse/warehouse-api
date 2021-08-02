import json
import graphene
from models.common import FilterRaportInput, SortRaportInput
from models.custom_columns import CustomColumnModel

from middlewares.integrations_apps.evernote import default_note
from models.product import ProductModel, ProductsListFilteredResolver


class parseRaportData:
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
    '''Boilerplate class for all integrations'''
    def raport():
        pass


def raportField(description, type, resolver, **kwargs):
    '''Create raport Field for graphene'''
    return graphene.Field(
        description=description,
        type=type,
        resolver=resolver,
        **kwargs
    )


class EvernoteType(graphene.ObjectType):
    created_note = graphene.Boolean()


class evernote(integration):
    def raport(**kwargs):
        raportData = ProductsListFilteredResolver.resolve_filter_sort_products(
            parent=None,
            info=None,
            show_custom_columns=kwargs['show_custom_columns'],
            filter_by=kwargs['filter_by'],
            sort_by=kwargs['sort_by'],
            limit=kwargs['limit']
        )
        raportData = parseRaportData().parseData(raportData=raportData)
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


def resolve_evernote(parent, info, **kwargs):
    if evernote.raport(**kwargs):
        return EvernoteType(created_note=True)
    return EvernoteType(created_note=False)


_evernoteRaportResolver = raportField(
    description="Evernote raport integration",
    type=EvernoteType,
    resolver=resolve_evernote,
    show_custom_columns=graphene.List(
                graphene.String,
                description="List of IDs of custom columns which are present in products"
    ),
    filter_by=graphene.Argument(graphene.List(
        FilterRaportInput), required=False),
    sort_by=graphene.Argument(SortRaportInput),
    limit=graphene.Int()
)


class IntegrationsResolvers(graphene.ObjectType):
    evernoteRaportResolver = _evernoteRaportResolver
