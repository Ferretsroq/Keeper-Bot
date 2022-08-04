const {SlashCommandBuilder} = require('@discordjs/builders');
const { ActionRowBuilder, ButtonBuilder, SelectMenuComponent, EmbedBuilder, ButtonStyle, resolveColor } = require('discord.js');
const fs = require('fs');
const Character = require('../characters.js');


module.exports = 
{
	data: new SlashCommandBuilder()
	.setName('luck')
	.setDescription('Mark luck on a character!')
	.addStringOption(option =>
		option.setName('name')
		.setRequired(true)
		.setDescription('Name of character to mark luck on'))
	.addIntegerOption(option =>
		option.setName('luck')
		.setRequired(true)
		.setDescription('Amount of luck to mark')),
	async execute(interaction, characters)
	{
		let name = interaction.options.getString('name');
		let luckNumber = interaction.options.getInteger('luck');
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
			char.MarkLuck(luckNumber);
			await interaction.reply(`Added ${luckNumber} xp to ${name}.\nCurrent xp: ${char.luck}/7`);
		}
	},
}