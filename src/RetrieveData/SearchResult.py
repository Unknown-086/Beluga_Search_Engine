class SearchResult:
    def __init__(self):
        self.doc_id = None
        self.title = None
        self.url = None
        self.description = None
        self.source = None

    def to_dict(self):
        return {
            "docId": self.doc_id,  # Note: camelCase to match Java
            "title": self.title,
            "url": self.url,
            "description": self.description,
            "source": self.source
        }