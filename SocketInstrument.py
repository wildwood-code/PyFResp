# *******************************************************************************
#  Copyright © 2023 Kerry S. Martin, martin@wild-wood.net
#  Free for usage without warranty, expressed or implied; attribution required
#
#  Filename   : SocketInstrument.py
#  Description:
#    Implements the SocketInstrument class, from which an IP socket
#    instrument, generally test equipment using SCPI protocol, can be
#    implemented.
#
#  Created    : 08/20/2023
#  Modified   : 08/20/2023
#  Author     : Kerry S. Martin, martin@wild-wood.net
# ******************************************************************************/

"""SocketInstrument class: IP socket based instrument control class"""

import socket
import time
import re

# static initialization class decorator
def static_init(cls):
    if getattr(cls, "static_init", None):
        cls.static_init()
    return cls

@static_init
class SocketInstrument:
    """SocketInstrument class - SCPI over IP socket
    """

    @classmethod
    def static_init(cls):
        cls.__RECV_BUFLEN:int = 256
        cls.__num_instr_attached = 0
        #if not cls.__init_sockets():
        #    raise Exception("Unable to initialize sockets")


    def __init__(self):
        """SocketInstrument constructor
        """
        self.__connected_socket = None
        self.__connected_resource = None
        self.__FH_LOG_FILE = None


    def __del__(self):
        """SocketInstrument destructor
        """
        self.detach()
        self.close_log()


    def start_log(self, filename):
        """Open a logfile to capture all writes and reads
        """
        if self.__FH_LOG_FILE is None:
            try:
                self.__FH_LOG_FILE = open(filename, "w")
            except:
                self.__FH_LOG_FILE = None

        if self.__FH_LOG_FILE is not None:
            self.__write_log(r"[[LOG STARTED]]")


    def close_log(self):
        """Close an existing logfile
        """
        if self.__FH_LOG_FILE is not None:
            self.__write_log(r"[[LOG ENDED]]")
            self.__FH_LOG_FILE.close()
            self.__FH_LOG_FILE = None


    def __write_log(self, line):
        """Write to an existing logfile or ignore if logfile not opened
        """
        if self.__FH_LOG_FILE is not None:
            self.__FH_LOG_FILE.write(line)
            self.__FH_LOG_FILE.write("\n")


    def attach(self, resource:str) -> bool:
        """Attach a resource to the SocketInstrument

        Args:
            resource: IP address and port, ex/ "192.168.0.197:5025"

        Returns:
            True if successful, False otherwise
        """
        result = False
        if self.__connected_socket is not None:
            self.detach()

        if (addr_port := SocketInstrument._extract_addr_port(resource)) is not None:
            self.__connected_socket = socket.socket()
            if self.__connected_socket is not None:
                try:
                    self.__connected_socket.connect(addr_port)
                    SocketInstrument.__num_instr_attached += 1
                    self.__connected_resource = resource
                    self.__write_log(f"{resource} attached")
                    result = True
                except:
                    self.__write_log(f"{resource} failed to attach")
                    # result = False is already the default
            else:
                self.__write_log(f"{self.__connected_resource} already attached, did not attach {resource}")
        else:
            self.__write_log(f"{resource} invalid")

        return result


    def detach(self) -> bool:
        """Detach a resource from the SocketInstrument

        Returns:
            True if successful, False otherwise
        """
        result = False
        if self.__connected_socket is not None:
            try:
                self.__connected_socket.shutdown()
                self.__connected_socket.close()
                self.__connected_socket = None
                SocketInstrument.__num_instr_attached -= 1
                self.__write_log(f"{self.__connected_resource} detached")
                result = True
            except:
                self.__write_log(f"{self.__connected_resource} failed to detach")
                # result = False is already the default

        return result


    def get_attached_status(self):
        if self.__connected_socket is not None:
            return True
        else:
            return False


    def write(self, cmd:str) -> bool:
        """Write an SCPI command to a SocketInstrument, append newline if needed

        Args:
            cmd: SCPI command, ex/ "*IDN?" (newline appended automatically)

        Returns:
            True if successful, False otherwise
        """
        if not cmd.endswith("\n"):
            cmd = cmd + "\n"
        cmd_bytes = bytes(cmd, "utf-8")
        return self.writeex(cmd_bytes)


    def writeex(self, cmd_bytes:bytes) -> bool:
        """Write an SCPI command to a SocketInstrument exactly as provided

        Args:
            cmd_bytes: SCPI command or data, 'bytes' object, ex/ b"*IDN?\n"

        Returns:
            True if successful, False otherwise
        """
        result = False
        if self.__connected_socket is not None:
            if self.__connected_socket.send(cmd_bytes) == len(cmd_bytes):
                result = True

        cmd = cmd_bytes.decode()
        if cmd.endswith("\n"):
            cmd = cmd.rstrip()
        if result:
            self.__write_log(f"{self.__connected_resource} SEND SUCCESS : {cmd}")
        else:
            self.__write_log(f"{self.__connected_resource} SEND FAILED : {cmd}")

        return result


    def query(self, cmd:str, delay_ms:int=0) -> str|None:
        """Write an SCPI command to a SocketInstrument and read the response

        Args:
            cmd: SCPI command, ex/ "*IDN?" (newline appended automatically)
            delay_ms: Optional delay in ms. Defaults to 0 (no delay added).

        Returns:
            Response as a string
        """
        resp = None

        if not cmd.endswith("\n"):
            cmd = cmd + "\n"
        cmd_bytes = bytes(cmd, "utf-8")
        if (resp := self.queryex(cmd_bytes, delay_ms)) is not None:
            resp = resp.decode()
            if resp.endswith("\n"):
                resp = resp.rstrip() # remove the trailing newline

        return resp


    def queryex(self, cmd_bytes:bytes, delay_ms:int=0) -> bytes|None:
        """Write an SCPI command to a SocketInstrument and read the response

        Args:
            cmd_bytes: SCPI command or data, 'bytes' object, ex/ b"*IDN?\n"
            delay_ms: Optional delay in ms. Defaults to 0 (no delay added).

        Returns:
            Response as a 'bytes' object
        """
        resp_bytes = None
        if self.writeex(cmd_bytes):
            if delay_ms>0:
                time.sleep(delay_ms/1000.0)
            resp_bytes = self.__connected_socket.recv(SocketInstrument.__RECV_BUFLEN)

        if resp_bytes is not None:
            resp = resp_bytes.decode()
            if resp.endswith("\n"):
                resp = resp.rstrip()
            self.__write_log(f"{self.__connected_resource} RECV SUCCESS : {resp}")
        else:
            self.__write_log(f"{self.__connected_resource} RECV FAILED")

        return resp_bytes


    @staticmethod
    def _extract_addr_port(resource:str) -> tuple:
        """Extract the address and port from the resource spec

        Args:
            resource: resource spec ex/ "192.168.0.197:5025"

        Returns:
            Tuple with address str and port int:  (addr, port)
        """
        result = (None, None)
        m = re.search(r"^(?:[a-zA-Z]+://)?([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}):([0-9]{1,5})/?$", resource)
        if m is not None:
            result = (m.group(1), int(m.group(2)))
        return result


# ******************************************************************************
#  Copyright © 2023 Kerry S. Martin, martin@wild-wood.net
#  Free for usage without warranty, expressed or implied; attribution required
# ******************************************************************************