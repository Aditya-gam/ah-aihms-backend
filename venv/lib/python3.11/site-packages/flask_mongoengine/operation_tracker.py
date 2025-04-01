from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import str
from builtins import range
import functools
import time
import inspect
import copy
import re
import sys
import os
import socketserver

import pymongo
import pymongo.collection
import pymongo.command_cursor
import pymongo.cursor
import pymongo.helpers

from flask import g

from bson import SON


__all__ = ['queries', 'inserts', 'updates', 'removes', 'install_tracker',
           'uninstall_tracker', 'reset', 'response_sizes']


_original_methods = {
    'insert': pymongo.collection.Collection.insert,
    'update': pymongo.collection.Collection.update,
    'remove': pymongo.collection.Collection.remove,
    'refresh': pymongo.cursor.Cursor._refresh,
    '_unpack_response': pymongo.command_cursor.CommandCursor._unpack_response,
}

def tracker_array(attr):
    # This shouldn't be necessary but is just an additional safety measure in
    # in case we don't initialize g.mongoengine_operation_tracker but the
    # methods are monkey patched. In case something goes wrong, just return an
    # empty list that will be discarded.
    try:
        return g.mongoengine_operation_tracker[attr]
    except:
        return []

def is_quick():
    try:
        return g.mongoengine_operation_tracker_quick
    except: # Undefined, no context, cosmic rays etc.
        return False

# Wrap helpers._unpack_response for getting response size
@functools.wraps(_original_methods['_unpack_response'])
def _unpack_response(response, *args, **kwargs):

    result = _original_methods['_unpack_response'](
        response,
        *args,
        **kwargs
    )
    tracker_array('response_sizes').append(sys.getsizeof(response) / 1024.0)
    return result

# Wrap Cursor.insert for getting queries
@functools.wraps(_original_methods['insert'])
def _insert(collection_self, doc_or_docs, manipulate=True,
           safe=False, check_keys=True, **kwargs):
    start_time = time.time()
    result = _original_methods['insert'](
        collection_self,
        doc_or_docs,
        safe=safe,
        check_keys=check_keys,
        **kwargs
    )
    total_time = (time.time() - start_time) * 1000

    if is_quick():
        stack_trace, internal = [], False
    else:
        __traceback_hide__ = True
        stack_trace, internal = _tidy_stacktrace()

    tracker_array('inserts').append({
        'document': doc_or_docs,
        'safe': safe,
        'time': total_time,
        'stack_trace': stack_trace,
        'size': tracker_array('response_sizes')[-1] if tracker_array('response_sizes') else 0,
        'internal': internal
    })
    return result

# Wrap Cursor.update for getting queries
@functools.wraps(_original_methods['update'])
def _update(collection_self, spec, document, upsert=False,
           maniuplate=False, safe=False, multi=False, **kwargs):
    start_time = time.time()
    result = _original_methods['update'](
        collection_self,
        spec,
        document,
        upsert=upsert,
        safe=safe,
        multi=multi,
        **kwargs
    )
    total_time = (time.time() - start_time) * 1000

    if is_quick():
        stack_trace, internal = [], False
    else:
        __traceback_hide__ = True
        stack_trace, internal = _tidy_stacktrace()

    tracker_array('updates').append({
        'document': document,
        'upsert': upsert,
        'multi': multi,
        'spec': spec,
        'safe': safe,
        'time': total_time,
        'stack_trace': stack_trace,
        'size': tracker_array('response_sizes')[-1] if tracker_array('response_sizes') else 0,
        'internal': internal
    })
    return result

# Wrap Cursor.remove for getting queries
@functools.wraps(_original_methods['remove'])
def _remove(collection_self, spec_or_id, safe=False, **kwargs):
    start_time = time.time()
    result = _original_methods['remove'](
        collection_self,
        spec_or_id,
        safe=safe,
        **kwargs
    )
    total_time = (time.time() - start_time) * 1000

    __traceback_hide__ = True
    stack_trace, internal = _tidy_stacktrace()
    tracker_array('removes').append({
        'spec_or_id': spec_or_id,
        'safe': safe,
        'time': total_time,
        'stack_trace': stack_trace,
        'size': tracker_array('response_sizes')[-1] if tracker_array('response_sizes') else 0,
        'internal': internal
    })
    return result

# Wrap Cursor._refresh for getting queries
@functools.wraps(_original_methods['refresh'])
def _cursor_refresh(cursor_self):
    # Look up __ private instance variables
    def privar(name):
        return getattr(cursor_self, '_Cursor__{0}'.format(name))

    if privar('id') is not None:
        # getMore not query - move on
        return _original_methods['refresh'](cursor_self)

    # NOTE: See pymongo/cursor.py+557 [_refresh()] and
    # pymongo/message.py for where information is stored

    # Time the actual query
    start_time = time.time()
    result = _original_methods['refresh'](cursor_self)
    total_time = (time.time() - start_time) * 1000

    query_son = privar('query_spec')()
    if not isinstance(query_son, SON):

        if "$query" not in query_son:
            query_son = {"$query": query_son}

        data = privar("data")
        if data:
            query_son["data"] = data

        orderby = privar("ordering")
        if orderby:
            query_son["$orderby"] = orderby

        hint = privar("hint")
        if hint:
            query_son["$hint"] = hint

        maxScan = privar("max_scan")
        if maxScan:
            query_son["$maxScan"] = maxScan

    if is_quick():
        stack_trace, internal = [], False
        data = None
    else:
        __traceback_hide__ = True
        stack_trace, internal = _tidy_stacktrace()
        data = copy.copy(privar('data')),

    query_data = {
        'time': total_time,
        'operation': 'query',
        'stack_trace': stack_trace,
        'size': tracker_array('response_sizes')[-1] if tracker_array('response_sizes') else 0,
        'data': data,
        'internal': internal
    }

    # Collection in format <db_name>.<collection_name>
    collection_name = privar('collection')
    query_data['collection'] = collection_name.full_name.split('.')[1]

    if query_data['collection'] == '$cmd':
        query_data['operation'] = 'command'
        # Handle count as a special case
        if 'count' in query_son:
            # Information is in a different format to a standar query
            query_data['collection'] = query_son['count']
            query_data['operation'] = 'count'
            query_data['skip'] = query_son.get('skip')
            query_data['limit'] = query_son.get('limit')
            query_data['query'] = query_son['query']
        elif 'mapreduce' in query_son:
            query_data['collection'] = query_son['mapreduce']
            query_data['operation'] = 'mreduce'
            query_data['query'] = query_son['query']
            query_data['data'] = {
                'map': re.sub('[\n\ ]+', ' ', str(query_son['map'])),
                'map_scope': query_son['map'].scope,
                'reduce': re.sub('[\n\ ]+', ' ', str(query_son['reduce'])),
                'finalize': re.sub('[\n\ ]+', ' ', str(query_son.get('finalize'))),
                'field': query_son.get('field'),
            }
        elif 'distinct' in query_son:
            query_data['collection'] = query_son['distinct']
            query_data['operation'] = 'distinct'
            query_data['query'] = query_son['query']
            query_data['data'] = {'key': query_son['key']}
        elif 'aggregate' in query_son:
            query_data['collection'] = query_son['aggregate']
            query_data['operation'] = 'aggregate'
            query_data['query'] = query_son['pipeline']
    else:
        # Normal Query
        query_data['skip'] = privar('skip')
        query_data['limit'] = privar('limit')
        query_data['query'] = query_son['$query']
        query_data['ordering'] = _get_ordering(query_son)

    tracker_array('queries').append(query_data)

    return result

def install_tracker():
    pymongo.collection.Collection.insert = _insert
    pymongo.collection.Collection.update = _update
    pymongo.collection.Collection.remove = _remove
    pymongo.cursor.Cursor._refresh = _cursor_refresh
    pymongo.command_cursor.CommandCursor._unpack_response = _unpack_response

def uninstall_tracker():
    pymongo.collection.Collection.insert = _original_methods['insert']
    pymongo.collection.Collection.update = _original_methods['update']
    pymongo.collection.Collection.remove = _original_methods['remove']
    pymongo.cursor.Cursor._refresh = _original_methods['refresh']
    pymongo.command_cursor.CommandCursor._unpack_response = _original_methods[
        '_unpack_response'
    ]

def reset():
    g.mongoengine_operation_tracker = {
        'queries': [],
        'inserts': [],
        'updates': [],
        'removes': [],
        'response_sizes': [],
    }

def _get_ordering(son):
    """Helper function to extract formatted ordering from dict.
    """
    def fmt(field, direction):
        return '{0}{1}'.format({-1: '-', 1: '+'}[direction], field)

    if '$orderby' in son:
        return ', '.join(fmt(f, d) for f, d in son['$orderby'].items())

def _tidy_stacktrace():
    """
    Tidy the stack_trace
    """
    socketserver_path = os.path.realpath(os.path.dirname(socketserver.__file__))
    pymongo_path = os.path.realpath(os.path.dirname(pymongo.__file__))
    paths = ['/site-packages/', '/flaskext/', socketserver_path, pymongo_path]
    internal = False

    # Check html templates
    fnames = []
    for i in range(100):
        try:
            fname = sys._getframe(i).f_code.co_filename
            if 'html' in fname:
                fnames.append(fname)
        except:
            break
    fnames = list(set(fnames))
    trace = []

    for path in fnames:
        if 'flask_debugtoolbar' in path:
            internal = True
        trace.append((path, '?', '?', '?', False))

    if trace:
        return trace, internal

    stack = inspect.stack()
    reversed(stack)

    trace = []
    for frame, path, line_no, func_name, text in (f[:5] for f in stack):
        s_path = os.path.realpath(path)
        # Support hiding of frames -- used in various utilities that provide
        # inspection.
        if '__traceback_hide__' in frame.f_locals:
            continue
        hidden = False
        if func_name == "<genexpr>":
            hidden = True
        if any([p for p in paths if p in s_path]):
            hidden = True
        if not text:
            text = ''
        else:
            text = (''.join(text)).strip()
        trace.append((path, line_no, func_name, text, hidden))
    return trace, internal
