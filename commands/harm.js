const {SlashCommandBuilder} = require('@discordjs/builders');
const { ActionRowBuilder, ButtonBuilder, SelectMenuComponent, EmbedBuilder, ButtonStyle, resolveColor } = require('discord.js');
const fs = require('fs');
const Character = require('../characters.js');


module.exports = 
{
	data: new SlashCommandBuilder()
	.setName('harm')
	.setDescription('Mark harm on a character!')
	.addStringOption(option =>
		option.setName('name')
		.setRequired(true)
		.setDescription('Name of character to mark harm on'))
	.addIntegerOption(option =>
		option.setName('harm')
		.setRequired(true)
		.setDescription('Amount of harm to mark')),
	async execute(interaction, characters)
	{
		let name = interaction.options.getString('name');
		let harmNumber = interaction.options.getInteger('harm');
		let char = null;
		for(character in Object.keys(characters))
		{
			if(Object.keys(characters)[character] === name)
			{
				char = characters[Object.keys(characters)[character]];
			}
		}
		if(char === null)
		{
			await interaction.reply(`I couldn't find character ${name}`);
		}
		else
		{
			char.TakeHarm(harmNumber);
			await interaction.reply(`Added ${harmNumber} harm to ${name}.\nCurrent harm: ${char.harm}/7`);
		}
	},
}