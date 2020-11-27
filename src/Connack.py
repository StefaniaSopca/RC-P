from pachet import *


class ConnackVariable(VariableHeader):
    __slots__ = ('session_present', 'return_code')

    def __init__(self, session_present = None, return_code = None):
        super().__init__()
        self.session_present = session_present
        self.return_code = return_code






    def to_bytes(self):
        ret = bytearray(2)
        if self.session_present:
            ret[0] = 1
        else:
            ret[0] = 0

        ret[1] = self.return_code
        return ret

    def __repr__(self):
        return type(self).__name__ + '(session_parent={0}, return_code={1})' \
            .format(hex(self.session_parent), hex(self.return_code))


class ConnackPacket(MQTTPacket):
    VARIABLE_HEADER = ConnackVariable
    PAYLOAD = None

    @property
    def get_return_cod(self):
        return self.variable_header.return_code

    @return_code.setter
    def set_return_code(self, new_code):
        self.variable_header.return_code = new_code

    @property
    def session_present(self):
        return self.variable_header.session_present

    @session_present.setter
    def session_parent(self, session_new):
        self.variable_header.session_present = session_new

    def __init__(self, fixed : MQTTFixed = None, variable : ConnackVariable = None, payload = None):
        if fixed is None :
            h = MQTTFixed(CONNACK, 0x00)
        else:
            if fixed.packet_type is not CONNACK:
                raise Exception("Invalid fixed packet type %s for Connack init" % fixed.packet_type)
            h = fixed

        super().__init__(h)
        self.variable_header = variable
        self.payload = None
""""
    @classmethod
    def build(cls, session_present = None, return_code = None):
        var = ConnackVariable(session_present, return_code)
        p = ConnackPacket(variable_header=var)
        """



