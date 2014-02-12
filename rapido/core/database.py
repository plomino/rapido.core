from zope.interface import implements
from zope.annotation.interfaces import IAnnotations
from persistent.dict import PersistentDict

from interfaces import IDatabase, IStorage, IDocument, IForm
from index import Index

ANNOTATION_KEY = "RAPIDO_ANNOTATION"


class Database(Index):
    """
    """
    implements(IDatabase)

    def __init__(self, context):
        self.context = context
        self.annotations = IAnnotations(context)
        if ANNOTATION_KEY not in self.annotations:
            self.annotations[ANNOTATION_KEY] = PersistentDict({
                'rules': {},
            })

    def initialize(self):
        self.storage.initialize()

    @property
    def storage(self):
        return IStorage(self.context)

    @property
    def url(self):
        return self.context.url()

    def create_document(self, docid=None):
        record = self.storage.create()
        doc = IDocument(record)
        if not docid:
            docid = str(hash(record))
        doc.set_item('docid', docid)
        return doc

    def get_document(self, id):
        if type(id) is int:
            record = self.storage.get(id)
            if record:
                return IDocument(record)
        elif type(id) is str:
            search = self.search('docid=="%s"' % id)
            if len(search) == 1:
                return search[0]

    def _documents(self):
        for record in self.storage.documents():
            yield IDocument(record)

    def documents(self):
        return list(self._documents())

    def get_form(self, form_id):
        form_obj = self.context.get(form_id)
        if form_obj:
            return IForm(form_obj)

    @property
    def rules(self):
        return self.annotations[ANNOTATION_KEY]["rules"]

    def set_rule(self, rule_id, rule_settings):
        self.annotations[ANNOTATION_KEY]['rules'][rule_id] = rule_settings

    def remove_rule(self, rule_id):
        if self.annotations[ANNOTATION_KEY]['rules'].get(rule_id):
            del self.annotations[ANNOTATION_KEY]['rules'][rule_id]

