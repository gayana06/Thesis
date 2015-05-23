# Copyright (c) 2010-2012 OpenStack Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Monkey Patch httplib.HTTPResponse to buffer reads of headers. This can improve
performance when making large numbers of small HTTP requests.  This module
also provides helper functions to make HTTP connections using
BufferedHTTPResponse.

.. warning::

    If you use this, be sure that the libraries you are using do not access
    the socket directly (xmlrpclib, I'm looking at you :/), and instead
    make all calls through httplib.
"""

from swift import gettext_ as _
from urllib import quote
import logging
import time
import socket

from eventlet.green.httplib import CONTINUE, HTTPConnection, HTTPMessage, \
    HTTPResponse, HTTPSConnection, _UNKNOWN
#from httplib  import CONTINUE, HTTPConnection, HTTPMessage, \
#    HTTPResponse, HTTPSConnection, _UNKNOWN

from datetime import datetime

class BufferedHTTPResponse(HTTPResponse):
    """HTTPResponse class that buffers reading of headers"""

    def __init__(self, sock, debuglevel=0, strict=0,
                 method=None):          # pragma: no cover
        self.sock = sock
        # sock is an eventlet.greenio.GreenSocket
        # sock.fd is a socket._socketobject
        # sock.fd._sock is a socket._socket object, which is what we want.
        self._real_socket = sock.fd._sock
        self.fp = sock.makefile('rb')
        self.debuglevel = debuglevel
        self.strict = strict
        self._method = method

        self.msg = None

        # from the Status-Line of the response
        self.version = _UNKNOWN         # HTTP-Version
        self.status = _UNKNOWN          # Status-Code
        self.reason = _UNKNOWN          # Reason-Phrase

        self.chunked = _UNKNOWN         # is "chunked" being used?
        self.chunk_left = _UNKNOWN      # bytes left to read in current chunk
        self.length = _UNKNOWN          # number of bytes left in response
        self.will_close = _UNKNOWN      # conn will close at end of response

    def expect_response(self):
	#with open("/home/ubuntu/spawn.txt", "a") as tran_file:
	#    tran_file.write("At expected_response Datetime = "+str(datetime.now())+"\n")
        if self.fp or True:
            self.fp.close()
            self.fp = None
	#with open("/home/ubuntu/spawn.txt", "a") as tran_file:
        #    tran_file.write("Before self.fp Datetime = "+str(datetime.now())+"\n")

        self.fp = self.sock.makefile('rb', 0)
	#with open("/home/ubuntu/spawn.txt", "a") as tran_file:
        #    tran_file.write("After sef.fp and Before read_status Datetime = "+str(datetime.now())+"\n")
        version, status, reason = self._read_status()
	#with open("/home/ubuntu/spawn.txt", "a") as tran_file:
    	#    tran_file.write("After read status Version = "+str(version)+" Status="+str(status)+" Datetime="+str(datetime.now())+"\n")
        if status != CONTINUE:
            #with open("/home/ubuntu/spawn.txt", "a") as tran_file:
            #    tran_file.write("At If start  Datetime = "+str(datetime.now())+"\n")
	    self._read_status = lambda: (version, status, reason)
            #with open("/home/ubuntu/spawn.txt", "a") as tran_file:
            #    tran_file.write("At If next  Datetime = "+str(datetime.now())+"\n")
            self.begin()
	    #with open("/home/ubuntu/spawn.txt", "a") as tran_file:
            #    tran_file.write("At If last  Datetime = "+str(datetime.now())+"\n")
        else:
            self.status = status
            self.reason = reason.strip()
            self.version = 11
            self.msg = HTTPMessage(self.fp, 0)
            self.msg.fp = None

    def nuke_from_orbit(self):
        """
        Terminate the socket with extreme prejudice.

        Closes the underlying socket regardless of whether or not anyone else
        has references to it. Use this when you are certain that nobody else
        you care about has a reference to this socket.
        """
        if self._real_socket:
            # this is idempotent; see sock_close in Modules/socketmodule.c in
            # the Python source for details.
            self._real_socket.close()
        self._real_socket = None
        self.close()

    def close(self):
        HTTPResponse.close(self)
        self.sock = None
        self._real_socket = None


class BufferedHTTPConnection(HTTPConnection):
    """HTTPConnection class that uses BufferedHTTPResponse"""
    response_class = BufferedHTTPResponse

    def connect(self):
        #self._connected_time = time.time()
        #return HTTPConnection.connect(self)
	#with open("/home/ubuntu/spawn.txt", "a") as tran_file:
    	#    tran_file.write("At Connect = "+str(datetime.now())+"\n")
	self._connected_time = time.time()
        ret = HTTPConnection.connect(self)
        #self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
	#self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	#self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        return ret

    def putrequest(self, method, url, skip_host=0, skip_accept_encoding=0):
        self._method = method
        self._path = url
        return HTTPConnection.putrequest(self, method, url, skip_host,
                                         skip_accept_encoding)

    def getexpect(self):
        response = BufferedHTTPResponse(self.sock, strict=self.strict,
                                        method=self._method)
        #with open("/home/ubuntu/spawn.txt", "a") as tran_file:
    	#    tran_file.write("Before Response at = "+str(datetime.now())+" SOCK="+str(self.sock)+"\n")
	response.expect_response()
	#with open("/home/ubuntu/spawn.txt", "a") as tran_file:
        #    tran_file.write("After Response at = "+str(datetime.now())+"\n")
        return response
    #gayana-start
    def close(self):
	#pass
	HTTPConnection.close(self)
	#with open("/home/ubuntu/spawn.txt", "a") as tran_file:
        #    tran_file.write("Connection closed = "+str(datetime.now())+"\n")
    	#HTTPResponse.close(self)
	#HTTPResponse.nuke_from_orbit(self)
     
    #gayana-end
    def getresponse(self):
        response = HTTPConnection.getresponse(self)
        logging.debug(_("HTTP PERF: %(time).5f seconds to %(method)s "
                        "%(host)s:%(port)s %(path)s)"),
                      {'time': time.time() - self._connected_time,
                       'method': self._method, 'host': self.host,
                       'port': self.port, 'path': self._path})
        return response


def http_connect(ipaddr, port, device, partition, method, path,
                 headers=None, query_string=None, ssl=False):
    """
    Helper function to create an HTTPConnection object. If ssl is set True,
    HTTPSConnection will be used. However, if ssl=False, BufferedHTTPConnection
    will be used, which is buffered for backend Swift services.

    :param ipaddr: IPv4 address to connect to
    :param port: port to connect to
    :param device: device of the node to query
    :param partition: partition on the device
    :param method: HTTP method to request ('GET', 'PUT', 'POST', etc.)
    :param path: request path
    :param headers: dictionary of headers
    :param query_string: request query string
    :param ssl: set True if SSL should be used (default: False)
    :returns: HTTPConnection object
    """
    if isinstance(path, unicode):
        try:
            path = path.encode("utf-8")
        except UnicodeError as e:
            logging.exception(_('Error encoding to UTF-8: %s'), str(e))
    path = quote('/' + device + '/' + str(partition) + path)
    return http_connect_raw(
        ipaddr, port, method, path, headers, query_string, ssl)


def http_connect_raw(ipaddr, port, method, path, headers=None,
                     query_string=None, ssl=False):
    """
    Helper function to create an HTTPConnection object. If ssl is set True,
    HTTPSConnection will be used. However, if ssl=False, BufferedHTTPConnection
    will be used, which is buffered for backend Swift services.

    :param ipaddr: IPv4 address to connect to
    :param port: port to connect to
    :param method: HTTP method to request ('GET', 'PUT', 'POST', etc.)
    :param path: request path
    :param headers: dictionary of headers
    :param query_string: request query string
    :param ssl: set True if SSL should be used (default: False)
    :returns: HTTPConnection object
    """
    if not port:
        port = 443 if ssl else 80
    if ssl:
        conn = HTTPSConnection('%s:%s' % (ipaddr, port))
    else:
        conn = BufferedHTTPConnection('%s:%s' % (ipaddr, port))
    if query_string:
        path += '?' + query_string
    conn.path = path
    conn.putrequest(method, path, skip_host=(headers and 'Host' in headers))
    if headers:
        for header, value in headers.iteritems():
            conn.putheader(header, str(value))
    conn.endheaders()
    return conn