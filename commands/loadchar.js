const {SlashCommandBuilder} = require('@discordjs/builders');
const {ActionRowBuilder, SelectMenuBuilder, ButtonBuilder, ButtonStyle, SelectMenuOptionBuilder, EmbedBuilder} = require('discord.js');
fs = require('fs');
Character = require('../characters.js');


module.exports = 
{
	data: new SlashCommandBuilder()
	.setName('loadchar')
	.setDescription('Load a character!')
	.addStringOption(option =>
		option.setName('playbook')
		.setRequired(true)
		.setDescription('Playbook of character to load'))
	.addStringOption(option =>
		option.setName('name')
		.setRequired(false)
		.setDescription('Name of character to load')),
	char: null,
	async execute(interaction, activeGame, characters)
	{
		let name = interaction.options.getString('name');
		let playbook = Character.PlaybookByName(interaction.options.getString('playbook'));
		this.char = null;
		if(name == null)
		{
			name = `The_${playbook.Playbook()}`
		}
		if(fs.existsSync(`./Character Stuff/${activeGame}/${name}.pdf`))
		{
			this.char = await Character.DumpPDFToJSON(directory = activeGame, name=name, playbook=playbook);
			characters[this.char.alias] = this.char;

		}
		if(this.char != null)
		{
			await interaction.reply({embeds: [this.char.playbookEmbed()]});
			return this.char;
		}
		else
		{
			await interaction.reply({content: 'Could not find character!'});
		}
	},
	
}