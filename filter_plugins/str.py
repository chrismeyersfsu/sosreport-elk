#!/usr/bin/python
def string_prefix(prefix, s):
    return prefix + s
def string_postfix(postfix, s):
    return s + postfix
class FilterModule(object):
    ''' Ansible filters. Python string operations.'''
    def filters(self):
        return {
            'string_prefix' : string_prefix,
            'string_postfix' : string_postfix
        }
