import time
import discord
import requests

from asyncio import sleep

bot_token = '<YOUR TOKEN HERE>'
target_channel = 0
threshold = 1000

client = discord.Client()


@client.event
async def on_ready():

    # Log in and set presence.
    print(f'Logged in as {client.user}.')
    await client.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name='Big Trades on Serum DEX'
        )
    )
    channel = client.get_channel(target_channel)
    last_time = time.time() * 1000

    # Start loop.
    while True:
        
        try:
            # Grab trades data from Serum API.
            data = requests.get(
                'https://serum-api.bonfida.com/trades/ROPEUSDC'
            ).json()['data']
            trades = [
                trade for trade in data
                if trade['time'] > last_time
                and trade['side'] == 'buy'
                and trade['size'] > threshold
            ]

            # Send new trades above threshold to Discord.
            if trades:
                last_time = max([int(trade['time']) for trade in trades])
                for trade in trades:
                    await channel.send(
                        f'🔥 **{trade["size"]}** ROPE bought at '
                        f'**{round(trade["price"], 2)}** USD on Serum DEX!'
                    )
                trades = []
            
        except Exception as e:
            # Catch all errors, print, and continue.
            print(f'Error: {e}.')
            
        finally:
            # Wait 10 seconds.
            await sleep(10)


client.run(bot_token, reconnect=True)
