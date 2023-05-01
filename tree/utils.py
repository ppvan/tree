import uuid


# Django CKEditor helper
def get_filename(filename, request):
    return filename.upper()


def hashed_filename(instance, filename):
    extension = filename.split(".")[-1]
    uuid_name = uuid.uuid1().hex
    return f"{uuid_name}.{extension}"
