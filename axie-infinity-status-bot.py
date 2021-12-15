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
    """function to format the response to a good looking output in discord chat
    
    args:
        response(dict): a dictionary of the response
        
        schema:
        {
            "status_maintenance": boolean,  # maintenance undergoing if true
            "status_battles": int,          # -1 ok, 0 running with restrictions, 1 offline
            "status_graphql": boolean,      # online if true 
            "status_cloudflare": boolean    # online if true 
        }
        
    returns:
        data (dict): formatted dictionary for output

    """
    data = {}
    data['status_maintenance'] = ':green_circle: No Maintenance' if not response['status_maintenance'] else ':red_circle: Maintenance undergoing'
    data['status_battles'] = get_battle_status(response['status_battles'])
    data['status_graphql'] = ':green_circle: Game servers OK' if response['status_graphql'] else ':red_circle: Game servers Offline'
    data['status_cloudflare'] = ':green_circle: Marketplace OK' if response['status_cloudflare'] else ':red_circle: Marketplace Offline'
    return data

def get_battle_status(status):
    """function to create a message from the statuscode
    
    args:
        status(int): the current battlestatus of the response.
        
    returns 
        (str): the formatted string for output.
    
    """
    if(status == -1): return ':green_circle: Battle servers OK'
    if(status == 0): return ':yellow_circle: Battle servers running with restrictions'
    if(status == 1):  return ':red_circle: Battle servers offline'
    else: return ':black_circle: Undefined Status'

client.run(TOKEN)
