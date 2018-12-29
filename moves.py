import os
import discord
import json
import asyncio

arrowLeft = chr(0x2B05)
arrowRight = chr(0x27A1)
listEmoji = chr(0x1f4dc)
questionMark = '\u2754'
emojiNumbers = ['0\u20e3',
				'1\u20e3',
				'2\u20e3',
				'3\u20e3',
				'4\u20e3',
				'5\u20e3',
				'6\u20e3',
				'7\u20e3',
				'8\u20e3',
				'9\u20e3']

movesDirectory = './Moves/'


class MovesMessage:
	def __init__(self, user):
		self.moves = [move.split('.')[0] for move in os.listdir(movesDirectory) if move.endswith('.move')]
		self.embed = discord.Embed()
		self.message = None
		self.index = 0
		self.user = user
		self.overflowMessages = []
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
	async def GoToNumber(self, number):
		self.index = emojiNumbers.index(number)
		await self.Edit()
	async def Edit(self, details=False, listing=False):
		for message in self.overflowMessages:
			await message.delete()
		self.overflowMessages = []
		if(not listing):
			move = self.moves[self.index]
			if(details):
				fileType = '.details'
			else:
				fileType = '.move'
			dataFile = open(movesDirectory + move + fileType)
			#data = dataFile.read()[:2000]
			data = dataFile.read()
			dataFile.close()
			self.embed.title = self.moves[self.index]
			self.embed.description = data[:2000]
			await self.message.edit(embed=self.embed)
			await self.SetReactions()
			if(len(data) > 2000):
				number = 2000
				while(number < len(data)):
					lastNumber = number
					number += 2000
					newEmbed = discord.Embed()
					newEmbed.description = data[lastNumber:number]
					self.overflowMessages.append(await self.message.channel.send(embed=newEmbed))
		else:
			await self.message.edit(embed=self.embed)
			await self.SetListReactions()
	async def Send(self, channel):
		self.message = await channel.send(embed=self.embed)
		await self.Edit()
	async def SetReactions(self):
		await self.message.clear_reactions()
		await self.message.add_reaction(arrowLeft)
		await self.message.add_reaction(arrowRight)
		await self.message.add_reaction(questionMark)
		await self.message.add_reaction(listEmoji)
	async def SetListReactions(self):
		await self.message.clear_reactions()
		for index in range(len(self.moves)):
			await self.message.add_reaction(emojiNumbers[index])
	async def ShowDetails(self):
		await self.Edit(details=True)
	async def ListMoves(self):
		self.embed = discord.Embed()
		self.embed.title = "Basic Hunter Moves"
		self.embed.description = '\n'.join(['{}: {}'.format(index, self.moves[index]) for index in range(len(self.moves))])
		await self.Edit(listing=True)
