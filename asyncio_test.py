import asyncio
import logging
import os
from test_commands import TEST_COMMANDS
import re

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
        requests = cmd['request']
        logger.debug("Sending ({}): {}".format(addr, str(requests)))
        # for data in requests:
        #     writer.write(data)
        #     await writer.drain()
        writer.writelines([bytes(req, 'utf-8') for req in requests])
        await writer.drain()

        resp_regexs = cmd['responseRegex']
        for resp_regex in resp_regexs:
            response = await reader.readline()
            response = response.decode()
            if re.match(resp_regex, response):
                logm = 'Received "{0}" from {1}'.format(response.strip(), addr)
                logger.debug(logm)
            else:
                logm = 'Received "{0}" from {1}'.format(response.strip(), addr)
                logger.error(logm)

    print("Closing client socket ({})".format(addr))
    writer.close()


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
