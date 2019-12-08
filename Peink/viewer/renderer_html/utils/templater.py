from mako.template import Template
from core.utils import file_utils


def template(file, **kwargs):
    text = file_utils.read_as_string(file)
    return Template(text).render(**kwargs)
