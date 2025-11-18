import { APIEmbed, ChatInputCommandInteraction, Interaction } from "discord.js";
import config from "@/config.json";
import { get } from "@/utils";

const setContext = (ctx: object, str: string) => {
  for (const [key, value] of Object.entries(ctx)) {
    // @ts-ignore
    str = str.replaceAll(`{${key}}`, value);
  }
  return str;
};

async function getTranslationFile(interaction: Interaction, path: string) {
  const defaultLang = await import(`./${config.lang}.json`);
  const lang = await import(`./${interaction.locale.slice(0, 2)}.json`);
  return get(lang, path) ?? get(defaultLang, path);
}

export async function translate(
  interaction: Interaction,
  path: string,
  context = {}
) {
  const translation = await getTranslationFile(interaction, path);
  if (!translation || typeof translation != "string") return "NOT_FOUND";
  return setContext(context, translation);
}

export async function embedTranslation(
  interaction: Interaction,
  path: string,
  context: Record<string, any> = {}
): Promise<APIEmbed> {
  const translation = await getTranslationFile(interaction, path);

  if (!translation) return { title: "TRANSLATION_NOT_FOUND" };

  const result = translateDeep(translation, translation, context);

  return result as APIEmbed;
}

function applyContext(str: string, ctx: Record<string, any>) {
  let result = str;

  for (const [k, v] of Object.entries(ctx)) {
    result = result.replaceAll(`{${k}}`, String(v));
  }

  return result;
}

function translateDeep(
  value: any,
  langObj: any,
  context: Record<string, any>
): any {
  // Cas 1 : string → traduction
  if (typeof value === "string") {
    const translated = get(langObj, value) ?? value;
    return applyContext(translated, context);
  }

  // Cas 2 : array → map récursif
  if (Array.isArray(value)) {
    return value.map((v) => translateDeep(v, langObj, context));
  }

  // Cas 3 : object → transformer chaque clé/valeur
  if (typeof value === "object" && value !== null) {
    const out: Record<string, any> = {};

    for (const [k, v] of Object.entries(value)) {
      out[k] = translateDeep(v, langObj, context);
    }

    return out;
  }

  // Autres cas : number, bool, null…
  return value;
}
