from os import getenv
from datetime import datetime

from resolvers.products_filter import ProductsListFilteredResolver, parseRaportData

from services.integrations.integration import integration

from evernote.api.client import EvernoteClient
import evernote.edam.type.ttypes as Types


class default_note:
    client = EvernoteClient(token=getenv("INTEGRATIONN_EVERNOTE_TOKEN"))
    noteStore = client.get_note_store()
    note = Types.Note()

    def __init__(self, title, lines: list(str())):
        self.title = title
        self.lines = lines
        self.start_note()

    def start_note(self):
        self.note.content = '<?xml version="1.0" encoding="UTF-8"?>'
        self.note.content += '<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
        self.note.content += '<en-note>'
        noteTitleGenerated = self.title + " - generated at - " + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.note.title = noteTitleGenerated

    def end_note(self):
        self.note.content += '</en-note>'
        self.noteStore.createNote(self.note)
        return True

    def create_note(self):
        for line in self.lines:
            self.note.content += line + '<br/>'
        return self.end_note()

    def create_todo(self):
        for line in self.lines:
            self.note.content += '<en-todo/>' + line + '<br/>'
        return self.end_note()


class evernote(integration):
    def raport(self, **kwargs):

        if type(kwargs['integrated_element']['show_custom_columns'][0]) is not str:
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
                lambda parentNode:
                    parentNode['custom_column']['custom_column_name'] + " : " + parentNode['value'] + " | ",
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
