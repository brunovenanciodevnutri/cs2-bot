import json
import discord
from discord import app_commands
from apikey import *
import asyncio
import requests

cor = 16758579
msg_id = None
msg_user = None

class csbot(discord.Client):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix='/', intents=intents, timeout=None)

        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

    async def on_ready(self):
        print(f'{self.user} EM EXECUÇÃO')

bot = csbot()

@bot.tree.command(name="stats", description='Show the player stats of a Counter-Strike 2.')
@app_commands.describe(steamid="Enter your steamID.")
async def stats(interaction: discord.interactions, steamid: str):
    try:
        embed = discord.Embed(
            title="🔍 Searching...",
            color=cor,
            description="")
        # COLETA DE DADOS CSGO2:
        request = requests.get(f'https://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v2/?appid=730&key=45FF1ED6AD5F43621103584263AA6C68&steamid={steamid}')
        status = json.loads(request.content)
        with open('data.json', 'w') as arquivo:
            json.dump(status, arquivo, indent=4)

        # COLETA DE DADOS STEAM:
        request2 = requests.get(f'https://www.steamwebapi.com/steam/api/profile?key=RM6FWUF94W7LDHNV&steam_id={steamid}')
        status2 = json.loads(request2.content)
        with open('dataprofile.json', 'w') as arquivo:
            json.dump(status2, arquivo, indent=4)
        
        await interaction.response.send_message('', embed=embed)
        # ENTREGA DE DADOS:
        with open('data.json', 'r') as arquivo:
            playerstats = json.load(arquivo)
        with open('dataprofile.json', 'r') as arquivo:
            playerprofile = json.load(arquivo)
            
            embed = discord.Embed(
            title=f"CS2 Stats of {playerprofile['personaname']}",
            color=cor,
            description=''
            )
        embed.set_author(name=playerprofile['personaname'], icon_url='https://cdn2.steamgriddb.com/icon/e1bd06c3f8089e7552aa0552cb387c92/32/512x512.png')
        embed.add_field(name='', value='', inline=False)

        total_hits = 0
        for item in playerstats['playerstats']['stats']:
            nome = item['name']
            valor = item['value']
            if 'total_hits_' in nome:
                total_hits += valor
            if nome == 'total_time_played':
                time_played = valor
            if nome == 'total_matches_played':
                total_matches_played = valor
            if nome == 'total_matches_won':
                total_matches_wons = valor
            if nome == 'total_kills':
                total_kills = valor
            if nome == 'total_deaths':
                total_deaths = valor
            if nome == 'total_planted_bombs':
                total_planted_bombs = valor
            if nome == 'total_defused_bombs':
                total_defused_bombs = valor
            if nome == 'total_kills_knife':
                kills_knife = valor
            if nome == 'total_kills_ak47':
                kills_ak47 = valor
            if nome == 'total_kills_m4a1':
                kills_m4a1 = valor
            if nome == 'total_kills_deagle':
                kills_deagle = valor
            if nome == 'total_kills_awp':
                kills_awp = valor
            if nome == 'total_kills_taser':
                kills_taser = valor
            if nome == 'total_kills_headshot':
                kills_headshot = valor
            for i in playerprofile['mostplayedgamestimes']:
                appid = i['appid']
                horas = i['hoursonrecord']
                if appid == 730:
                    total_time_played = horas
            if nome == 'GI.lesson.csgo_instr_explain_inspect':
                if kills_ak47 > kills_m4a1:
                    embed.set_thumbnail(url=playerprofile['avatarfull'])
                if kills_ak47 < kills_m4a1:
                    embed.set_thumbnail(url='https://static.wikia.nocookie.net/cswikia/images/b/ba/Ct-patch-small.png/revision/latest?cb=20220130164507')
                if kills_ak47 == kills_m4a1:
                    embed.set_thumbnail(url='')
                kd = total_kills / total_deaths
                hs_rate = (kills_headshot / total_hits) * 100
                total_matches_losses = total_matches_played - total_matches_wons
                win_rate = (total_matches_wons / total_matches_played) * 100
                
                embed.add_field(name='Time', value=f'{total_time_played}h')
                embed.add_field(name='', value='', inline=False)

                embed.add_field(name='HS Rate', value=f'{hs_rate:.2f}%')
                embed.add_field(name='', value='', inline=False)

                embed.add_field(name='Matches', value=f'```m\nWin Rate {win_rate:.2f} | Wins {total_matches_wons} | Losses {total_matches_losses}\n```')
                embed.add_field(name='', value='', inline=False)

                embed.add_field(name='Score', value=f'```m\nK/D {kd:.2f} | Kills {total_kills} | Deaths {total_deaths}\n```')
                embed.add_field(name='', value='', inline=False)

                embed.add_field(name='Bombs', value=f'```m\nPlanted {total_planted_bombs} | Defused {total_defused_bombs}\n```')
                embed.add_field(name='', value='', inline=False)

                embed.add_field(name='Weapons Kills', value=f'```m\nKnife {kills_knife} | Taser {kills_taser} | Deagle {kills_deagle}\nAK47 {kills_ak47} | M4A1 {kills_m4a1} | AWP {kills_awp}\n```')

                embed.set_footer(text='🛡️ Desenvolvido por Bruno Venâncio')

        
                await interaction.followup.send(f'{interaction.user.mention}', embed=embed)
    except (discord.app_commands.errors.CommandInvokeError, KeyError):
            embed = discord.Embed(
            title='ERROR',
            color=16711680,
            description='Your **Steam profile or game library is private**, please try again.\nTo use the /stats command you need:\n- Steam profile: **Public**\n- Game library: **Public**'
            )
            await interaction.followup.send(f'{interaction.user.mention}', embed=embed)
    except (discord.errors.NotFound, json.decoder.JSONDecodeError):
            embed = discord.Embed(
            title='ERROR',
            color=16711680,
            description='What you entered is **not** a steamID.\nPlease enter a **valid steamID**.'
            )
            await interaction.response.send_message(f'{interaction.user.mention}', embed=embed)

bot.run(bot_token)