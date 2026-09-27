export function least_number_with_bouncy_ratio(percent: number): number {
  if (percent < 1 || percent > 99 || !Number.isInteger(percent)) {
    throw new Error("El porcentaje debe ser un entero entre 1 y 99.");
  }

  let bouncyCount = 0;
  let number = 99;

  while (true) {
    number++;

    if (isBouncy(number)) {
      bouncyCount++;
    }

    // evitando números decimales.
    if (bouncyCount * 100 === percent * number) {
      return number;
    }
  }
}

function isBouncy(number: number): boolean {
  const digits = String(number).split("").map(Number);

  let increasing = true;
  let decreasing = true;

  for (let i = 1; i < digits.length; i++) {
    if (digits[i] > digits[i - 1]) {
      decreasing = false;
    }
    if (digits[i] < digits[i - 1]) {
      increasing = false;
    }
  }
  return !increasing && !decreasing;
}