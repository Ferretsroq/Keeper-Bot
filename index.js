// Require the necessary discord.js classes
const {Client, Collection, GatewayIntentBits, InteractionType} = require('discord.js');
const {token} = require('./config.json');
const { clientId, guildIds } = require('./config.json');
const { REST } = require('@discordjs/rest');
const { Routes } = require('discord-api-types/v9');
fs = require('fs');
Character = require('./characters.js');


// Create a new client instance
const client = new Client({ intents: [GatewayIntentBits.Guilds] });
client.characters = {};
client.activeGame = 'Quarantine2Characters';
client.commands = new Collection();
const commandFiles = fs.readdirSync('./commands').filter(file => file.endsWith('.js'));

for (const file of commandFiles)
{
	const command = require(`./commands/${file}`);
	// Set a new item in the Collection
	// With the key as the command name and the value as the exported module
	client.commands.set(command.data.name, command);
}

// Load character data
LoadCharacters(client);
client.players = {
			   '287370784568246272': 'Anne',
			   '448613063713751042': 'Shaggy',
			   '232645483976327168': 'Aaron',
			   '397784579915644928': 'Quinn',
			   '111529517541036032': 'Chuck'
			   };
// When the client is ready, run this code (only once)
client.once('ready', () => {
	console.log('Ready!');
	setInterval(function(){SaveCharacters(client)}, 60000);
});

// Command listener
client.on('interactionCreate', async interaction =>
{
	if(interaction.type != InteractionType.ApplicationCommand) return;
	const command = client.commands.get(interaction.commandName);
	if(!command) return;
	try
	{
		if(interaction.commandName === 'char')
		{
			await command.execute(interaction, client.characters, client.players);
		}
		else if(interaction.commandName === 'loadchar')
		{
			let newchar = await command.execute(interaction, client.activeGame, client.characters);
			client.characters[newchar.name] = newchar;
		}
		else if(interaction.commandName === 'roll')
		{
			await command.execute(interaction, client.characters, client.players);
		}
		else if(interaction.commandName === 'harm')
		{
			await command.execute(interaction, client.characters);
		}
		else if(interaction.commandName === 'inventory')
		{
			await command.execute(interaction, client.characters);
		}
		else if(interaction.commandName === 'additem')
		{
			await command.execute(interaction, client.characters, client.players)
		}
		else
		{
			await command.execute(interaction);
		}
	}
	catch (error)
	{
		console.error(error);
		await interaction.reply({content: 'There was an error while executing this command!', ephemeral: true});
	}
});

// Button listener
client.on('interactionCreate', async interaction =>
{
	if(!interaction.isButton()) return;
	if(interaction.customId.startsWith('roll'))
	{
		await client.commands.get('roll').Roll(interaction, interaction.customId.split('roll')[1]);
	}
	else if(interaction.customId === 'movesLeft')
	{
		await client.commands.get('moves').MoveLeft(interaction);
	}
	else if(interaction.customId === 'movesRight')
	{
		await client.commands.get('moves').MoveRight(interaction);
	}
	else if(interaction.customId === 'movesList')
	{
		await client.commands.get('moves').ListMoves(interaction);
	}
	else if(interaction.customId === 'movesExpand')
	{
		await client.commands.get('moves').ExpandMove(interaction);
	}
	else if(interaction.customId.startsWith('movesGoTo'))
	{
		let number = interaction.customId.split('movesGoTo')[1];
		await client.commands.get('moves').GoToMove(interaction, number);
	}
	else if (interaction.customId.startsWith('inventoryShow'))
	{
		let item = interaction.customId.split('inventoryShow')[1];
		await client.commands.get('inventory').ShowItem(interaction, item);
	}
	else if(interaction.customId.startsWith('inventoryDelete'))
	{
		let item = interaction.customId.split('inventoryDelete')[1];
		await client.commands.get('inventory').DeleteItem(interaction, item);
	}
	else if(interaction.customId == 'inventoryGoBack')
	{
		await client.commands.get('inventory').ShowInventory(interaction);
	}
	

});

// Modal submit listener
client.on('interactionCreate', async interaction =>
{
	if(interaction.type != InteractionType.ModalSubmit) return;
	if(interaction.customId == 'modalFoo')
	{
		await client.commands.get('testmodal').Submit(interaction);
	}
});



//Login to Discord with your client's token
client.login(token);


function LoadCharacters(client)
{
	let playerCharacters = [['Anne', Character.Professional], ['Shaggy', Character.Spooky], ['Aaron Hunter', Character.Monstrous], ['Quinn', Character.Searcher], ['Chuck', Character.Chosen]];
	client.characters = Character.LoadAllCharactersFromJSON(playerCharacters);
}

function SaveCharacters(client)
{
	for(character = 0; character < Object.keys(client.characters).length; character++)
	{
		console.log(`Saving character ${client.characters[Object.keys(client.characters)[character]].alias}`)
		client.characters[Object.keys(client.characters)[character]].Save();
	}

}