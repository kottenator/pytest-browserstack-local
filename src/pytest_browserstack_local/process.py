import json
import os
import select
import signal
from subprocess import Popen, PIPE, TimeoutExpired
import time


EXPECTED_OUTPUT_MESSAGE = b'You can now access your local server(s) in our remote browser.\n'
TIMEOUT = 10  # in seconds
POLL_PERIOD = 1  # in seconds


def start_daemon(cmd):
    """
    Start BrowserStackLocal background process.

    When ``--daemon=start`` is passed, BrowserStackLocal returns a JSON with
    the following format (e.g.):

    .. code-block :: python

        {'state': 'connected', 'pid': 35246, 'message': 'Connected'}
    """
    print("Starting BrowserStackLocal daemon ...", flush=True)

    process = Popen(cmd, stdout=PIPE, stderr=PIPE)

    try:
        out, err = process.communicate(timeout=TIMEOUT)
    except TimeoutExpired:
        print("Error: timeout ({:d} sec).".format(TIMEOUT))
        stop_process(process.pid)
    else:
        if err:
            print("Error: " + err.decode().strip())
        elif out:
            print("Success: " + out.decode().strip())
            data = json.loads(out)
            return data


def start_process(cmd):
    """
    Start BrowserStackLocal foreground process.

    Monitor its output to find a specific text that indicates that the process has
    successfully established connection to BrowserStack server and ready to serve.

    Credits to https://stackoverflow.com/questions/10756383

    :param list[str] cmd:
    :rtype: subprocess.Popen | None
    """
    print("Starting BrowserStackLocal process ", end='', flush=True)

    process = Popen(cmd, stdout=PIPE)
    poll_obj = select.poll()
    poll_obj.register(process.stdout, select.POLLIN)
    connected = False
    start_time = time.time()

    while time.time() - start_time < TIMEOUT and not connected:
        poll_result = poll_obj.poll(0)

        if poll_result:
            line = process.stdout.readline()

            if b'*** Error: ' in line:
                print('\n' + line[line.index(b'Error:'):].decode().strip())
                break

            if line == EXPECTED_OUTPUT_MESSAGE:
                connected = True

        print('.', end='', flush=True)

        time.sleep(POLL_PERIOD)

    if connected:
        print(' Done.', flush=True)
        return process
    else:
        if time.time() - start_time >= TIMEOUT:
            print(' Timeout ({:d} sec).'.format(TIMEOUT), flush=True)
        print('Terminating the process ...', flush=True)
        stop_process(process.pid)


def stop_process(pid):
    """
    Terminate a process by sending SIGTERM to PID.

    :param pid:
    """
    os.kill(pid, signal.SIGTERM)
