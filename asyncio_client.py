import sys
import asyncio
from commands import CLIENT

async def connect_to_server(loop, client_id):
    client_id = str(client_id)
    reader, writer = await asyncio.open_connection('127.0.0.1', 56700, loop=loop)
    data = await reader.readline()
    remoteRequest = data.decode().strip()
    print('Received: {}'.format(remoteRequest))
    print(CLIENT['remoteRequest'])
    if remoteRequest == CLIENT['remoteRequest']:
        response = CLIENT['responseTemplate'].format(client_id)
        print('Send: {}'.format(response))
        writer.write(response.encode())
    writer.close()


try:
    client_nr = int(sys.argv[1])
except:

    client_nr = 1

print('Setting up {} clients'.format(client_nr))
loop = asyncio.get_event_loop()
work = []
for client_id in range(1, client_nr + 1):
    future = asyncio.ensure_future(connect_to_server(loop, client_id))
    work.append(future)

loop.run_until_complete(asyncio.gather(*work))
loop.close()
