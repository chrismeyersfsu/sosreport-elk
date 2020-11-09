# python 3 headers, required if submitting to Ansible
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
        lookup: file
        author: Chris Meyers <cmeyers@redhat.com>
        version_added: "0.9"
        short_description: find sosreports in dirs
        description:
            - This lookup finds any sosreport in the dirs specified. Does not recurse
        options:
          _terms:
            description: path(s) of dirs to find sos reports in
            required: True
        notes:
          - None
"""
from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display

import os
import re

display = Display()


class LookupModule(LookupBase):

    def looks_like_sosreport(self, pathname):
        if pathname.startswith('sosreport'):
            return True
        return False

    def get_tower_hostname(self, root, pathname):
        path = os.path.join(root, pathname, "etc", "tower", "conf.d", "cluster_host_id.py")
        try:
            with open(path) as f:
                data = f.read()
            m = re.search("CLUSTER_HOST_ID = '(.*?)'", data)
            if m.group(1):
                return m.group(1)
        except FileNotFoundError:
            pass

        with open(os.path.join(root, pathname, "etc", "hostname")) as f:
            return f.read()

    def run(self, terms, variables=None, **kwargs):
        entry = {
            'hostname': '',
            'path': '',
        }

        # lookups in general are expected to both take a list as input and output a list
        # this is done so they work with the looping construct 'with_'.
        ret = []
        for term in terms:
            matches = []
            try:
                for x in os.listdir(term):
                    fullpath = os.path.join(term, x)
                    if not os.path.isdir(fullpath):
                        continue
                    if not self.looks_like_sosreport(x):
                        continue
                    entry = {
                        'hostname': self.get_tower_hostname(term, x),
                        'path': x,
                    }
                    ret.append(entry)
            except FileNotFoundError:
                pass

        return ret
