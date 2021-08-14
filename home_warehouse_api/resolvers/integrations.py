import graphene

from models.common import product_filter_fields
from resolvers.products_filter import ProductsListFilteredResolver, parseRaportData
from services.integrations.evernote import evernote


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


def resolve_evernote(parent, info, **kwargs):
    new_kwargs = {
        'integrated_element': dict((key, value) for key, value in kwargs.items())
    }
    new_kwargs['integrated_element']['short_results'] = new_kwargs['integrated_element']['limit']

    if evernote(kwargs.get('config')).raport(
        ProductsListFilteredResolver,
        parseRaportData,
            **new_kwargs):
        return EvernoteType(created_note=True)
    return EvernoteType(created_note=False)


_evernoteRaportResolver = raportField(
    description="Evernote raport integration",
    type=EvernoteType,
    resolver=resolve_evernote,
    config=graphene.String(required="True"),
    **product_filter_fields
)


class IntegrationsResolvers(graphene.ObjectType):
    evernoteRaportResolver = _evernoteRaportResolver
