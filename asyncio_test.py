import asyncio
import logging
import os
from test_commands import TEST_COMMANDS

os.makedirs('./log', exist_ok=True)

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('./log/asynciotest.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter(FORMAT)
fh.setFormatter(formatter)
logger.addHandler(fh)

async def handle_echo(reader, writer):

    # data = await reader.read(160)
    # message = data.decode()
    # addr = writer.get_extra_info('peername')
    # logm = 'Received "{0}" from {1}'.format(message.strip(), addr)
    # logger.debug(logm)
    # 
    # logger.debug("Sending ({}): {}".format(addr, message.strip()))
    # writer.write(data)
    # await writer.drain()
    #
    # print("Closing client socket ({})".format(addr))
    # writer.close()

    addr = writer.get_extra_info('peername')
    for cmd in TEST_COMMANDS:
        message = cmd
        logger.debug("Sending ({}): {}".format(addr, message.strip()))
        writer.write(data)
        await writer.drain()


loop = asyncio.get_event_loop()
coro = asyncio.start_server(handle_echo, '127.0.0.1', 56700, loop=loop)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
logger.debug('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
