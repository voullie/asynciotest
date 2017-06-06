import asyncio
import logging
import os
from commands import SERVER
import re

os.makedirs('./log', exist_ok=True)

FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('./log/asynciotest.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter(FORMAT)
fh.setFormatter(formatter)
logger.addHandler(fh)

async def handle_client(reader, writer):
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
    logger.debug("Client {} connected".format(addr))

    # for cmd in SERVER:
    #     requests = cmd['request']
    #     logger.debug("Sending ({}): {}".format(addr, str(requests)))
    #     writer.writelines([bytes(req, 'utf-8') for req in requests])
    #     await writer.drain()
    #     resp_regexs = cmd['responseRegex']
    #     for resp_regex in resp_regexs:
    #         logger.debug("Waiting ({}) for match for :{}".format(add, resp_regex))
    #         response = await reader.readline()
    #         response = response.decode()
    #         if re.match(resp_regex, response):
    #             logm = 'Received "{0}" from {1}'.format(response.strip(), addr)
    #             logger.debug(logm)
    #         else:
    #             logm = 'Received "{0}" from {1}'.format(response.strip(), addr)
    #             logger.error(logm)
    # logger.debug("Closing client socket ({})".format(addr))
    # writer.close()

    cmd = SERVER[0]
    request = cmd['request']
    logger.debug("Sending ({}): {}".format(addr, str(request)))
    writer.write(bytes('{}\n'.format(request), 'utf-8'))
    await writer.drain()
    resp_regex = cmd['responseRegex']
    logger.debug("Waiting ({}) for match for :{}".format(addr, resp_regex))
    response = await reader.readline()
    response = response.decode()
    logm = 'Received "{0}" from {1}'.format(response.strip(), addr)
    if re.match(resp_regex, response):
        logger.debug(logm)
    else:
        logger.error(logm)

    logger.debug("Closing client socket ({})".format(addr))
    writer.close()


loop = asyncio.get_event_loop()
loop.set_debug(True)
coro = asyncio.start_server(handle_client, '127.0.0.1', 56700, loop=loop)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed (or whaterver interrupt key sequence your shell is set for)
logger.debug('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass


# Close the server
logger.debug('Closing server on {}'.format(server.sockets[0].getsockname()))
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
