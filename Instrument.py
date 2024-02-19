# *******************************************************************************
#  Copyright © 2023 Kerry S. Martin, martin@wild-wood.net
#  Free for usage without warranty, expressed or implied; attribution required
#
#  Filename   : Instrument.py
#  Description:
#    Implements the abstracted Instrument base class which serves as the base
#    class for all test instruments
#
#  Created    : 09/26/2023
#  Modified   : 09/26/2023
#  Author     : Kerry S. Martin, martin@wild-wood.net
# ******************************************************************************/

"""Instrument class: abstracted base class"""

from abc import ABC, abstractmethod


class Instrument(ABC):
    """Instrument class: implements an abstracted, generic instrument
    """

    def __init__(self):
        self._mfg = None
        self._model = None
        self._sn = None
        self._fw = None


    def _set_info(self, mfg:str=None, model:str=None, sernum:str=None, firmware:str=None):
        """Used by the derived instrument class to set standard info

        Args:
            mfg: instrument manufacturer string
            model: instrument model string
            sernum: instrument serial number string
            firmware: instrument firmware revision string
        """
        if mfg is not None:
            self._mfg = mfg
        if model is not None:
            self._model = model
        if sernum is not None:
            self._sernum = sernum
        if firmware is not None:
            self._firmware = firmware


    @property
    def manufacturer(self):
        """Returns the manufacturer name of the instrument (str)
        """
        return self._mfg


    @property
    def model(self):
        """Returns the model name/number of the instrument (str)
        """
        return self._model


    @property
    def sernum(self):
        """Returns the serial number of the instrument (str)
        """
        return self._sernum


    @property
    def firmware(self):
        """Returns the firmware revision of the instrument (str)
        """
        return self._firmware


    @property
    @abstractmethod
    def is_attached(self):
        """Check to see if object is attached to an instrument (bool)
        """
        return False


    @abstractmethod
    def attach(self, resource:str):
        """Attach the object to the instrument by resource name
        """
        pass


    @abstractmethod
    def detach(self):
        """Detach the object from the instrument
        """
        pass


    @abstractmethod
    def is_operation_complete(self):
        """Wait until operation is complete
        """
        return True

    @abstractmethod
    def reset(self):
        """Reset the instrument to a known state
        """
        pass


# ******************************************************************************
#  Copyright © 2023 Kerry S. Martin, martin@wild-wood.net
#  Free for usage without warranty, expressed or implied; attribution required
# ******************************************************************************