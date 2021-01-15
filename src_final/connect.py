from pachet import*
from packettype import CONNECT

import encode_decode
class ConnectVariable(VariableHeader):
    __slots__ = ('p_name', 'p_level','flags','keep_alive')

    USERNAME =0x80
    PASSWORD = 0x40
    WILL_RETAIN = 0x20
    WILL = 0x04
    WILL_QOS = 0x18
    CLEAN_SESSION = 0x02
    RESERVED = 0x01


    def __init__(self, connect_flags = 0x00, p_name = 'MQTT', p_level = 0x04,k_a=0):
        super().__init()
        self.flags = connect_flags
        self.p_name = p_name
        self.p_level = p_level
        self.keep_alive = k_a

    def __repr__(self):
        return "ConnectVariable(proto_name={0}, proto_level={1}, flags={2}, keepalive={3})".format(
            self.proto_name, self.proto_level, hex(self.flags), self.keep_alive)

    def set_flag (self, val, nr):
        if val:
            self.flags |= nr
        else:
            self.flags &= ~nr
    """"""
    def get_flag(self, nr):
        if self.flags & nr:
            return True
        else:
            return False

    @property
    def username(self) -> bool:
        return self.get_flag(self.USERNAME)

  
    def username_flag(self, val: bool):
        self.set_flag(val, self.USERNAME)

    @property
    def password_flag(self) -> bool:
        return self.get_flag(self.PASSWORD)

    @password_flag.setter
    def password_flag(self, val: bool):
        self.set_flag(val, self.PASSWORD)

    @property
    def will_retain_flag(self) -> bool:
        return self.get_flag(self.WILL_RETAIN)

    @will_retain_flag.setter
    def will_retain_flag(self, val: bool):
        self.set_flag(val, self.WILL_RETAIN)

    @property
    def will_flag(self) -> bool:
        return self.get_flag(self.WILL)

    @will_flag.setter
    def will_flag(self, val: bool):
        self.set_flag(val, self.WILL)

    @property
    def clean_session_flag(self) -> bool:
        return self.get_flag(self.CLEAN_SESSION)

    @clean_session_flag.setter
    def clean_session_flag(self, val: bool):
        self.set_flag(val, self.CLEAN_SESSION)

    @property
    def reserved_flag(self) -> bool:
        return self.get_flag(self.RESERVED)


    @property
    def will_qos(self):
        #select qos bits and shift
        return (self.flags & 0x18) >>3

    @will_qos.setter
    def will_qos(self, nr: int):
        #qos bit 0
        self.flags = self.flags & 0xe7
        aux = nr<<3
        self.flags |=aux

    def to_bytes(self) -> bytes:
        ret = bytearray
        ret.extend(encode_decode.encode_string())

        ret.append(self.p_level)
        ret.append(self.flags)
        ret.extend(int_to_bytes(self.keep_alive, 2))
        return ret

class ConnectPayload(Payload):
    __slots__ = ('id', 'will_topic', 'will_message', 'username', 'password')

    def __init__ (self, id = None, will_topic = None, will_message = None, username = None, password= None):
        super().__init__()
        self.id = id
        self.will_topic = will_topic
        self.will_message = will_message
        self.username = username
        self.password= password

    def __repr__(self):
        return "ConnectVariable(client_id={0}, will_topic={1}, will_message={2}, username={3}, password={4})". \
            format(self.id, self.will_topic, self.will_message, self.username, self.password)

    def to_bytes(self, fixed_header: FixedHeader, variable_header: ConnectVariable):
        ret = bytearray()

        ret.extend(encode_decode.encode_string(self.id))

        if variable_header.will_flag:
            ret.extend(encode_decode.encode_string(self.will_topic))
            ret.extend(encode_decode.encode_data_with_length(self.will_message))

        if variable_header.username_flag:
            ret.extend(encode_decode.encode_string(self.username))

        if variable_header.password_flag:
            ret.extend(encode_decode.encode_string(self.password))

        return ret


class ConnectPacket(MQTTPacket):
    VARIABLE = ConnectVariable
    PAYLOAD = ConnectPayload

    @property
    def p_name(self):
        return self.variable.p_name

   
    def p_name(self, name: str):
        self.variable.p_name = name

    @property
    def proto_level(self):
        return self.variable.p_level

    @proto_level.setter
    def proto_level(self, level):
        self.variable.p_level = level

    @property
    def username_flag(self):
        return self.variable.username

    @username_flag.setter
    def username_flag(self, flag):
        self.variable.username = flag

    @property
    def password_flag(self):
        return self.variable.password

    @password_flag.setter
    def password_flag(self, flag):
        self.variable.password = flag

    @property
    def clean_session_flag(self):
        return self.variable.clean_session

    @clean_session_flag.setter
    def clean_session_flag(self, flag):
        self.variable.clean_session = flag

    @property
    def will_retain_flag(self):
        return self.variable.will_retain_flag

    @will_retain_flag.setter
    def will_retain_flag(self, flag):
        self.variable.will_retain_flag = flag

    @property
    def will_qos(self):
        return self.variable.will_qos

    @will_qos.setter
    def will_qos(self, flag):
        self.variable.will_qos = flag

    @property
    def will_flag(self):
        return self.variable.will_flag

    @will_flag.setter
    def will_flag(self, flag):
        self.variable.will_flag = flag

    @property
    def reserved_flag(self):
        return self.variable.reserved

    @reserved_flag.setter
    def reserved_flag(self, flag):
        self.variable.reserved = flag
    @property
    def id(self):
        return self.payload.id

    @id.setter
    def id(self, client_id):
        self.payload.id = client_id

    @property
    def will_topic(self):
        return self.payload.will_topic

    @will_topic.setter
    def will_topic(self, will_t):
        self.payload.will_topic = will_t

    @property
    def will_message(self):
        return self.payload.will_message

    @will_message.setter
    def will_message(self, will_mess):
        self.payload.will_message = will_mess

    @property
    def username(self):
        return self.payload.username

    @username.setter
    def username(self, un):
        self.payload.username = un

    @property
    def password(self):
        return self.payload.password

    @password.setter
    def password(self, passw):
        self.payload.password = passw

    @property
    def keep_alive(self):
        return self.variable_header.keep_alive

    @keep_alive.setter
    def keep_alive(self, k_alive):
        self.variable_header.keep_alive = k_alive

