# *******************************************************************************
#  Copyright © 2023 Kerry S. Martin, martin@wild-wood.net
#  Free for usage without warranty, expressed or implied; attribution required
#
#  Filename   : OscilloscopeTrigger.py
#  Description:
#    Implements a container for all oscilloscope trigger settings
#
#  Created    : 09/26/2023
#  Modified   : 09/26/2023
#  Author     : Kerry S. Martin, martin@wild-wood.net
# ******************************************************************************/

from InstrumentSettings import StringList, FloatRange, IndexedFloatRange
from HandlerClass import HandlerClass as HC


class Trigger:
    """Class to hold the settings controlling the triggering of the oscope

    This class is instantiated by the Oscilloscope-specific class. During
    construction, the setting options and initial values are specified.

    Configured setting options:
    sources = string list of options
    types = string list of options
    polarities = string list of options
    levels = range list [default min max]
    couplings = string list of options
    noise_rejects = string list of options
    holdoffs = range list [default min max]
    """
    def __init__(self, owner, sources, types, polarities, levels, couplings, noise_rejects):
        self._owner = owner
        self.__set_sources(sources)
        self.__set_types(types)
        self.__set_polarities(polarities)
        self.__set_levels(levels)
        self.__set_couplings(couplings)
        self.__set_noise_rejects(noise_rejects)


    def __set_sources(self, sources):
        self._source = StringList(sources)


    def __set_types(self, types):
        self._type = StringList(types)


    def __set_polarities(self, polarities):
        self._polarity = StringList(polarities)


    def __set_levels(self, levels):
        self._level = FloatRange(levels)


    def __set_couplings(self, couplings):
        self._coupling = StringList(couplings)


    def __set_noise_rejects(self, noise_rejects):
        self._noise_reject = StringList(noise_rejects)


    @property
    def holdoffs(self):
        # holdoffs is handled entirely within the implementing class
        return self._owner._handler_read(HC.trigger_holdoffs)


    @property
    def holdoff(self):
        # holdoff is handled entirely within the implementing class
        return self._owner._handler_read(HC.trigger_holdoff)


    @holdoff.setter
    def holdoff(self, holdoff):
        # holdoff is handled entirely within the implementing class
        self._owner._handler_write(HC.trigger_holdoff, holdoff)


    @property
    def noise_rejects(self):
        return self._noise_reject.criteria


    @property
    def noise_reject(self):
        return self._noise_reject.value


    @noise_reject.setter
    def noise_reject(self, noise_reject):
        self._noise_reject.value = noise_reject
        self._owner._handler_write(HC.trigger_noise_reject, self._noise_reject.value)


    @property
    def couplings(self):
        return self._coupling.criteria


    @property
    def coupling(self):
        return self._coupling.value


    @coupling.setter
    def coupling(self, coupling):
        self._coupling.value = coupling
        self._owner._handler_write(HC.trigger_coupling, self._coupling.value)


    @property
    def sources(self):
        return self._source.criteria


    @property
    def source(self):
        return self._source.value


    @source.setter
    def source(self, source):
        self._source.value = source
        self._owner._handler_write(HC.trigger_source, self._source.value)


    @property
    def types(self):
        return self._type.criteria


    @property
    def type(self):
        return self._type.value


    @type.setter
    def type(self, type):
        self._type.value = type
        self._owner._handler_write(HC.trigger_type, self._type.value)


    @property
    def polarities(self):
        return self._polarity.criteria


    @property
    def polarity(self):
        return self._polarity.value


    @polarity.setter
    def polarity(self, polarity):
        self._polarity.value = polarity
        self._owner._handler_write(HC.trigger_polarity, self._polarity.value)


    @property
    def levels(self):
        return self._level.criteria


    @property
    def level(self):
        return self._level.value


    @level.setter
    def level(self, level):
        self._level.value = level
        self._owner._handler_write(HC.trigger_level, self._level.value)


# ******************************************************************************
#  Copyright © 2023 Kerry S. Martin, martin@wild-wood.net
#  Free for usage without warranty, expressed or implied; attribution required
# ******************************************************************************