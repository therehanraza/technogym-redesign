from datetime import datetime, timezone


def now_utc():
    return datetime.now(timezone.utc)


def serialize_doc(doc):
    if not doc:
        return None

    for key, value in list(doc.items()):
        if isinstance(value, datetime):
            doc[key] = value.isoformat()

    return doc


def serialize_docs(docs):
    return [serialize_doc(doc) for doc in docs]
