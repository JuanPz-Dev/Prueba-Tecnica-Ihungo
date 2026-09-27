import { describe, expect, test } from "vitest";
import { least_number_with_bouncy_ratio } from "../src/bouncy";

describe("leastNumberWithBouncyRatio", () => {
  test("50% debe devolver 538", () => {
    expect(least_number_with_bouncy_ratio(50)).toBe(538);
  });

  test("90% debe devolver 21780", () => {
    expect(least_number_with_bouncy_ratio(90)).toBe(21780);
  });

  test("99% debe devolver 1587000", () => {
    expect(least_number_with_bouncy_ratio(99)).toBe(1587000);
  });

  test("debe rechazar porcentajes menores que 1", () => {
    expect(() => least_number_with_bouncy_ratio(0)).toThrow();
  });

  test("debe rechazar porcentajes mayores que 99", () => {
    expect(() => least_number_with_bouncy_ratio(100)).toThrow();
  });
});