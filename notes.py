import os
import discord
import json
import asyncio
import csv

arrowLeft = chr(0x2B05)
arrowRight = chr(0x27A1)
questionMark = '\u2754'

notesDirectory = './Character Stuff/Notes/'


class NotesMessage:
	def __init__(self, user, characterName):
		notesFile = open(notesDirectory+characterName+'.csv', 'r')
		reader = csv.reader(notesFile)
		self.notes = []
		for row in reader:
			self.notes += row
		notesFile.close()
		self.embed = discord.Embed()
		self.message = None
		self.index = 0
		self.user = user
		self.showingHelp = False
		self.characterName = characterName
	async def Advance(self):
		self.showingHelp = False
		self.index += 1
		if(self.index+1 > len(self.notes)):
			self.index = 0
		await self.Edit()
	async def Back(self):
		self.showingHelp = False
		self.index -= 1
		if(self.index < 0):
			self.index = len(self.notes)-1
		await self.Edit()
	async def GoToNumber(self, number):
		self.showingHelp = False
		self.index = number-1
		await self.Edit()
	async def Edit(self):
		self.showingHelp = False
		note = self.notes[self.index]
		self.embed.title = 'Note {}/{} - {}'.format(self.index+1, len(self.notes), self.characterName)
		self.embed.description = note
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
	async def ShowHelp(self):
		if(not self.showingHelp):
			self.embed.title = 'Notes Help'
			self.embed.description = 'Shows notes added with the addnote command. Only the user who created this message can interact with it.\nUse left/right arrows to scroll through, or type \'$notes <x>\' where <x> is a number to skip there.\nPress ? again to go back to notes.'
			await self.message.edit(embed=self.embed)
			await self.message.clear_reactions()
			await self.message.add_reaction(questionMark)
			self.showingHelp = True
		else:
			await self.Edit()
			self.showingHelp = False