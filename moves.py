import os
import discord
import json
import asyncio

arrowLeft = chr(0x2B05)
arrowRight = chr(0x27A1)
listEmoji = chr(0x1f4dc)
questionMark = '\u2754'

movesDirectory = './Moves/'


class MovesMessage:
	def __init__(self, user):
		self.moves = [move.split('.')[0] for move in os.listdir(movesDirectory) if move.endswith('.move')]
		self.embed = discord.Embed()
		self.message = None
		self.index = 0
		self.user = user
	async def Advance(self):
		self.index += 1
		if(self.index+1 > len(self.moves)):
			self.index = 0
		await self.Edit()
	async def Back(self):
		self.index -= 1
		if(self.index < 0):
			self.index = len(self.moves)-1
		await self.Edit()
	async def Edit(self, details=False):
		move = self.moves[self.index]
		if(details):
			fileType = '.details'
		else:
			fileType = '.move'
		dataFile = open(movesDirectory + move + fileType)
		data = dataFile.read()[:2000]
		dataFile.close()
		self.embed.title = self.moves[self.index]
		self.embed.description = data
		await self.message.edit(embed=self.embed)
		await self.SetReactions()
	async def Send(self, channel):
		self.message = await channel.send(embed=self.embed)
		await self.Edit()
	async def SetReactions(self):
		await self.message.clear_reactions()
		await self.message.add_reaction(arrowLeft)
		await self.message.add_reaction(arrowRight)
		await self.message.add_reaction(questionMark)
	async def ShowDetails(self):
		await self.Edit(details=True)