#!/usr/bin/env python
import os
import sys

try:
    me = os.path.realpath(os.readlink(__file__))
except OSError:
    me = os.path.realpath(__file__)
DEMO = os.path.dirname(me)
ROOT = os.path.normpath(os.path.join(DEMO, os.pardir, os.pardir))
TESTS = os.path.normpath(os.path.join(ROOT, 'tests'))
SRC = os.path.normpath(os.path.join(ROOT, 'src'))

sys.path.insert(0, SRC)
if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
    import logging

    l = logging.getLogger('raven.contrib.django.client.DjangoClient')

    from django.core.management import execute_from_command_line

    debug_on_error = '--pdb' in sys.argv
    args = [a for a in sys.argv if a != '--pdb']

    try:
        execute_from_command_line(args)
    except:
        if debug_on_error:
            import pdb, traceback
            type, value, tb = sys.exc_info()
            traceback.print_exc()
            pdb.post_mortem(tb)
        else:
            raise
