
import io
from websockets.protocol import WebSocketCommonProtocol
from websockets.exceptions import ConnectionClosed
from asyncio import StreamReader, StreamWriter
import logging


class ReaderAdapter:


    def read(self, n=-1) -> bytes:
     pass

    def feed_eof(self):
       pass


class WriterAdapter:


    def write(self, data):
       pass

    def drain(self):
       pass

    def get_peer_info(self):
       pass

    def close(self):
        pass



class WebSocketsReader(ReaderAdapter):

    def __init__(self, protocol: WebSocketCommonProtocol):
        self._protocol = protocol
        self._stream = io.BytesIO(b'')


    def read(self, n=-1) -> bytes:
        yield from self._feed_buffer(n)
        data = self._stream.read(n)
        return data

    def _feed_buffer(self, n=1):
        buffer = bytearray(self._stream.read())
        while len(buffer) < n:
            try:
                message = yield from self._protocol.recv()
            except ConnectionClosed:
                message = None
            if message is None:
                break
            if not isinstance(message, bytes):
                raise TypeError("message must be bytes")
            buffer.extend(message)
        self._stream = io.BytesIO(buffer)


class WebSocketsWriter(WriterAdapter):
    def __init__(self, protocol: WebSocketCommonProtocol):
        self._protocol = protocol
        self._stream = io.BytesIO(b'')

    def write(self, data):
        self._stream.write(data)


    def drain(self):

        data = self._stream.getvalue()
        if len(data):
            yield from self._protocol.send(data)
        self._stream = io.BytesIO(b'')

    def get_peer_info(self):
        return self._protocol.remote_address

    def close(self):
        yield from self._protocol.close()


class StreamReaderAdapter(ReaderAdapter):

    def __init__(self, reader: StreamReader):
        self._reader = reader


    def read(self, n=-1) -> bytes:
        if n == -1:
            data = yield from self._reader.read(n)
        else:
            data = yield from self._reader.readexactly(n)
        return data

    def feed_eof(self):
        return self._reader.feed_eof()


class StreamWriterAdapter(WriterAdapter):
    def __init__(self, writer: StreamWriter):
        self.logger = logging.getLogger(__name__)
        self._writer = writer
        self.is_closed = False

    def write(self, data):
        if not self.is_closed:
            self._writer.write(data)


    def drain(self):
        if not self.is_closed:
            yield from self._writer.drain()

    def get_peer_info(self):
        extra_info = self._writer.get_extra_info('peername')
        return extra_info[0], extra_info[1]


    def close(self):
        if not self.is_closed:
            self.is_closed = True # we first mark this closed so yields below don't cause races with waiting writes
            yield from self._writer.drain()
            if self._writer.can_write_eof():
                self._writer.write_eof()
            self._writer.close()
            try: yield from self._writer.wait_closed() # py37+
            except AttributeError: pass


class BufferReader(ReaderAdapter):
    def __init__(self, buffer: bytes):
        self._stream = io.BytesIO(buffer)

    def read(self, n=-1) -> bytes:
        return self._stream.read(n)


class BufferWriter(WriterAdapter):
    def __init__(self, buffer=b''):
        self._stream = io.BytesIO(buffer)

    def write(self, data):
        self._stream.write(data)


    def drain(self):
        pass

    def get_buffer(self):
        return self._stream.getvalue()

    def get_peer_info(self):
        return "BufferWriter", 0


    def close(self):
        self._stream.close()

