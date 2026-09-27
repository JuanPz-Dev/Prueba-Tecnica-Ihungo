# Backend 3 — Números Bouncy

Implementación del ejercicio de números bouncy en **Python** y **TypeScript**.

## Estructura

```text
3-bouncy/
├── python/
│   ├── bouncy.py
│   ├── cli.py
│   └── test/
│       ├── test_bouncy.py
│       └── test_cli.py
│
├── typescript/
│   ├── src/
│   │   ├── bouncy.ts
│   │   └── cli.ts
│   ├── test/
│   │   ├── bouncy.test.ts
│   │   └── cli.test.ts
│   ├── package.json
│   ├── package-lock.json
│   ├── tsconfig.json
│   └── vitest.config.ts
│
└── README.md
```

## Python

Desde `backend/3-bouncy/python`:

```bash
pytest -v
```

Ejecutar la CLI:

```bash
python cli.py 50
python cli.py 90
python cli.py 99
```

Resultados:

```text
50 → 538
90 → 21780
99 → 1587000
```

## TypeScript

Desde `backend/3-bouncy/typescript`:

```bash
npm install
npm test
```

Verificar tipos:

```bash
npx tsc --noEmit
```

Ejecutar la CLI:

```bash
npx tsx src/cli.ts 50
npx tsx src/cli.ts 90
npx tsx src/cli.ts 99
```

Resultados:

```text
50 → 538
90 → 21780
99 → 1587000
```

## Validación

El porcentaje debe ser un entero entre `1` y `99`. Las dos implementaciones rechazan valores fuera de este rango.

La proporción se compara mediante aritmética entera:

```text
bouncyCount * 100 == percent * number
```

Esto evita utilizar operaciones con punto flotante.

## Complejidad

Para `N` como resultado:

* Tiempo: `O(N log N)`
* Espacio: `O(log N)`

## Tiempo de ejecución para 99%

Medido en el equipo de desarrollo:

| Implementación | Resultado |     Tiempo |
| -------------- | --------: | ---------: |
| Python         |   1587000 | 0.952460 s |
| TypeScript     |   1587000 | 0.224548 s |

## Pruebas

Se utilizaron:

* **pytest** para Python.
* **Vitest** para TypeScript.

Se probaron los casos `50%`, `90%`, `99%` y entradas inválidas.

Las pruebas fueron creadas antes de la implementación de la lógica principal para seguir TDD.