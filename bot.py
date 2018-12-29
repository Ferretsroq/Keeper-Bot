import discord
from discord.ext import commands
import characters
import moves

TOKEN = open('token.token').read()

bot = commands.Bot(command_prefix='$', case_insensitive=True)

bot.moveMessage = None

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
						'Wronged': None}

@bot.command()
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
async def test(ctx, *, arg):
	await ctx.send('You said {}'.format(arg))

@bot.command()
async def chosen(ctx):
	data, fields = characters.LoadCharacter('Chosen')
	bot.playbookMessages['Chosen'] = characters.ChosenMessage(characters.Chosen(data, fields), ctx.author)
	await bot.playbookMessages['Chosen'].Send(ctx)

@bot.command()
async def crooked(ctx):
	data, fields = characters.LoadCharacter('Crooked')
	bot.playbookMessages['Crooked'] = characters.CrookedMessage(characters.Crooked(data, fields), ctx.author)
	await bot.playbookMessages['Crooked'].Send(ctx)

@bot.command()
async def divine(ctx):
	data, fields = characters.LoadCharacter('Divine')
	bot.playbookMessages['Divine'] = characters.DivineMessage(characters.Divine(data, fields), ctx.author)
	await bot.playbookMessages['Divine'].Send(ctx)

@bot.command()
async def expert(ctx):
	data, fields = characters.LoadCharacter('Expert')
	bot.playbookMessages['Expert'] = characters.ExpertMessage(characters.Expert(data, fields), ctx.author)
	await bot.playbookMessages['Expert'].Send(ctx)

@bot.command()
async def flake(ctx):
	data, fields = characters.LoadCharacter('Flake')
	bot.playbookMessages['Flake'] = characters.FlakeMessage(characters.Flake(data, fields), ctx.author)
	await bot.playbookMessages['Flake'].Send(ctx)

@bot.command()
async def initiate(ctx):
	data, fields = characters.LoadCharacter('Initiate')
	bot.playbookMessages['Initiate'] = characters.InitiateMessage(characters.Initiate(data, fields), ctx.author)
	await bot.playbookMessages['Initiate'].Send(ctx)

@bot.command()
async def monstrous(ctx):
	data, fields = characters.LoadCharacter('Monstrous')
	bot.playbookMessages['Monstrous'] = characters.MonstrousMessage(characters.Monstrous(data, fields), ctx.author)
	await bot.playbookMessages['Monstrous'].Send(ctx)

@bot.command()
async def mundane(ctx):
	data, fields = characters.LoadCharacter('Mundane')
	bot.playbookMessages['Mundane'] = characters.MundaneMessage(characters.Mundane(data, fields), ctx.author)
	await bot.playbookMessages['Mundane'].Send(ctx)

@bot.command()
async def professional(ctx):
	data, fields = characters.LoadCharacter('Professional')
	bot.playbookMessages['Professional'] = characters.ProfessionalMessage(characters.Professional(data, fields), ctx.author)
	await bot.playbookMessages['Professional'].Send(ctx)

@bot.command()
async def spellslinger(ctx):
	data, fields = characters.LoadCharacter('Spell-Slinger')
	bot.playbookMessages['Spell-Slinger'] = characters.SpellSlingerMessage(characters.SpellSlinger(data, fields), ctx.author)
	await bot.playbookMessages['Spell-Slinger'].Send(ctx)

@bot.command()
async def spooky(ctx):
	data, fields = characters.LoadCharacter('Spooky')
	bot.playbookMessages['Spooky'] = characters.SpookyMessage(characters.Spooky(data, fields), ctx.author)
	await bot.playbookMessages['Spooky'].Send(ctx)

@bot.command()
async def wronged(ctx):
	data, fields = characters.LoadCharacter('Wronged')
	bot.playbookMessages['Wronged'] = characters.WrongedMessage(characters.Wronged(data, fields), ctx.author)
	await bot.playbookMessages['Wronged'].Send(ctx)


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
						pass

if(__name__ == '__main__'):
	bot.run(TOKEN)