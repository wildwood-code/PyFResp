# *******************************************************************************
#  Copyright © 2023 Kerry S. Martin, martin@wild-wood.net
#  Free for usage without warranty, expressed or implied; attribution required
#
#  Filename   : Oscilloscope.py
#  Description:
#    Implements the Oscilloscope abstracted base class which serves as the base
#    class for oscilloscope instruments
#
#  Created    : 09/26/2023
#  Modified   : 09/26/2023
#  Author     : Kerry S. Martin, martin@wild-wood.net
# ******************************************************************************/

"""Oscilloscope class: abstracted base class for an oscilloscope instrument"""

from abc import ABC, abstractmethod
import re
from Instrument import Instrument
import OscilloscopeChannel
import OscilloscopeTimebase
import OscilloscopeTrigger
from HandlerClass import HandlerClass as HC


class Oscilloscope(Instrument, ABC):
    """Oscilloscope class: implements an abstracted oscilloscope interface
    """

    class Channel(OscilloscopeChannel.Channel):
        def __init__(self, name, owner, units, attens, scales, offsets, bandwidths, couplings):
            super().__init__(name, owner, units, attens, scales, offsets, bandwidths, couplings)


    class Timebase(OscilloscopeTimebase.Timebase):
        def __init__(self, owner, scales, delay):
            super().__init__(owner, scales, delay)


    class Trigger(OscilloscopeTrigger.Trigger):
        def __init__(self, owner, sources, types, polarities, levels, couplings, noise_rejects):
            super().__init__(owner, sources, types, polarities, levels, couplings, noise_rejects)


    def __init__(self):
        Instrument.__init__(self)
        self.__channels = []
        self.__timebase = None
        self.__trigger = None


    def _add_channel(self, channel):
        """Allows the derived oscilloscope to build up a channel set

        Args:
            channel: initialized Channel object to add to the set
        """
        self.__channels.append(channel)


    def __find_channel(self, name:str|int) -> int|None:
        """Get the index of a channel number (1-N) or string 'CH3'

        Args:
            name: integer channel number (1-N) or string ex/ 'CH3'

        Returns:
            0-based index if it exists, or None if it does not exist
        """
        if isinstance(name, int):
            if name >= 1 and name <= len(self.__channels):
                # 1-based channel number is in range
                return name-1
            else:
                # out of range
                return None
        elif isinstance(name, str):
            # valid forms: "1", "C1", "CH1", "CHAN1", "CHANNEL1"
            if (m := re.search(r"^(?:CH?|CHAN(?:NEL)?)?([0-9]+)$", name, re.IGNORECASE)) is not None:
                n = int(m.group(1))-1
                if n >= 1 and n <= len(self.__channels):
                    # 1-based channel number is in range
                    return n
                else:
                    # out of range
                    return None
            else:
                # invalid channel form
                return None
        else:
            # invalid type
            return None


    def _set_timebase(self, timebase):
        """Allows the derived oscilloscope to set the timebase spec

        Args:
            timebase: initialized Timebase object
        """
        self.__timebase = timebase


    def _set_trigger(self, trigger):
        """Allows the derived oscilloscope to set the trigger spec

        Args:
            trigger: initialized Trigger object
        """
        self.__trigger = trigger


    def channel(self, ch:str|int):
        """Access one of the channels, allowing channel params to be read/set

        Args:
            ch: Channel identifier: integer 1-N or string "C1", "CH1", etc

        Returns:
            Reference to the channel object. Getter/setter methods may be used
            to read/change the channel parameters
        """
        index = self.__find_channel(ch)
        if index is not None:
            return self.__channels[index]


    def channels(self):
        """Returns a list of all of the channel names
        """
        return [ c.name for c in self.__channels]

    def num_channels(self):
        """Returns the number of channels in the oscilloscope
        """
        return len(self.__channels)


    @abstractmethod
    def is_operation_complete(self):
        return super().is_operation_complete()


    @abstractmethod
    def reset(self):
        # refresh all of the settings for channel, timebase, and trigger
        Nch = len(self.__channels)
        for i in range(Nch):
            _ = self.__channels[i].state
            _ = self.__channels[i].visible
            _ = self.__channels[i].unit
            _ = self.__channels[i].scale
            _ = self.__channels[i].offset
            _ = self.__channels[i].bandwidth
            _ = self.__channels[i].coupling
            # TODO: atten
            _ = self.is_operation_complete()
        # TODO: timebase and trigger, etc.

        super().reset()

    @property
    def timebase(self):
        """Reference to the timebase object. Getter/setter methods may be used
        to read/change the timebase parameters
        """
        return self.__timebase


    @property
    def time(self):
        """Alternate reference to the timebase object
        """
        return self.__timebase


    @property
    def trigger(self):
        """Reference to the trigger object. Getter/setter methods may be used
        to read/change the trigger parameters
        """
        return self.__trigger


    @property
    @abstractmethod
    def mode(self):
        """Abstract method to get the current oscilloscope mode
        """
        pass


    @mode.setter
    @abstractmethod
    def mode(self, mode):
        """Abstract method to set the current oscilloscope mode
        """
        pass


    @property
    @abstractmethod
    def modes(self):
        """Abstract method to get the available oscilloscope modes
        """
        pass


    @abstractmethod
    def _handler(self, hclass:HC, write:bool, *args):
        """Abstract callback method used to cause action on the oscilloscope
        in response to changed parameters

        Args:
            hclass: callback handler class (HandlerClass enumeration)
            write: True for write operation; False for read operation
            args:   varies depending upon the hclass
        """
        pass


    @abstractmethod
    def run(self):
        pass


    @abstractmethod
    def stop(self):
        pass


    @property
    @abstractmethod
    def status(self):
        pass


    def _handler_write(self, hclass:HC, *args):
        return self._handler(hclass, True, *args)


    def _handler_read(self, hclass:HC, *args):
        return self._handler(hclass, False, *args)


# ******************************************************************************
#  Copyright © 2023 Kerry S. Martin, martin@wild-wood.net
#  Free for usage without warranty, expressed or implied; attribution required
# ******************************************************************************