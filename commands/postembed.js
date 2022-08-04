const {SlashCommandBuilder} = require('@discordjs/builders');
const { MessageActionRow, MessageButton, SelectMenuComponent, EmbedBuilder, Util, resolveColor} = require('discord.js');
const fs = require('fs');


module.exports = 
{
	data: new SlashCommandBuilder()
	.setName('postembed')
	.setDescription('Posts an embed!')
	.addStringOption(option =>
		option.setName('name')
		.setDescription('The embed\'s name')
		.setRequired(true)),

	async execute(interaction)
	{
		const name = interaction.options.getString('name');
		const embedData = JSON.parse(fs.readFileSync(`./Embed Data/${name}.json`));
		const embed = new EmbedBuilder()
		.setColor(resolveColor(embedData.color))
		.setTitle(embedData.title)
		.setThumbnail(embedData.url)
		.setDescription(embedData.description.replaceAll('\\n', '\n'));
		await interaction.reply({embeds: [embed]});
	},
}