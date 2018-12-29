import discord
from discord.ext import commands
import characters
import moves

TOKEN = open('token.token').read()

bot = commands.Bot(command_prefix='$')
bot.moveMessage = None
bot.chosenMessage = None
bot.crookedMessage = None
bot.divineMessage = None
bot.expertMessage = None
bot.flakeMessage = None
bot.initiateMessage = None
bot.monstrousMessage = None
bot.mundaneMessage = None
bot.professionalMessage = None
bot.spellslingerMessage = None
bot.spookyMessage = None
bot.wrongedMessage = None

@bot.command()
async def test(ctx, *, arg):
	await ctx.send('You said {}'.format(arg))

@bot.command()
async def chosen(ctx):
	data, fields = characters.LoadCharacter('Chosen')
	chosen = characters.Chosen(data, fields)
	bot.chosenMessage = characters.ChosenMessage(chosen, ctx.author)
	await bot.chosenMessage.Send(ctx)

@bot.command()
async def crooked(ctx):
	data, fields = characters.LoadCharacter('Crooked')
	crooked = characters.Crooked(data, fields)
	bot.crookedMessage = characters.CrookedMessage(crooked, ctx.author)
	await bot.crookedMessage.Send(ctx)

@bot.command()
async def divine(ctx):
	data, fields = characters.LoadCharacter('Divine')
	divine = characters.Divine(data, fields)
	bot.divineMessage = characters.DivineMessage(divine, ctx.author)
	await bot.divineMessage.Send(ctx)

@bot.command()
async def expert(ctx):
	data, fields = characters.LoadCharacter('Expert')
	expert = characters.Expert(data, fields)
	bot.expertMessage = characters.ExpertMessage(expert, ctx.author)
	await bot.expertMessage.Send(ctx)

@bot.command()
async def flake(ctx):
	data, fields = characters.LoadCharacter('Flake')
	flake = characters.Flake(data, fields)
	bot.flakeMessage = characters.FlakeMessage(flake, ctx.author)
	await bot.flakeMessage.Send(ctx)

@bot.command()
async def initiate(ctx):
	data, fields = characters.LoadCharacter('Initiate')
	initiate = characters.Initiate(data, fields)
	bot.initiateMessage = characters.InitiateMessage(initiate, ctx.author)
	await bot.initiateMessage.Send(ctx)

@bot.command()
async def monstrous(ctx):
	data, fields = characters.LoadCharacter('Monstrous')
	monstrous = characters.Monstrous(data, fields)
	bot.monstrousMessage = characters.MonstrousMessage(monstrous, ctx.author)
	await bot.monstrousMessage.Send(ctx)

@bot.command()
async def mundane(ctx):
	data, fields = characters.LoadCharacter('Mundane')
	mundane = characters.Mundane(data, fields)
	bot.mundaneMessage = characters.MundaneMessage(mundane, ctx.author)
	await bot.mundaneMessage.Send(ctx)

@bot.command()
async def professional(ctx):
	data, fields = characters.LoadCharacter('Professional')
	professional = characters.Professional(data, fields)
	bot.professionalMessage = characters.ProfessionalMessage(professional, ctx.author)
	await bot.professionalMessage.Send(ctx)

@bot.command()
async def spellslinger(ctx):
	data, fields = characters.LoadCharacter('Spell-Slinger')
	spellslinger = characters.SpellSlinger(data, fields)
	bot.spellslingerMessage = characters.SpellSlingerMessage(spellslinger, ctx.author)
	await bot.spellslingerMessage.Send(ctx)

@bot.command()
async def spooky(ctx):
	data, fields = characters.LoadCharacter('Spooky')
	spooky = characters.Spooky(data, fields)
	bot.spookyMessage = characters.SpookyMessage(spooky, ctx.author)
	await bot.spookyMessage.Send(ctx)

@bot.command()
async def wronged(ctx):
	data, fields = characters.LoadCharacter('Wronged')
	wronged = characters.Wronged(data, fields)
	bot.wrongedMessage = characters.WrongedMessage(wronged, ctx.author)
	await bot.wrongedMessage.Send(ctx)



@bot.command(name='moves')
async def move(ctx):
	'''Lists all of the basic hunter moves. Left/Right arrows to scroll. Question Mark shows additional details. List lists all of the basic moves.'''
	bot.moveMessage = moves.MovesMessage(ctx.author)
	await bot.moveMessage.Send(ctx.channel)

@bot.command()
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
		if(bot.chosenMessage != None):
			if(reaction.message.id == bot.chosenMessage.message.id and bot.chosenMessage.user == user):
				if(str(reaction) == characters.listEmoji):
					await bot.chosenMessage.ShowInfo()
				elif(str(reaction) == characters.starEmoji):
					await bot.chosenMessage.PlaybookFields()
				elif(str(reaction) == characters.mEmoji):
					await bot.chosenMessage.ShowMoves()
		if(bot.crookedMessage != None):
			if(reaction.message.id == bot.crookedMessage.message.id and bot.crookedMessage.user == user):
				if(str(reaction) == characters.listEmoji):
					await bot.crookedMessage.ShowInfo()
				elif(str(reaction) == characters.starEmoji):
					await bot.crookedMessage.PlaybookFields()
				elif(str(reaction) == characters.mEmoji):
					await bot.crookedMessage.ShowMoves()
		if(bot.divineMessage != None):
			if(reaction.message.id == bot.divineMessage.message.id and bot.divineMessage.user == user):
				if(str(reaction) == characters.listEmoji):
					await bot.divineMessage.ShowInfo()
				elif(str(reaction) == characters.starEmoji):
					await bot.divineMessage.PlaybookFields()
				elif(str(reaction) == characters.mEmoji):
					await bot.divineMessage.ShowMoves()
		if(bot.expertMessage != None):
			if(reaction.message.id == bot.expertMessage.message.id and bot.expertMessage.user == user):
				if(str(reaction) == characters.listEmoji):
					await bot.expertMessage.ShowInfo()
				elif(str(reaction) == characters.starEmoji):
					await bot.expertMessage.PlaybookFields()
				elif(str(reaction) == characters.mEmoji):
					await bot.expertMessage.ShowMoves()
		if(bot.flakeMessage != None):
			if(reaction.message.id == bot.flakeMessage.message.id and bot.flakeMessage.user == user):
				if(str(reaction) == characters.listEmoji):
					await bot.flakeMessage.ShowInfo()
				elif(str(reaction) == characters.starEmoji):
					await bot.flakeMessage.PlaybookFields()
				elif(str(reaction) == characters.mEmoji):
					await bot.flakeMessage.ShowMoves()
		if(bot.initiateMessage != None):
			if(reaction.message.id == bot.initiateMessage.message.id and bot.initiateMessage.user == user):
				if(str(reaction) == characters.listEmoji):
					await bot.initiateMessage.ShowInfo()
				elif(str(reaction) == characters.starEmoji):
					await bot.initiateMessage.PlaybookFields()
				elif(str(reaction) == characters.mEmoji):
					await bot.initiateMessage.ShowMoves()
		if(bot.monstrousMessage != None):
			if(reaction.message.id == bot.monstrousMessage.message.id and bot.monstrousMessage.user == user):
				if(str(reaction) == characters.listEmoji):
					await bot.monstrousMessage.ShowInfo()
				elif(str(reaction) == characters.starEmoji):
					await bot.monstrousMessage.PlaybookFields()
				elif(str(reaction) == characters.mEmoji):
					await bot.monstrousMessage.ShowMoves()
		if(bot.mundaneMessage != None):
			if(reaction.message.id == bot.mundaneMessage.message.id and bot.mundaneMessage.user == user):
				if(str(reaction) == characters.listEmoji):
					await bot.mundaneMessage.ShowInfo()
				elif(str(reaction) == characters.starEmoji):
					await bot.mundaneMessage.PlaybookFields()
				elif(str(reaction) == characters.mEmoji):
					await bot.mundaneMessage.ShowMoves()
		if(bot.professionalMessage != None):
			if(reaction.message.id == bot.professionalMessage.message.id and bot.professionalMessage.user == user):
				if(str(reaction) == characters.listEmoji):
					await bot.professionalMessage.ShowInfo()
				elif(str(reaction) == characters.starEmoji):
					await bot.professionalMessage.PlaybookFields()
				elif(str(reaction) == characters.mEmoji):
					await bot.professionalMessage.ShowMoves()
		if(bot.spellslingerMessage != None):
			if(reaction.message.id == bot.spellslingerMessage.message.id and bot.spellslingerMessage.user == user):
				if(str(reaction) == characters.listEmoji):
					await bot.spellslingerMessage.ShowInfo()
				elif(str(reaction) == characters.starEmoji):
					await bot.spellslingerMessage.PlaybookFields()
				elif(str(reaction) == characters.mEmoji):
					await bot.spellslingerMessage.ShowMoves()
		if(bot.spookyMessage != None):
			if(reaction.message.id == bot.spookyMessage.message.id and bot.spookyMessage.user == user):
				if(str(reaction) == characters.listEmoji):
					await bot.spookyMessage.ShowInfo()
				elif(str(reaction) == characters.starEmoji):
					await bot.spookyMessage.PlaybookFields()
				elif(str(reaction) == characters.mEmoji):
					await bot.spookyMessage.ShowMoves()
		if(bot.wrongedMessage != None):
			if(reaction.message.id == bot.wrongedMessage.message.id and bot.wrongedMessage.user == user):
				if(str(reaction) == characters.listEmoji):
					await bot.wrongedMessage.ShowInfo()
				elif(str(reaction) == characters.starEmoji):
					await bot.wrongedMessage.PlaybookFields()
				elif(str(reaction) == characters.mEmoji):
					await bot.wrongedMessage.ShowMoves()

if(__name__ == '__main__'):
	bot.run(TOKEN)