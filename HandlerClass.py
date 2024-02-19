# *******************************************************************************
#  Copyright © 2023 Kerry S. Martin, martin@wild-wood.net
#  Free for usage without warranty, expressed or implied; attribution required
#
#  Filename   : HandlerClass.py
#  Description:
#    Enumeration of different reasons for calling the oscilloscope _handler()
#    callback function
#
#  Created    : 09/26/2023
#  Modified   : 09/26/2023
#  Author     : Kerry S. Martin, martin@wild-wood.net
# ******************************************************************************/

"""Enumeration of different oscilloscope _handler() callback classes"""

from enum import Enum

HandlerClass = Enum('HandlerClass',
               [
                'os_mode',
                'ch_state',
                'ch_visible',
                'ch_unit',
                'ch_scale',
                'ch_offset',
                'ch_bw',
                'ch_coupling',
                'ch_atten',
                'time_scale',
                'time_delay',
                'trigger_mode',
                'trigger_source',
                'trigger_type',
                'trigger_polarity',
                'trigger_level',
                'trigger_coupling',
                'trigger_noise_reject',
                'trigger_holdoff',
                'trigger_holdoffs'
               ])


# ******************************************************************************
#  Copyright © 2023 Kerry S. Martin, martin@wild-wood.net
#  Free for usage without warranty, expressed or implied; attribution required
# ******************************************************************************