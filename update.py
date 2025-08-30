Run python update.py
  python update.py
  shell: /usr/bin/bash -e {0}
  env:
    pythonLocation: /opt/hostedtoolcache/Python/3.10.18/x64
    PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.10.18/x64/lib/pkgconfig
    Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.10.18/x64
    Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.10.18/x64
    Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.10.18/x64
    LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.10.18/x64/lib
    TELEGRAM_API_ID: ***
    TELEGRAM_API_HASH: ***
    TELEGRAM_CHANNEL: SpotilifeIPAs
    GITHUB_TOKEN: ***
Traceback (most recent call last):
  File "/home/runner/work/altstore-spotilife/altstore-spotilife/update.py", line 70, in <module>
    with client:
  File "/opt/hostedtoolcache/Python/3.10.18/x64/lib/python3.10/site-packages/telethon/helpers.py", line 219, in _sync_enter
    return loop.run_until_complete(self.__aenter__())
  File "/opt/hostedtoolcache/Python/3.10.18/x64/lib/python3.10/asyncio/base_events.py", line 649, in run_until_complete
    return future.result()
  File "/opt/hostedtoolcache/Python/3.10.18/x64/lib/python3.10/site-packages/telethon/client/auth.py", line 669, in __aenter__
    return await self.start()
  File "/opt/hostedtoolcache/Python/3.10.18/x64/lib/python3.10/site-packages/telethon/client/auth.py", line 167, in _start
    value = phone()
  File "/opt/hostedtoolcache/Python/3.10.18/x64/lib/python3.10/site-packages/telethon/client/auth.py", line 22, in <lambda>
    phone: typing.Union[typing.Callable[[], str], str] = lambda: input('Please enter your phone (or bot token): '),
EOFError: EOF when reading a line
/home/runner/work/_temp/dac6d2f2-af35-420e-a5d8-be6060a112de.sh: line 1:  2255 Segmentation fault      (core dumped) python update.py
Please enter your phone (or bot token): 
Error: Process completed with exit code 139.
