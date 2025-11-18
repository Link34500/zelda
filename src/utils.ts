import { Collection } from "discord.js";
import fs, { promises } from "fs";
import path from "path";
import { Command } from "@/index";

export async function registerCommandsDir(
  directory: string,
  commands: Collection<string, Command>
) {
  const directoryIter = fs.readdirSync(directory);
  for (const file of directoryIter) {
    const pathToFile = path.join(directory, file);
    const stats = await promises.stat(pathToFile);
    if (stats.isDirectory()) {
      commands = await registerCommandsDir(pathToFile, commands);
      continue;
    }

    if (file.endsWith(".ts") || file.endsWith(".js")) {
      const { default: command }: { default: Command } = require(pathToFile);
      commands.set(command.data.name, command);
    }
  }
  return commands;
}

export function get(obj: any, path: string) {
  return path.split(".").reduce((o, k) => (o ? o[k] : undefined), obj);
}
