import os
import discord
import json
import asyncio
import random

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
plusEmoji = chr(0x2795)
minusEmoji = chr(0x2796)
dieEmoji = chr(0x1F3B2)
charm = '<:charm:548985823379324929>'
cool = '<:cool:548981332043366420>'
sharp = '<:sharp:548985524413530129>'
tough = '<:tough:548985524753268736>'
weird = '<:weird:548981465904578580>'
charmReaction = ':charm:548985823379324929'
coolReaction = ':cool:548981332043366420'
sharpReaction = ':sharp:548985524413530129'
toughReaction = ':tough:548985524753268736'
weirdReaction = ':weird:548981465904578580'
charmID = 548985823379324929
coolID = 548981332043366420
sharpID = 548985524413530129
toughID = 548985524753268736
weirdID = 548981465904578580
statEmoji = [charm, cool, sharp, tough, weird]

movesDirectory = './Moves/'


class MovesMessage:
	def __init__(self, user):
		self.moves = sorted([move.split('.')[0] for move in os.listdir(movesDirectory) if move.endswith('.move')])
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

class RollMessage:
	def __init__(self, user, character, arg=''):
		self.user = user
		self.character = character
		self.embed = discord.Embed()
		self.bonus = 0
		if(arg != ''):
			self.embed.title = 'Roll for {} - {}'.format(character['name'], arg)
		else:
			self.embed.title = 'Roll for {}'.format(character['name'])
		self.embed.description = 'Select a stat to roll with that stat, or select the die to roll with no stat.\nCurrent ongoing/forward bonus: {}'.format(self.bonus)
		self.message = None
		self.index = 0
		self.die1 = random.randint(1,6)
		self.die2 = random.randint(1,6)
		self.roll = self.die1 + self.die2 #2d6 for all rolls
		self.result = self.roll
		self.statName = ''
	async def Send(self, channel):
		self.message = await channel.send(embed=self.embed)
		await self.SetReactions()
	async def SetReactions(self):
		#emojis = list(self.message.guild.emojis) # Hooooooooly shit reactions are the dumbest fucking thing, I am so fucking mad right now
		await self.message.clear_reactions()
		self.embed.description = 'Select a stat to roll with that stat, or select the die to roll with no stat.\nCurrent ongoing/forward bonus: {}'.format(self.bonus)
		await self.message.edit(embed=self.embed)
		#await self.message.add_reaction(emojis[next(index for index,emoji in enumerate(emojis) if emoji.id==charmID)])
		#await self.message.add_reaction(emojis[next(index for index,emoji in enumerate(emojis) if emoji.id==coolID)])
		#await self.message.add_reaction(emojis[next(index for index,emoji in enumerate(emojis) if emoji.id==sharpID)])
		#await self.message.add_reaction(emojis[next(index for index,emoji in enumerate(emojis) if emoji.id==toughID)])
		#await self.message.add_reaction(emojis[next(index for index,emoji in enumerate(emojis) if emoji.id==weirdID)])
		await self.message.add_reaction(charmReaction)
		await self.message.add_reaction(coolReaction)
		await self.message.add_reaction(sharpReaction)
		await self.message.add_reaction(toughReaction)
		await self.message.add_reaction(weirdReaction)
		await self.message.add_reaction(plusEmoji)
		await self.message.add_reaction(minusEmoji)
		await self.message.add_reaction(dieEmoji)
		#self.embed.description = 'Select a stat to roll with that stat, or select the die to roll with no stat.\nCurrent ongoing/forward bonus: {}'.format(self.bonus)
		#await self.message.edit(embed=self.embed)
	async def Add(self):
		self.bonus += 1
		await self.SetReactions()
	async def Minus(self):
		self.bonus -= 1
		await self.SetReactions()
	async def OnStatPick(self, stat=None):
		if(stat):
			self.statName = str(stat).split(':')[1] # discord emoji follow the form <:NAME:ID>
			statValue = int(self.character[self.statName])
			self.result += statValue
		self.result += self.bonus
		await self.ReportResult()
	async def ReportResult(self):
		self.embed.description = "You rolled **{}**\n(({}+{}) + {} for stat {} + {} for ongoing/forward)".format(self.result, self.die1, self.die2, self.character[self.statName], self.statName, self.bonus)
		await self.message.edit(embed=self.embed)
		await self.message.clear_reactions()
