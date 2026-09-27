import {describe, expect, test } from "vitest";
import {main} from "../src/cli"

describe("CLI de números bouncy", () => {
  test("50% debe mostrar 538", () => {
    expect(main(["50"])).toBe(538);
  });

  test("90% debe mostrar 21780", () => {
    expect(main(["90"])).toBe(21780);
  });

  test("debe rechazar un porcentaje inválido", () => {
    expect(() => main(["100"])).toThrow();
  });
});