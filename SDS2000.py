# *******************************************************************************
#  Copyright © 2023 Kerry S. Martin, martin@wild-wood.net
#  Free for usage without warranty, expressed or implied; attribution required
#
#  Filename   : SDS2000.py
#  Description:
#    Implements the SDS2000 oscilloscope instrument
#
#  Created    : 09/26/2023
#  Modified   : 09/26/2023
#  Author     : Kerry S. Martin, martin@wild-wood.net
# ******************************************************************************/

"""SDS2000 class: abstracted base class"""

from Oscilloscope import Oscilloscope as OS
from SocketInstrument import SocketInstrument
from InstrumentSettings import StringList
from HandlerClass import HandlerClass as HC
from ScaleShift import ScaleShift
import re

# TODO: error out if setting is made without connected instrument

class SDS2000(OS, SocketInstrument):

    # INSTRUMENT settings
    __MODES   = [ "YT" ]

    # CHANNEL settings
    __UNITS   = [ "V", "A" ]
    __ATTEN   = [ "10X", "1X", "0.1X" ]  # indexes __RANGE and __OFFSET
    __RANGE   = [ [ ("5M", 0.005), ("10M",0.01), ("20M",0.02), ("50M",0.05), ("100M",0.1), ("200M",0.2), ("500M",0.5), ("1",1.0), ("2",2.0), ("5",5.0), ("10",10.0), ("20",20.0), ("50",50.0), ("100",100.0) ],        # 10X
                  [ ("500U",0.0005), ("1M",0.001), ("2M",0.002), ("5M", 0.005), ("10M",0.01), ("20M",0.02), ("50M",0.05), ("100M",0.1), ("200M",0.2), ("500M",0.5), ("1",1.0), ("2",2.0), ("5",5.0), ("10",10.0) ],            # 1X
                  [ ("50U",50.0e-6), ("100U",0.0001), ("200",0.0002), ("500U",0.0005), ("1M",0.001), ("2M",0.002), ("5M", 0.005), ("10M",0.01), ("20M",0.02), ("50M",0.05), ("100M",0.1), ("200M",0.2), ("500M",0.5), ("1",1.0) ]  # 0.1X
                ]
    __OFFSET  = [ [ 0.0, -10.0, 10.0 ],     # 10X
                  [ 0.0, -10.0, 10.0 ],     # 1X
                  [ 0.0, -10.0, 10.0 ]      # 0.1X
                ]
    __BWL     = [ "FULL", "20M", "200M" ]
    __COUP    = [ "DC", "AC", "GND" ]

    # TIMEBASE settings
    __SCALE   = [ ("1N", 1.0e-9), ("2N", 2.0e-9), ("5N", 5.0e-9),
                  ("10N", 10.0e-9), ("20N", 20.0e-9), ("50N", 50.0e-9),
                  ("100N", 100.0e-9), ("200N", 200.0e-9), ("500N", 500.0e-9),
                  ("1U",1.0e-6), ("2U",2.0e-6), ("5U",5.0e-6),
                  ("10U", 10.0e-6), ("20U", 20.0e-6), ("50U", 50.0e-6),
                  ("100U", 100.0e-6), ("200U", 200.0e-6), ("500U", 500.0e-6),
                  ("1M", 1.0e-3), ("2M", 2.0e-3), ("5M", 5.0e-3),
                  ("10M", 10.0e-3), ("20M", 20.0e-3), ("50M", 50.0e-3),
                  ("100M", 100.0e-3), ("200M", 200.0e-3), ("500M", 500.0e-3),
                  ("1", 1.0), ("2", 2.0), ("5", 5.0),
                  ("10", 10.0), ("20", 20.0), ("50", 50.0),
                  ("100", 100.0), ("200", 200.0), ("500", 500.0),
                  ("1000", 1000.0) ]  # indexes __DELAY
    __DELAY   = [ [ 0.0, -100.0, 100.0 ], # TODO: scale dependent
                  [ 0.0, -100.0, 100.0 ],
                  [ 0.0, -100.0, 100.0 ],
                  [ 0.0, -100.0, 100.0 ],
                  [ 0.0, -100.0, 100.0 ],
                  [ 0.0, -100.0, 100.0 ],
                  [ 0.0, -100.0, 100.0 ],
                  [ 0.0, -100.0, 100.0 ],
                  [ 0.0, -100.0, 100.0 ],
                  [ 0.0, -100.0, 100.0 ],
                  [ 0.0, -100.0, 100.0 ],
                  [ 0.0, -100.0, 100.0 ],
                  [ 0.0, -100.0, 100.0 ],
                  [ 0.0, -100.0, 100.0 ],
                  [ 0.0, -100.0, 100.0 ],
                  [ 0.0, -100.0, 100.0 ],
                  [ 0.0, -100.0, 100.0 ],
                  [ 0.0, -100.0, 100.0 ],
                  [ 0.0, -100.0, 100.0 ],
                  [ 0.0, -100.0, 100.0 ],
                  [ 0.0, -100.0, 100.0 ],
                  [ 0.0, -100.0, 100.0 ],
                  [ 0.0, -100.0, 100.0 ],
                  [ 0.0, -100.0, 100.0 ],
                  [ 0.0, -100.0, 100.0 ],
                  [ 0.0, -100.0, 100.0 ],
                  [ 0.0, -100.0, 100.0 ],
                  [ 0.0, -100.0, 100.0 ],
                  [ 0.0, -100.0, 100.0 ],
                  [ 0.0, -100.0, 100.0 ],
                  [ 0.0, -100.0, 100.0 ],
                  [ 0.0, -100.0, 100.0 ],
                  [ 0.0, -100.0, 100.0 ],
                  [ 0.0, -100.0, 100.0 ],
                  [ 0.0, -100.0, 100.0 ],
                  [ 0.0, -100.0, 100.0 ],
                  [ 0.0, -100.0, 100.0 ]
                ]

    # TRIGGER settings
    __MODE    = [ "AUTO", "NORM", "SINGLE" ]
    __STATE   = [ "RUN", "STOP" ]
    __TYPE    = [ "EDGE" ]
    __SLOPE   = [ "RISING", "FALLING", "ALTERNATE" ]
    __TCOUP   = [ "DC", "AC", "LFREJECT", "HFREJECT" ]
    __TNREJ   = [ "OFF", "ON" ]

    __THRNG   = [[], [ 8.00e-9, 8.00e-9, 3.00e1 ], [[1, 1, 100000000]]]  # index: 0=off, 1=time, 2=events
    __TLEVEL  = [ 0.0, -4.1, 4.1 ]   # TODO: this is calculated (this value*vert_scale - vert_offset)


    def __init__(self):
        OS.__init__(self)
        SocketInstrument.__init__(self)
        self.__mode = StringList(SDS2000.__MODES)
        for i in range(1,4+1): # 1..4
            ch_name = f"CH{i}"
            ch = OS.Channel(
                ch_name, self,
                units=SDS2000.__UNITS,
                attens=SDS2000.__ATTEN,
                scales=SDS2000.__RANGE,
                offsets=SDS2000.__OFFSET,
                bandwidths=SDS2000.__BWL,
                couplings=SDS2000.__COUP
            )
            OS._add_channel(self, ch)
        channels = super().channels() + ["LINE"]
        OS._set_timebase(self, OS.Timebase(self, SDS2000.__SCALE, SDS2000.__DELAY))
        trig = OS.Trigger(
            self,
            sources=channels,
            types=SDS2000.__TYPE,
            polarities=SDS2000.__SLOPE,
            levels=SDS2000.__TLEVEL,
            couplings=SDS2000.__TCOUP,
            noise_rejects=SDS2000.__TNREJ
        )
        OS._set_trigger(self, trig)


    def attach(self, resource:str):
        is_attached = False
        if SocketInstrument.attach(self, resource):
            idn = SocketInstrument.query(self, "*IDN?")
            if (m := re.match(r"^(Siglent[^,]+),(SDS2[^,]+),([^,]+),([^,]+)$", idn, re.IGNORECASE)) is not None:
                mfg = m[1]
                model = m[2]
                sn = m[3]
                fw = m[4]
                self._set_info(mfg, model, sn, fw)
                is_attached = True
        if not is_attached:
            raise Exception("Unable to attach to SDS2000 series oscilloscope")


    def detach(self):
        SocketInstrument.detach(self)


    def run(self):
        self.write(":TRIG:RUN")


    def stop(self):
        self.write(":TRIG:STOP")

    @property
    def status(self):
        return self.query(":TRIG:STAT?")


    @property
    def is_attached(self):
        return SocketInstrument.get_attached_status(self)


    @property
    def modes(self):
        return self.__mode.criteria


    @property
    def mode(self):
        return self.__mode.value


    @mode.setter
    def mode(self, mode):
        self.__mode.value = mode
        self._handler(HC.os_mode, mode)


    # override SocketInstrument write
    def write(self, cmd:str, wait=True):
        super().write(cmd)
        if wait:
            self.is_operation_complete()


    def is_operation_complete(self):
        self.query("*OPC?")
        return super().is_operation_complete()


    def reset(self):
        self.write("*RST")
        super().reset()


    def measure_config(self, enable=None, lines=None, style=None):
        if style is not None:
            is_style_valid = False
            if isinstance(style, int):
                if style>=1 and style<=2:
                    is_style_valid = True
                pass
            elif isinstance(style, str):
                if (m := re.match(r"^[Mm]?([12])$", style)) is not None:
                    style = int(m[1])
                    is_style_valid = True

            if not is_style_valid:
                raise Exception("Invalid style")

            self.__handler_cmd(True, f":MEAS:ADV:STYL M{style}")

        if lines is not None:
            if isinstance(lines, int) and lines>=1 and lines<=12:
                self.__handler_cmd(True, f":MEAS:ADV:LIN {lines}")
            else:
                raise Exception("Invalid lines")

        if enable is not None:
            if isinstance(enable, bool):
                if enable:
                    self.__handler_cmd(True, ":MEAS ON")
                    self.__handler_cmd(True, ":MEAS:MODE ADV")   # only advanced mode is used for instrument control
                else:
                    self.__handler_cmd(True, ":MEAS OFF")
            else:
                raise Exception("Invalid enable")

    @staticmethod
    def __get_source(source):
        if source is None:
            return None
        if isinstance(source, int) and source>=1 and source<=4:
            return f"C{source}"
        #TODO: other sources as string
        return None

    def __is_valid_sources(s, s1, s2, invs2=False):
        b_s = s is not None
        b_s1 = s1 is not None
        b_s2 = s2 is not None
        if invs2:
            b_s2 = not b_s2
        return (b_s != b_s1) and b_s2


    def set_measure(self, line, type, source=None, source1=None, source2=None):
        if not isinstance(line, int) and line>=1 and line<=12:
            raise Exception("Invalid line")
        # TODO: validate type and determie if dual
        is_dual = False
        source = SDS2000.__get_source(source)
        source1 = SDS2000.__get_source(source1)
        source2 = SDS2000.__get_source(source2)
        if is_dual:
            if not SDS2000.__is_valid_sources(source, source1, source2):
                raise Exception("Invalid dual source measurement specified")
        else:
            if not SDS2000.__is_valid_sources(source, source1, source2, True):
                raise Exception("Invalid single source measurement specified")
        #TODO: left off here


    def get_measure(self, line):
        if not isinstance(line, int) and line>=1 and line<=12:
            raise Exception("Invalid line")
        return self.__handler_cmd(False, f":MEAS:ADV:P{line}:VAL?")


    def __process_holdoff(self, write, args):
        # args = holdoff
        if write:
            holdoff = args[0]
            if isinstance(holdoff, str):
                # check for LAST_TRIG|ACQ_START
                hu = holdoff.upper()
                if hu in ["LAST_TRIG", "ACQ_START"]:
                    return self.__handler_cmd(True, f":TRIG:EDGE:HST {hu}")
                elif hu in ["OFF", "TIME", "EVEN", "EVENTS"]:
                    return self.__handler_cmd(True, ":TRIG:EDGE:HOLD {hu}")
                else:
                    pass # TODO: convert to float or fail out here

            if holdoff is None:
                # turn holdoff off
                return self.__handler_cmd(True, ":TRIG:EDGE:HOLD OFF")
            elif isinstance(holdoff, int):
                # events holdoff
                holdtype = self.__handler_cmd(False, ":TRIG:EDGE:HOLD?")
                if holdtype != "EVENts":
                    self.__handler_cmd(True, ":TRIG:EDGE:HOLD EVEN")
                # TODO: range check on holdoff count
                return self.__handler_cmd(True, f":TRIG:EDGE:HLDEV {holdoff}")
            elif isinstance(holdoff, float):
                # TODO: range check on holdoff value
                holdtype = self.__handler_cmd(False, ":TRIG:EDGE:HOLD?")
                if holdtype != "TIME":
                    self.__handler_cmd(True, ":TRIG:EDGE:HOLD TIME")
                return self.__handler_cmd(True, f":TRIG:EDGE:HLDT", args=args, argn=0)
        else:
            holdtype = self.__handler_cmd(False, ":TRIG:EDGE:HOLD?")
            if holdtype == "EVENts":
                return self.__handler_cmd(False, f":TRIG:EDGE:HLDEV?")
            elif holdtype == "TIME":
                return self.__handler_cmd(False, f":TRIG:EDGE:HLDT?")
            else:
                return "OFF"


    def __handler_cmd(self, write, cmd, arg=None, args=None, argn=0):
        if write:
            # write - verbatim if no args provided
            if arg is None:
                if args is not None:
                    arg = args[argn]
            if arg is not None:
                self.write(f"{cmd} {arg}")
            else:
                self.write(cmd)
            return None
        else:
            # query - append ? if not already there, verbatim otherwise
            if not cmd.endswith("?"):
                cmd = cmd + "?"
            return self.query(cmd)


    def _handler(self, hclass:HC, write, *args):
        """_handler handles all changes to oscilloscope settings

        Args:
            hclass: str, one of several predefined handler classes ex/ "ch.unit"
            write: True if operation is a write; False if operation is a read
            args:  varies by the type of handler class

        Raises:
            Exception: _description_
        """
        if hclass==HC.os_mode:
            # args = mode
            pass
        elif hclass==HC.ch_state:
            # args = chnum, {ON|OFF}
            return self.__handler_cmd(write, f":CHAN{args[0]}:SWIT", args=args, argn=1)
        elif hclass==HC.ch_visible:
            # args = chnum, {ON|OFF}
            return self.__handler_cmd(write, f":CHAN{args[0]}:VIS", args=args, argn=1)
        elif hclass==HC.ch_unit:
            # args = chnum, {unit}
            return self.__handler_cmd(write, f":CHAN{args[0]}:UNIT", args=args, argn=1)
        elif hclass==HC.ch_scale:
            # args = chnum, scale
            return self.__handler_cmd(write, f":CHAN{args[0]}:SCAL", args=args, argn=1)
        elif hclass==HC.ch_offset:
            # args = chname, offset
            return self.__handler_cmd(write, f":CHAN{args[0]}:OFFS", args=args, argn=1)
        elif hclass==HC.ch_bw:
            # args = chname, bw
            return self.__handler_cmd(write, f":CHAN{args[0]}:BWL", args=args, argn=1)
        elif hclass==HC.ch_coupling:
            # args = chname, coupling
            return self.__handler_cmd(write, f":CHAN{args[0]}:COUP", args=args, argn=1)
        elif hclass==HC.ch_atten:
            # args = chname, atten
            if write: # special handling due to "VAL,"
                return self.__handler_cmd(True, f":CHAN{args[0]}:PROB VAL,", args=args, argn=1)
            else:
                return self.__handler_cmd(False, f":CHAN{args[0]}:PROB?")
        elif hclass==HC.time_scale:
            # args = timescale
            return self.__handler_cmd(write, ":TIM:SCAL", args=args, argn=0)
        elif hclass==HC.time_delay:
            # args = delay
            return self.__handler_cmd(write, ":TIM:DEL", args=args, argn=0)
        elif hclass==HC.trigger_mode:
            # args = mode
            return self.__handler_cmd(write, ":TRIG:MODE", args=args, argn=0)
        elif hclass==HC.trigger_type:
            # args = type
            return self.__handler_cmd(write, ":TRIG:TYPE", args=args, argn=0)
        elif hclass==HC.trigger_source:
            # args = source
            return self.__handler_cmd(write, ":TRIG:EDGE:SOUR", args=args, argn=0)
        elif hclass==HC.trigger_polarity:
            # args = polarity
            return self.__handler_cmd(write, ":TRIG:EDGE:SLOP", args=args, argn=0)
        elif hclass==HC.trigger_level:
            # args = level
            return self.__handler_cmd(write, ":TRIG:EDGE:LEV", args=args, argn=0)
        elif hclass==HC.trigger_coupling:
            # args = coupling
            return self.__handler_cmd(write, ":TRIG:EDGE:COUP", args=args, argn=0)
        elif hclass==HC.trigger_noise_reject:
            # args = noise_reject
            return self.__handler_cmd(write, ":TRIG:EDGE:NREJ", args=args, argn=0)
        elif hclass==HC.trigger_holdoff:
            # args = holdoff
            return self.__process_holdoff(write, args)
        elif hclass==HC.trigger_holdoffs:
            # no action here, just provide the list of holdoff options
            return ["OFF", "LAST_TRIG", "ACQ_START", "TIME", "EVENTS", (1,100000000), (8.00E-09, 3.00E+01)]
        else:
            raise Exception("Unhandled handler")


if __name__ == "__main__":
    # Test code
    oscope = SDS2000()
    #oscope.start_log("C:\\Projects\\Python\\FResp\\log\\Fresp.log")
    oscope.attach("192.168.0.211:5025")
    if oscope.is_attached:
        oscope.reset()
        oscope.mode = "YT"
        oscope.channel(1).state = "ON"
        oscope.channel(1).visible = "ON"
        oscope.channel(1).coupling = "DC"
        oscope.channel(1).unit = "V"
        oscope.channel(1).scale = 0.2
        oscope.channel(1).scale = ScaleShift.DOWN
        print(oscope.channel(1).scale)
        oscope.channel(1).offset = 0.5
        print(oscope.channel(1).offset)
        oscope.channel(1).bandwidth = "FULL"

        oscope.time.scale = "2u"
        oscope.time.scale = ScaleShift.UP_DECADE

        oscope.stop()
        print(oscope.status)
        oscope.trigger.source = "CH1"
        oscope.trigger.type = "EDGE"
        oscope.trigger.polarity = "RISING"
        oscope.trigger.level = 2.5
        oscope.trigger.holdoff = 10.0e-6
        print(oscope.trigger.holdoff)
        print(oscope.trigger.holdoffs)
        oscope.measure_config(lines=4, style="M2", enable=True)
        oscope.run()
        print(oscope.status)

        print(oscope.model)
    else:
        print("Did not attach to oscope")

    oscope.close_log()


# ******************************************************************************
#  Copyright © 2023 Kerry S. Martin, martin@wild-wood.net
#  Free for usage without warranty, expressed or implied; attribution required
# ******************************************************************************