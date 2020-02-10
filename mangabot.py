# mangabot.py
# Author: hkpani
# Description: This is a bot that listens to the discord server and outputs a user recommended manga or anime from MAL.
# As of version 1.0 this tool only supports format of manga and anime from the source site myanimelist.com
# Even if the exact title is not found, the Jikan API will return the top result from the search
##################################################
# User input format : $MALrec <media type> <title>
# For Anime: $MALrec a <title>
# For Manga: $MALrec m <title>
##################################################
# Output format below:
##################################################
# Title:
# Genre:
# Rating:
# Summary:
# URL:
##################################################
import os

import discord
import random
from dotenv import load_dotenv
from discord.ext import commands
from jikanpy import Jikan

#this method loads variables defined in .env file of the same directory
#User must define their DISCORD_TOKEN for the bot and DISCORD_GUILD name 
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
bot = commands.Bot(command_prefix = '$')
jikan = Jikan()

client = discord.Client()

@bot.command(name='MALrec',help='This command will print a formatted manga/anime rec in the recommendations channel. Format: MALrec <a/m> <name>')
async def recommend(ctx,media_type,media_name):
	if media_type.lower() == 'a':
		#search with jikan API for anime
		media = 'anime'
		search = jikan.search(search_type="anime",query=media_name,parameters ={'limit': 1}) #only gets the first result
	elif media_type.lower() == 'm':
		media = 'manga'
		#ssearch with jikan API for manga
		search = jikan.search(search_type="manga",query=media_name,parameters ={'limit': 1}) #only gets the first result
	else:
		await ctx.send('Invalid format for the command')

	guild = ctx.guild
	mal_channel = discord.utils.get(guild.channels,name='recommendations')

	if not mal_channel: #create channel if the channel was not found
		await guild.create_text_channel('recommendations')
		mal_channel = discord.utils.get(guild.channels,name='recommendations')

	#if the channel is still not found, there was a problem creating the channel
	if mal_channel:
		channel_found = True
	else:
		channel_found = False

	#Jikan API results come back as a dictionary
	resultDict = search['results']

	#print out the information in the necessary format	
	if resultDict[0]['mal_id']: #this is a check to see if any elements were found from the API results
		if channel_found:
			await mal_channel.send('Title: {} \nMedia: {}\n'.format(resultDict[0]['title'],resultDict[0]['type']))
			if media == 'anime':
				await mal_channel.send("Completed: Yes") if not resultDict[0]['airing'] else await ctx.send("Completed: No")
			else:
				await mal_channel.send("Completed: Yes") if not resultDict[0]['publishing'] else await ctx.send("Completed: No")
			await mal_channel.send('Rating: {}\nSummary: {}\nURL: {}'.format(resultDict[0]['score'],resultDict[0]['synopsis'],resultDict[0]['url']))
		else:
			await ctx.send('There was an error finding or creating the recommendations channel')
	else:
		await ctx.send('No search results found, try again')

if __name__ == "__main__":
	bot.run(TOKEN)