import discord
from discord.ext import commands
import requests
import json

TOKEN = 'ODY5OTUzODE5MzY5NDMxMDQw.YQFtoQ.M-FDpqfploHfmKem6RmgnNb3gdo'

client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print('\n We are logged in as {0.user}'.format(client))


@client.command()
async def status(ctx):
    response = requests.get('https://axie.zone:3000/server_status', verify=False)
    json_data = repsonse_to_string(json.loads(response.text))

    embed=discord.Embed(title="Axie Infinity Server Status")
    embed.add_field(name="Maintenance", value=json_data['status_maintenance'], inline=False)
    embed.add_field(name="Battle Server", value=json_data['status_battles'], inline=False)
    embed.add_field(name="Game API Server ", value=json_data['status_graphql'], inline=False)
    embed.add_field(name="Marketplace", value=json_data['status_cloudflare'], inline=False)
    embed.set_footer(text="Powered by Alpha Bots")
    
    await ctx.send(embed=embed)

def repsonse_to_string(response):
    data = {}
    data['status_maintenance'] = ':green_circle: No Maintenance' if not response['status_maintenance'] else ':red_circle: Maintenance undergoing'
    data['status_battles'] = ':green_circle: Battle servers OK' if response['status_battles'] == 0 else ':red_circle: Battle servers Offline or running with restrictions'
    data['status_graphql'] = ':green_circle: Game servers OK' if response['status_graphql'] else ':red_circle: Game servers Offline'
    data['status_cloudflare'] = ':green_circle: Marketplace OK' if response['status_cloudflare'] else ':red_circle: Marketplace Offline'
    return data

client.run(TOKEN)