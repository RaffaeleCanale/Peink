import os
import tempfile
import hashlib
import json


def checksum(file):
    hash_md5 = hashlib.md5()
    with open(file, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def create_tmp_file(content=None, suffix=None):
    file = tempfile.NamedTemporaryFile(suffix=suffix).name
    if content:
        with open(file, "w") as text_file:
            text_file.write(content)
    return file


def get_package_file(package, file):
    package = (package or '').replace('.', '/')
    return os.path.join(os.getcwd(), package, file)


def read_as_string(file):
    with open(file, 'r') as myfile:
        return myfile.read()


def read_json(file):
    return json.loads(read_as_string(file))

# # __name__ in case you're within the package
# # - otherwise it would be 'lidtk' in this example as it is the package name
# path = 'classifiers/text_cat/README.md'  # always use slash
# filepath = pkg_resources.resource_filename(__name__, path)
# def get_location(file):
#     return os.path.realpath(
#         os.path.join(os.getcwd(), os.path.dirname(file))
#     )
