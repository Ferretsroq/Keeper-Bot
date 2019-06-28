import discord
from discord.ext import commands
import characters
import moves, notes, EmbedGenerator
import os, csv
import random
import asyncio

TOKEN = open('token.token').read()

bot = commands.Bot(command_prefix='$', case_insensitive=True)

bot.moveMessage = None
bot.activeGame = 'Playtest3Characters'

bot.playbookMessages = {'Chosen': None,
						'Crooked': None,
						'Divine': None,
						'Expert': None,
						'Flake': None,
						'Initiate': None,
						'Monstrous': None,
						'Mundane': None,
						'Professional': None,
						'Spell-Slinger': None,
						'Spooky': None,
						'Wronged': None,
						'Dominic': None,
						'Reinard': None,
						'Naomi': None}
bot.playerCharacters = [('Dominic', characters.Chosen), ('Reinard', characters.Flake), ('Naomi', characters.Expert), ('Kyrie', characters.Divine), ('Ben', characters.SpellSlinger)]
bot.noteMessages = []
bot.players = {133328216466259968: 'Dominic',
			   111529517541036032: 'Spooky',
			   448613063713751042: 'Reinard',
			   449619391005327361: 'Naomi',
			   330869232810196992: 'Kyrie',
			   222370387596410881: 'Ben'}
#bot.characters = characters.LoadAllCharacters(bot.playerCharacters)
bot.characters = characters.LoadAllCharactersFromJSON(bot.playerCharacters, bot.activeGame)
bot.rollMessages = {}
bot.embedGenerator = None

@bot.command()
@commands.is_owner()
async def allcharacters(ctx):
	'''Sends all 12 character messages at once for debugging purposes'''
	data, fields = characters.LoadCharacter('Chosen')
	bot.playbookMessages['Chosen'] = characters.ChosenMessage(characters.Chosen(data, fields), ctx.author)
	await bot.playbookMessages['Chosen'].Send(ctx)
	data, fields = characters.LoadCharacter('Crooked')
	bot.playbookMessages['Crooked'] = characters.CrookedMessage(characters.Crooked(data, fields), ctx.author)
	await bot.playbookMessages['Crooked'].Send(ctx)

	data, fields = characters.LoadCharacter('Divine')
	bot.playbookMessages['Divine'] = characters.DivineMessage(characters.Divine(data, fields), ctx.author)
	await bot.playbookMessages['Divine'].Send(ctx)
	data, fields = characters.LoadCharacter('Expert')
	bot.playbookMessages['Expert'] = characters.ExpertMessage(characters.Expert(data, fields), ctx.author)
	await bot.playbookMessages['Expert'].Send(ctx)
	data, fields = characters.LoadCharacter('Flake')
	bot.playbookMessages['Flake'] = characters.FlakeMessage(characters.Flake(data, fields), ctx.author)
	await bot.playbookMessages['Flake'].Send(ctx)
	data, fields = characters.LoadCharacter('Initiate')
	bot.playbookMessages['Initiate'] = characters.InitiateMessage(characters.Initiate(data, fields), ctx.author)
	await bot.playbookMessages['Initiate'].Send(ctx)
	data, fields = characters.LoadCharacter('Monstrous')
	bot.playbookMessages['Monstrous'] = characters.MonstrousMessage(characters.Monstrous(data, fields), ctx.author)
	await bot.playbookMessages['Monstrous'].Send(ctx)
	data, fields = characters.LoadCharacter('Mundane')
	bot.playbookMessages['Mundane'] = characters.MundaneMessage(characters.Mundane(data, fields), ctx.author)
	await bot.playbookMessages['Mundane'].Send(ctx)
	data, fields = characters.LoadCharacter('Professional')
	bot.playbookMessages['Professional'] = characters.ProfessionalMessage(characters.Professional(data, fields), ctx.author)
	await bot.playbookMessages['Professional'].Send(ctx)
	data, fields = characters.LoadCharacter('Spell-Slinger')
	bot.playbookMessages['Spell-Slinger'] = characters.SpellSlingerMessage(characters.SpellSlinger(data, fields), ctx.author)
	await bot.playbookMessages['Spell-Slinger'].Send(ctx)
	data, fields = characters.LoadCharacter('Spooky')
	bot.playbookMessages['Spooky'] = characters.SpookyMessage(characters.Spooky(data, fields), ctx.author)
	await bot.playbookMessages['Spooky'].Send(ctx)
	data, fields = characters.LoadCharacter('Wronged')
	bot.playbookMessages['Wronged'] = characters.WrongedMessage(characters.Wronged(data, fields), ctx.author)
	await bot.playbookMessages['Wronged'].Send(ctx)

@bot.command()
async def test(ctx):#, *, arg):
	#await ctx.send('You said {}'.format(arg))
	await ctx.invoke(chosen)
	#await chosen(ctx)
	#await bot.chosen(ctx)

@bot.command()
async def char(ctx, name=''):
	if(name.title() in bot.characters):
		character = bot.characters[name.title()]
		bot.playbookMessages[name.title()] = character.playbookMessage(character, ctx.author)
		await bot.playbookMessages[name.title()].Send(ctx)
	else:
		validCharacters = '\n'.join([character.title() for character in list(bot.characters.keys())])
		text = "Character {} not found. Valid characters:\n```\n{}```".format(name.title(), validCharacters)
		await ctx.send(text)

@bot.command()
@commands.is_owner()
async def loadcharacter(ctx, name='', directory='Demo Characters', playbook='Chosen'):
	path = './Character Stuff/{}/'.format(directory)
	data, fields = characters.LoadCharacter(playbook=playbook.title(), sheetPath=path, name=name.title())
	character = characters.PlaybookByName(playbook.title())(data, fields, alias=name.title())
	character.Save(bot.activeGame)
	bot.characters = characters.LoadAllCharactersFromJSON(bot.playerCharacters, bot.activeGame)


@bot.command(name='moves')
async def move(ctx):
	'''Lists all of the basic hunter moves. Left/Right arrows to scroll. Question Mark shows additional details. List lists all of the basic moves.'''
	bot.moveMessage = moves.MovesMessage(ctx.author)
	await bot.moveMessage.Send(ctx.channel)

@bot.command()
async def additem(ctx, *, arg):
	'''Add an item to the inventory of your character.'''
	if(ctx.author.id in bot.players):
		characterName = bot.players[ctx.author.id]
		if(characterName+'.csv' in os.listdir('./Character Stuff/Inventories')):
			inventoryFile = open('./Character Stuff/Inventories/'+characterName+'.csv', 'a')
			writer = csv.writer(inventoryFile)
			writer.writerow([arg])
			inventoryFile.close()
			await ctx.send('Added item `{}` to `{}`'.format(arg, characterName))
		else:
			await ctx.send('Character `{}` inventory not found.'.format(characterName))
	else:
		await ctx.send('No character found for user id `{}`'.format(ctx.author.id))

@bot.command()
async def addnote(ctx, *, arg):
	'''Add a note to the notes of your character.'''
	if(ctx.author.id in bot.players):
		characterName = bot.players[ctx.author.id]
		if(characterName+'.csv' in os.listdir('./Character Stuff/Notes')):
			notesFile = open('./Character Stuff/Notes/'+characterName+'.csv', 'a')
			writer = csv.writer(notesFile)
			writer.writerow([arg])
			notesFile.close()
			await ctx.send('Added note `{}` to `{}`'.format(arg, characterName))
		else:
			await ctx.send('Character `{}` notes not found.'.format(characterName))
	else:
		await ctx.send('No character found for user id `{}`'.format(ctx.author.id))

@bot.command(name='notes')
async def shownotes(ctx, arg=None):
	'''Show notes you've taken for your character. Only usable by people with characters.'''
	if(arg == None):
		if(ctx.author.id in bot.players):
			characterName = bot.players[ctx.author.id]
			if(characterName+'.csv' in os.listdir('./Character Stuff/Notes')):
				if(len(bot.noteMessages) >= 10):
					bot.noteMessages.pop(0)
				while(len([message for message in bot.noteMessages if message.user == ctx.author]) != 0):
					for index in range(len(bot.noteMessages)):
						if(bot.noteMessages[index].user == ctx.author):
							bot.noteMessages.pop(index)
							break
				bot.noteMessages.append(notes.NotesMessage(ctx.author, characterName))
				await bot.noteMessages[-1].Send(ctx.channel)
	else:
		for message in bot.noteMessages:
			if(message.user == ctx.author):
				if(arg.isdigit()):
					if(int(arg) <= len(message.notes) and int(arg) > 0):
						await message.GoToNumber(int(arg))

@bot.command()
async def roll(ctx, *, comment=''):
	'''Roll for your character. Only usable by people with characters. Use emoji to select a stat, or the die to roll with no stat.'''
	if(ctx.author.id in bot.players):
		character = bot.characters[bot.players[ctx.author.id]]
		if(ctx.author.id in bot.rollMessages):
			bot.rollMessages.pop(ctx.author.id)
		bot.rollMessages[ctx.author.id] = moves.RollMessage(ctx.author, character, comment)
		await bot.rollMessages[ctx.author.id].Send(ctx.channel)

@bot.command()
@commands.is_owner()
async def harm(ctx, character, harmNumber):
	if(character.title() in bot.characters):
		if(harmNumber.lstrip('-').isdigit()):
			bot.characters[character.title()].TakeHarm(int(harmNumber))
			await ctx.send('`{}` harm added to `{}`, current harm {}/7'.format(harmNumber, character.title(), bot.characters[character.title()].harm))
		else:
			await ctx.send("I'm just a bot, I can't figure out how `{}` is a number.".format(harmNumber))
	else:
		await ctx.send("Character `{}` not found.".format(character.title()))

@bot.command()
@commands.is_owner()
async def xp(ctx, character, xpNumber):
	if(character.title() in bot.characters):
		if(xpNumber.lstrip('-').isdigit()):
			bot.characters[character.title()].MarkXP(int(xpNumber))
			await ctx.send('`{}` xp added to `{}`, current xp {}/5'.format(xpNumber, character.title(), bot.characters[character.title()].xp))
		else:
			await ctx.send("I'm just a bot, I can't figure out how `{}` is a number.".format(xpNumber))
	else:
		await ctx.send("Character `{}` not found.".format(character.title()))

@bot.command()
@commands.is_owner()
async def luck(ctx, character, luckNumber):
	if(character.title() in bot.characters):
		if(luckNumber.lstrip('-').isdigit()):
			bot.characters[character.title()].MarkLuck(int(luckNumber))
			await ctx.send('`{}` luck added to `{}`, current luck {}/7'.format(luckNumber, character.title(), bot.characters[character.title()].luck))
		else:
			await ctx.send("I'm just a bot, I can't figure out how `{}` is a number.".format(luckNumber))
	else:
		await ctx.send("Character `{}` not found.".format(character.title()))

@bot.command()
@commands.is_owner()
async def teaser(ctx):
	embed = discord.Embed(title='Teaser')
	textFile = open('./Embed Data/Teaser.txt')
	text = textFile.read()
	textFile.close()
	embed.description = text
	await ctx.send(embed=embed)

@bot.command()
async def choose(ctx, choice1, choice2):
	'''Randomly choose between two choices. For multiple words, enclose choices in "quotation marks."'''
	result = random.choice([choice1, choice2])
	message = await ctx.send("```{}```".format(result))

@bot.command()
@commands.is_owner()
async def postembed(ctx, name=''):
	embed = EmbedGenerator.GenerateEmbed(name)
	await ctx.send(embed=embed)
	await ctx.message.delete()

@bot.command()
@commands.is_owner()
async def makeembed(ctx, filename='foo', author='', title='', color='', description ='', thumbnail='', image=''):
	bot.embedGenerator = EmbedGenerator.EmbedGenerator(ctx, filename, author, title, color, description, thumbnail, image)
	await bot.embedGenerator.Send(ctx)




@bot.command()
@commands.is_owner()
async def logout(ctx):
	await bot.logout()
	await bot.close()

@bot.event
async def on_reaction_add(reaction, user):
	if(user != bot.user):
		if(bot.moveMessage != None):
			if(reaction.message.id == bot.moveMessage.message.id and bot.moveMessage.user == user):
				if(str(reaction) == moves.arrowLeft):
					await bot.moveMessage.Back()
				elif(str(reaction) == moves.arrowRight):
					await bot.moveMessage.Advance()
				elif(str(reaction) == moves.questionMark):
					await bot.moveMessage.ShowDetails()
				elif(str(reaction) in moves.emojiNumbers):
					await bot.moveMessage.GoToNumber(str(reaction))
				elif(str(reaction) == moves.listEmoji):
					await bot.moveMessage.ListMoves()
		for playbookMessage in bot.playbookMessages:
			message = bot.playbookMessages[playbookMessage]
			if(message != None):
				if(reaction.message.id == message.message.id and message.user == user):
					if(str(reaction) == characters.listEmoji):
						await message.ShowInfo()
					elif(str(reaction) == characters.starEmoji):
						await message.PlaybookFields()
					elif(str(reaction) == characters.mEmoji):
						await message.ShowMoves()
					elif(str(reaction) == characters.toolsEmoji):
						await message.ShowInventory()
					elif(str(reaction) == characters.upEmoji):
						await message.ShowImprovements()
		for noteMessage in bot.noteMessages:
			if(reaction.message.id == noteMessage.message.id and noteMessage.user == user):
				if(str(reaction) == notes.arrowLeft):
					await noteMessage.Back()
				elif(str(reaction) == notes.arrowRight):
					await noteMessage.Advance()
				elif(str(reaction) == notes.questionMark):
					await noteMessage.ShowHelp()
		if(user.id in bot.rollMessages):
			if(reaction.message.id == bot.rollMessages[user.id].message.id and bot.rollMessages[user.id].user == user):
				if(str(reaction) in moves.statEmoji):
					await bot.rollMessages[user.id].OnStatPick(str(reaction))
					bot.rollMessages.pop(user.id)
				elif(str(reaction) == moves.dieEmoji):
					await bot.rollMessages[user.id].OnStatPick()
					bot.rollMessages.pop(user.id)
				elif(str(reaction) == moves.plusEmoji):
					await bot.rollMessages[user.id].Add()
				elif(str(reaction) == moves.minusEmoji):
					await bot.rollMessages[user.id].Minus()
		if(bot.embedGenerator != None and user.id == bot.embedGenerator.ctx.author.id):
			if(str(reaction) == EmbedGenerator.checkEmoji):
				await bot.embedGenerator.Save()


async def save_characters():
	await bot.wait_until_ready()
	while True:
		print('Saving Characters')
		for character in bot.characters:
			bot.characters[character].Save(bot.activeGame)
		await asyncio.sleep(60)

if(__name__ == '__main__'):
	bot.loop.create_task(save_characters())
	bot.run(TOKEN)
