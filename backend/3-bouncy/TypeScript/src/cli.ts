import { least_number_with_bouncy_ratio } from "./bouncy";

export function main(args: string[]): number {
  const percent = Number(args[0]);

  if (!Number.isInteger(percent) || percent < 1 || percent > 99) {
    throw new Error("El porcentaje debe ser un entero entre 1 y 99.");
  }

  return least_number_with_bouncy_ratio(percent);
}

if (process.argv[1]?.endsWith("cli.ts")) {
  try {
    const result = main(process.argv.slice(2));
    console.log(result);
  } catch (error) {
    console.error(error instanceof Error ? error.message : error);
    process.exit(1);
  }
}