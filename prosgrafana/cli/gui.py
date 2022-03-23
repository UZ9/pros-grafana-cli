import click
import signal
import time

from pros.cli.common import default_options, logger, project_option, pros_root, shadow_command, resolve_v5_port
import logging

from ..gui_data.gui_application import GUITerminal
from pros.serial.devices.vex import V5UserDevice
from pros.serial.ports import DirectPort
from pros.common.ui.log import PROSLogHandler, PROSLogFormatter

@click.command()
def gui():
    """
    Transfers GUI data from the robot to the computer
    """

    # Use same logging system as PROS
    ctx_obj = {}
    click_handler = PROSLogHandler(ctx_obj=ctx_obj)
    ctx_obj['click_handler'] = click_handler
    formatter = PROSLogFormatter('%(levelname)s - %(name)s:%(funcName)s - %(message)s', ctx_obj)
    click_handler.setFormatter(formatter)
    logging.basicConfig(level=logging.INFO, handlers=[click_handler])

    logger(__name__).info("Starting C# GUI Application...")

    # Wait for GUI to launch
    logger(__name__).info("Application successfully started, waiting for connection")

    logger(__name__).debug(f"Finding port...")

    port = DirectPort(resolve_v5_port(None, 'user')[0])
    device = V5UserDevice(port)
    app = GUITerminal(device)

    logger(__name__).info(f"Attempting to receive data...")

    signal.signal(signal.SIGINT, app.stop)
    app.start()

    while not app.alive.is_set():
        time.sleep(0.005)
    app.join()
    logger(__name__).info("Shutting down terminal...")
