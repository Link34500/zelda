import {
  ChatInputCommandInteraction,
  Client,
  Collection,
  GatewayIntentBits,
  MessageFlags,
  SlashCommandBuilder,
} from "discord.js";
import path from "path";
import { configDotenv } from "dotenv";
import { registerCommandsDir } from "@/utils";

configDotenv();

declare module "discord.js" {
  interface Client {
    commands: Collection<string, Command>;
  }
}

export interface Command {
  data: SlashCommandBuilder;
  execute: (interaction: ChatInputCommandInteraction) => Promise<void>;
}

export const client = new Client({
  intents: [
    GatewayIntentBits.GuildMembers,
    GatewayIntentBits.Guilds,
    GatewayIntentBits.MessageContent,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.DirectMessages,
    GatewayIntentBits.DirectMessageTyping,
  ],
});

// Chargemment des commandes
(async () => {
  client.commands = await registerCommandsDir(
    path.join(__dirname, "commands"),
    new Collection()
  );
  console.log("Les commandes ont été chargées");

  client.on("interactionCreate", async (interaction) => {
    if (!interaction.isChatInputCommand()) return;
    const command = interaction.client.commands.get(interaction.commandName);

    if (!command) {
      console.error(`No command Matching ${interaction.commandName}`);
      return;
    }
    try {
      await command.execute(interaction);
    } catch (error) {
      console.error(error);
      if (interaction.replied || interaction.deferred) {
        interaction.followUp({
          content: "Une erreur s'est produite",
          flags: MessageFlags.Ephemeral,
        });
      } else {
        interaction.reply({
          content: "Une erreur s'est produite",
          flags: MessageFlags.Ephemeral,
        });
      }
    }
  });
})();

client.login(process.env.DISCORD_TOKEN);
