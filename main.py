import asyncio
from pyrogram import Client
import dotenv
import os

dotenv.load_dotenv()
bridges_bot_tag = 'GetBridgesBot'

# place ur api_id and api_hash here
my_api_id = int(os.getenv(key='API_ID'))
my_api_hash = os.getenv(key='API_HASH')
torrc_directory = os.getenv(key='TORRC_PATH')  # ur torrc path

client = Client(name='tor_bridges_refresher', api_id=my_api_id, api_hash=my_api_hash)


async def get_last_bridges():
    async for message in client.get_chat_history(bridges_bot_tag, limit=1):
        return message.text.split('\n')


async def main():
    await client.send_message(bridges_bot_tag, 'Bridges')
    await asyncio.sleep(5)
    bridges = await get_last_bridges()
    await client.stop()
    with open(torrc_directory, 'r') as f:
        data = f.readlines()
    for num, bridge in enumerate(bridges):
        data[num + 3] = 'Bridge ' + bridge + '\n'
    with open(torrc_directory, 'w') as f:
        for x in data:
            f.write(x)


with client:
    client.loop.run_until_complete(main())
