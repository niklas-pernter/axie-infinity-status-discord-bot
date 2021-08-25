import discord
from discord.ext import commands
import requests
import json

TOKEN = 'your bot token comes here'

client = commands.Bot(command_prefix='!', help_command=None)

@client.event
async def on_ready():
    print('\n We are logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="!server"))

@client.command()
async def server(ctx):
    response = requests.get('https://axie.zone:3000/server_status', verify=False)
    json_data = repsonse_to_string(json.loads(response.text))

    embed=discord.Embed(title="Axie Infinity Server Status")
    embed.add_field(name="**Maintenance**", value=json_data['status_maintenance'], inline=False)
    embed.add_field(name="**Battle Server**", value=json_data['status_battles'], inline=False)
    embed.add_field(name="**Game API Server**", value=json_data['status_graphql'], inline=False)
    embed.add_field(name="**Marketplace**", value=json_data['status_cloudflare'], inline=False)
    embed.set_footer(text="Powered by Alpha Bots")

    await ctx.send(embed=embed)

def repsonse_to_string(response):
    data = {}
    data['status_maintenance'] = ':green_circle: No Maintenance' if not response['status_maintenance'] else ':red_circle: Maintenance undergoing'
    data['status_battles'] = get_battle_status(response['status_battles'])
    data['status_graphql'] = ':green_circle: Game servers OK' if response['status_graphql'] else ':red_circle: Game servers Offline'
    data['status_cloudflare'] = ':green_circle: Marketplace OK' if response['status_cloudflare'] else ':red_circle: Marketplace Offline'
    return data

def get_battle_status(status):
    if(status == 0): return ':green_circle: Battle servers OK'
    if(status == 1): return ':yellow_circle: Battle servers running with restrictions'
    if(status == 2):  return ':red_circle: Battle servers offline'
    else: return ':black_circle: Undefined Status'

client.run(TOKEN)
