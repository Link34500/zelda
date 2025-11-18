import { Collection, REST, Routes } from "discord.js";
import config from "@/config.json";
import { registerCommandsDir } from "@/utils";
import path from "path";
import { configDotenv } from "dotenv";

configDotenv();
const token = process.env.DISCORD_TOKEN!;
const rest = new REST().setToken(token);

(async () => {
  const collectionCommands = await registerCommandsDir(
    path.join(__dirname, "commands"),
    new Collection()
  );

  const commands = collectionCommands
    .mapValues((value) => value.data.toJSON())
    .values()
    .toArray();
  try {
    console.log(`Mise à jour de ${commands.length} commandes (/)`);
    const data: any = await rest.put(
      Routes.applicationGuildCommands(config.clientId, config.guildsId),
      { body: commands }
    );
    console.log(`Mise à jour réussite de ${data.length} commandes (/)`);
  } catch (error) {
    console.log(error);
  }
})();
