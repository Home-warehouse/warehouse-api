import graphene
from services.integration_runners.integration import integration
from services.integrations_apps.evernote import default_note


class EvernoteType(graphene.ObjectType):
    created_note = graphene.Boolean()


class evernote(integration):
    def raport(self, ProductsListFilteredResolver, parseRaportData, **kwargs):
        kwargs['integrated_element']['show_custom_columns'] = list(
            map(lambda show_cc: show_cc['$oid'],
                kwargs['integrated_element']['show_custom_columns'])
        )
        kwargs['integrated_element']['sort_by'] = {
            'custom_column': kwargs['integrated_element']['sort_by']['custom_column']['$oid'],
            'value': kwargs['integrated_element']['sort_by']['value']
        }

        raportData = ProductsListFilteredResolver.resolve_filter_sort_products(
            parent=None,
            info=None,
            show_custom_columns=kwargs['integrated_element']['show_custom_columns'],
            filter_by=kwargs['integrated_element']['filter_by'],
            sort_by=kwargs['integrated_element']['sort_by'],
            limit=kwargs['integrated_element']['short_results']
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
        if self.config['noteType'] == "NOTE":
            return default_note(self.config['noteTitle'], lines).create_note()
        if self.config['noteType'] == "TODO":
            return default_note(self.config['noteTitle'], lines).create_todo()
        return False
