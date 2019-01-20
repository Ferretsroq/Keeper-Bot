import discord
import os
import json

def GenerateEmbed(directory, name):
	if(name+'.json' in os.listdir('./Embed Data/' + directory)):
		dataFile = open('./Embed Data/{}/{}.json'.format(directory, name))
		data = json.load(dataFile)
		dataFile.close()
		# json doesn't support hexadecimal because they are FOOLS so we have to convert ourselves
		data['color'] = int(data['color'], 0)
		embed = discord.Embed.from_data(data)
		return embed
	else:
		embed = discord.Embed()
		embed.description = "File ./Embed Data/{}/{}.json not found".format(directory, name)
		return embed