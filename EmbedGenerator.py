import discord
from discord.ext import commands
import os
import json
import asyncio

checkEmoji = chr(0x2705)
xEmoji = chr(0x274c)

def GenerateEmbed(name):
	if(name+'.json' in os.listdir('./Embed Data/')):
		dataFile = open('./Embed Data/{}.json'.format(name))
		data = json.load(dataFile)
		dataFile.close()
		# json doesn't support hexadecimal because they are FOOLS so we have to convert ourselves
		#data['color'] = int(data['color'], 0)
		embed = discord.Embed.from_data(data)
		return embed
	else:
		embed = discord.Embed()
		embed.description = "File ./Embed Data/{}.json not found. Valid Files:\n```{}```".format(name, [embedFile for embedFile in os.listdir('./Embed Data/') if embedFile.endswith('.json')])
		return embed


class EmbedGenerator:
	def __init__(self, ctx, filename='', author='', title='', color='', description='', thumbnail='', image=''):
		self.ctx = ctx
		self.filename = filename
		self.author = author
		self.title = title
		if(color != ''):
			self.color = int(color,0)
		else:
			self.color = 0
		self.description = description
		self.image = image
		self.embed = discord.Embed()
		self.embed.set_author(name=self.author)
		self.embed.title = self.title
		self.embed.color = self.color
		self.embed.description = self.description
		if(thumbnail != ''):
			self.embed.set_thumbnail(url=thumbnail)
		if(image != ''):
			self.embed.set_image(url=image)
		self.message = None
	async def Send(self, ctx):
		self.message = await ctx.send("This is your embed! React with {} to save with name {}!".format(checkEmoji, self.filename), embed=self.embed)
		await self.message.add_reaction(checkEmoji)
	async def Save(self):
		dataFile = open('./Embed Data/{}.json'.format(self.filename), 'w')
		json.dump(self.embed.to_dict(), dataFile)
		dataFile.close()
		await self.message.edit(content="Embed {} saved!".format(self.filename))