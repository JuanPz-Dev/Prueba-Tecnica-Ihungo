import { describe, expect, test } from "vitest";
import { leastNumberWithBouncyRatio } from "../src/bouncy";

describe("leastNumberWithBouncyRatio", () => {
  test("50% debe devolver 538", () => {
    expect(leastNumberWithBouncyRatio(50)).toBe(538);
  });

  test("90% debe devolver 21780", () => {
    expect(leastNumberWithBouncyRatio(90)).toBe(21780);
  });

  test("99% debe devolver 1587000", () => {
    expect(leastNumberWithBouncyRatio(99)).toBe(1587000);
  });

  test("debe rechazar porcentajes menores que 1", () => {
    expect(() => leastNumberWithBouncyRatio(0)).toThrow();
  });

  test("debe rechazar porcentajes mayores que 99", () => {
    expect(() => leastNumberWithBouncyRatio(100)).toThrow();
  });
});