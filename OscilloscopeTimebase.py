# *******************************************************************************
#  Copyright © 2023 Kerry S. Martin, martin@wild-wood.net
#  Free for usage without warranty, expressed or implied; attribution required
#
#  Filename   : OscilloscopeTimebase.py
#  Description:
#    Implements a container for all oscilloscope time-base settings
#
#  Created    : 09/26/2023
#  Modified   : 09/26/2023
#  Author     : Kerry S. Martin, martin@wild-wood.net
# ******************************************************************************/

from InstrumentSettings import IndexedFloatRange, FloatStringList
from HandlerClass import HandlerClass as HC
from ScaleShift import ScaleShift as SCALE


class Timebase:
    def __init__(self, owner, scales, delays):
        self._owner = owner
        self.__set_scales(scales)
        self.__set_delays(delays)


    def __set_scales(self, scales):
        self._scale = FloatStringList(scales)


    def __set_delays(self, delays):
        self._delay = IndexedFloatRange(delays)


    @property
    def scales(self):
        return self._scale.criteria


    @property
    def scale(self):
        self._scale.value = self._owner._handler_read(HC.time_scale)
        return self._scale.value


    @scale.setter
    def scale(self, scale):
        self._scale.value = scale
        self._owner._handler_write(HC.time_scale, self._scale.value)


    @property
    def delays(self):
        return self._delay.criteria

    @property
    def delay(self):
        self._delay.value = self._owner._handler_read(HC.time_delay)
        return self._delay.value

    @delay.setter
    def delay(self, delay):
        self._delay.value = delay
        self._owner._handler_write(HC.time_delay, self._delay.value)


# ******************************************************************************
#  Copyright © 2023 Kerry S. Martin, martin@wild-wood.net
#  Free for usage without warranty, expressed or implied; attribution required
# ******************************************************************************