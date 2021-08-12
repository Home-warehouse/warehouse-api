from os import getenv
from datetime import datetime

from integrations.evernote.build.lib.evernote.api.client import EvernoteClient
import integrations.evernote.build.lib.evernote.edam.type.ttypes as Types

dev_token = getenv("INTEGRATION_EVERNOTE_TOKEN")


class default_note:
    client = EvernoteClient(token=dev_token)
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
