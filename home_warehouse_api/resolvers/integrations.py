import graphene

from models.common import product_filter_fields
from services.integration_runners.evernote import evernote
from models.product import ProductsListFilteredResolver, parseRaportData


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
    if evernote.raport(parent, ProductsListFilteredResolver, parseRaportData, **kwargs):
        return EvernoteType(created_note=True)
    return EvernoteType(created_note=False)


_evernoteRaportResolver = raportField(
    description="Evernote raport integration",
    type=EvernoteType,
    resolver=resolve_evernote,
    noteTitle=graphene.String(
        required=True,
        description="Note title"
        ),
    noteType=graphene.String(
        required=True,
        description="Can take values: 'TODO', 'NOTE'"
        ),
    **product_filter_fields
)


class IntegrationsResolvers(graphene.ObjectType):
    evernoteRaportResolver = _evernoteRaportResolver
