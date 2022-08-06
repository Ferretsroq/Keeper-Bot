const {SlashCommandBuilder} = require('@discordjs/builders');
const { ActionRowBuilder, ButtonBuilder, SelectMenuComponent, EmbedBuilder, ButtonStyle, resolveColor } = require('discord.js');
const fs = require('fs');
const Character = require('../characters.js');


module.exports = 
{
	data: new SlashCommandBuilder()
	.setName('xp')
	.setDescription('Mark xp on a character!')
	.addStringOption(option =>
		option.setName('name')
		.setRequired(true)
		.setDescription('Name of character to mark xp on'))
	.addIntegerOption(option =>
		option.setName('xp')
		.setRequired(true)
		.setDescription('Amount of xp to mark')),
	async execute(interaction, characters)
	{
		let name = interaction.options.getString('name');
		let xpNumber = interaction.options.getInteger('xp');
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
			char.MarkXP(xpNumber);
			await interaction.reply(`Added ${xpNumber} xp to ${name}.\nCurrent xp: ${char.xp}/5`);
		}
	},
}