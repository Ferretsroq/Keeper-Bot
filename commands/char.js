const {SlashCommandBuilder} = require('@discordjs/builders');
const {ActionRowBuilder, SelectMenuBuilder, ButtonBuilder, ButtonStyle, SelectMenuOptionBuilder, EmbedBuilder} = require('discord.js');
fs = require('fs');
Character = require('../characters.js');


module.exports = 
{
	data: new SlashCommandBuilder()
	.setName('char')
	.setDescription('Fetch your character!')
	.addStringOption(option =>
		option.setName('name')
		.setRequired(false)
		.setDescription('Name of character to fetch')),
	char: null,
	rows: [],
	embed: null,
	async execute(interaction, characters, players)
	{
		this.char = null;
		this.rows = [];
		let name = interaction.options.getString('name');
		if(name === null)
		{
			name = players[interaction.user.id.toString()];
		}
		for(character in Object.keys(characters))
		{
			if(Object.keys(characters)[character] === name)
			{
				this.char = characters[Object.keys(characters)[character]];
			}
		}
		

		await interaction.reply({embeds: [this.char.playbookEmbed()]});
	},
	
}