# *******************************************************************************
#  Copyright © 2023 Kerry S. Martin, martin@wild-wood.net
#  Free for usage without warranty, expressed or implied; attribution required
#
#  Filename   : OscilloscopeChannel.py
#  Description:
#    Implements a container for all oscilloscope channel settings
#
#  Created    : 09/26/2023
#  Modified   : 09/26/2023
#  Author     : Kerry S. Martin, martin@wild-wood.net
# ******************************************************************************/

from InstrumentSettings import StringList, IndexedFloatStringList, IndexedFloatRange
from HandlerClass import HandlerClass as HC
from ScaleShift import ScaleShift
import re

class Channel:

    def __init__(self, name, owner, units, attens, scales, offsets, bandwidths, couplings):
        # there is no sanity checking here, which will always be called
        # from an Oscilloscope-derived constructor... let's assume that
        # they know what they are doing

        self._name = name     # name/ID provided to _handler_write()
        self._owner = owner   # Oscilloscope class, we will call ._handler_write()

        if (m := re.search(r"(\d+)$", name)) is not None:
            self._num = int(m[1])
        else:
            self._num = None

        # set the valid lists and initial values
        self.__set_units(units)
        self.__set_scales(scales)
        self.__set_offsets(offsets)
        self.__set_bandwidths(bandwidths)
        self.__set_couplings(couplings)
        self.__set_attens(attens)
        self._state = StringList(["OFF", "ON"])    # defaults to off
        self._visible = StringList(["ON", "OFF"])  # defaults to visible


    def __set_units(self, units):
        self._unit = StringList(units)


    def __set_attens(self, attens):
        self._atten = StringList(attens)


    def __set_scales(self, scales):
        self._scale = IndexedFloatStringList(scales)


    def __set_offsets(self, offsets):
        self._offset = IndexedFloatRange(offsets)


    def __set_bandwidths(self, bandwidths):
        self._bandwidth = StringList(bandwidths)


    def __set_couplings(self, couplings):
        self._coupling = StringList(couplings)


    @property
    def name(self):
        return self._name

    @property
    def num(self):
        return self._num


    @property
    def state(self):
        self._state.value = self._owner._handler_read(HC.ch_state, self._num)
        return self._state.value


    @state.setter
    def state(self, state):
        self._state.value = state
        self._owner._handler_write(HC.ch_state, self._num, self._state.value)

    @property
    def visible(self):
        self._visible.value = self._owner._handler_read(HC.ch_visible, self._num)
        return self._visible.value


    @state.setter
    def visible(self, visible):
        self._visible.value = visible
        self._owner._handler_write(HC.ch_visible, self._num, self._visible.value)


    @property
    def units(self):
        return self._unit.criteria


    @property
    def unit(self):
        self._unit.value = self._owner._handler_read(HC.ch_unit, self._num)
        return self._unit.value


    @unit.setter
    def unit(self, unit:str):
        self._unit.value = unit
        self._owner._handler_write(HC.ch_unit, self._num, self._unit.value)


    @property
    def scales(self):
        return self._scale.criteria


    @property
    def scale(self):
        self._scale.value = self._owner._handler_read(HC.ch_scale, self._num)
        return self._scale.value


    @scale.setter
    def scale(self, scale):
        self._scale.value = scale
        self._owner._handler_write(HC.ch_scale, self._num, self._scale.value)


    @property
    def offsets(self):
        return self._offset.criteria


    @property
    def offset(self):
        self._offset.value = float(self._owner._handler_read(HC.ch_offset, self._num))
        return self._offset.value


    @offset.setter
    def offset(self, offset):
        self._offset.value = offset
        self._owner._handler_write(HC.ch_offset, self._num, self._offset.value)


    @property
    def bandwidths(self):
        return self._bandwidth.criteria


    @property
    def bandwidth(self):
        self._bandwidth.value = self._owner._handler_read(HC.ch_bw, self._num)
        return self._bandwidth.value


    @bandwidth.setter
    def bandwidth(self, bandwidth):
        self._bandwidth.value = bandwidth
        self._owner._handler_write(HC.ch_bw, self._num, self._bandwidth.value)


    @property
    def couplings(self):
        return self._coupling.criteria


    @property
    def coupling(self):
        self._coupling.value = self._owner._handler_read(HC.ch_coupling, self._num)
        return self._coupling.value


    @coupling.setter
    def coupling(self, coupling):
        self._coupling.value = coupling
        self._owner._handler_write(HC.ch_coupling, self._num, self._coupling.value)


    @property
    def attens(self):
        return self._atten.criteria


    @property
    def atten(self):
        return self._atten.value


    @atten.setter
    def atten(self, atten):
        self._atten.value = atten
        self._owner._handler_write(HC.ch_atten, self._num, self._atten.value)


# ******************************************************************************
#  Copyright © 2023 Kerry S. Martin, martin@wild-wood.net
#  Free for usage without warranty, expressed or implied; attribution required
# ******************************************************************************