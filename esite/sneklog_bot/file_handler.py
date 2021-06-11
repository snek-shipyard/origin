import datetime
import os
import time
from .download_from_url import get_size, time_formatter


async def progress(current, total, event, start):
    """Generic progress_callback for both
    upload.py and download.py"""
    now = time.time()
    diff = now - start
    if round(diff % 1.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion

        progress_str = f"""Yummy, Master gave sum juicy sound UwU
**Downloading : {"%.2f" % (percentage)}%
File Size:** {get_size(total)}
**Speed:** {get_size(speed)}/s
**Downloaded:** {get_size(current)}
**ETA:** {time_formatter(estimated_total_time)}
**TTC:** {time_formatter(time_to_completion) or "0s"}"""

        await event.edit(progress_str)


# SPDX-License-Identifier: (MIT)
# Copyright © 2021 snek.at

# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2021 snek.at
