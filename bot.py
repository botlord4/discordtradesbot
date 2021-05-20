import discord
import asyncio
from urllib.request import Request,urlopen
import json
import datetime

botToken = 'bot_token'
threshold = 500

lastTime = 0

client = discord.Client()

async def getTrades():
  req = Request('https://serum-api.bonfida.com/trades/ROPEUSDC',headers={'User-Agent': 'Mozilla/5.0'})
  webpage = json.loads(urlopen(req).read().decode())
  newTrades = webpage["data"]
  newTrades = [trade for trade in newTrades if trade["time"] > lastTime and trade['side'] == 'buy' and trade['price']*trade['size']> threshold]
  global lastTime
  lastTime = webpage["data"][0]["time"]
  return newTrades

async def post(posts):
  if (not posts):
    return
  print('posting')
  while(True):
    try:
      channel = client.get_channel(828317684826505286) # testing channel, to be removed
      for post in posts:
        message = '🔥  Big Trade Alert! ' + str(post['size']) + " ROPE @ " + str(round(post['price'],2)) + " 'BUY' " + datetime.datetime.fromtimestamp(post['time']/1000).strftime('%c')
        await channel.send(message)
      print('posted')
      break
    except Exception as e:
      print(e)
      await asyncio.sleep(10)
      continue

async def main():
  while(True):
    try:
      await getTrades() 
      break
    except Exception as e:
      print(e)
      await asyncio.sleep(5)
  while True:
      await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Big Trades | Serum Dex"))
      try:
        newTrades = await getTrades()
        print(lastTime)
        print(newTrades)
        await post(newTrades)
      except Exception as e:
        print(e)
        await asyncio.sleep(20)
        continue
      await asyncio.sleep(10)


@client.event
async def on_ready():
    print('logged in as {0.user}'.format(client))
    await main()

client.run(botToken,  reconnect = True)
