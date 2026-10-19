
import argparse
import textwrap

LABERINTO = [
    ['F', 1, 1, 3, 0, 1, 1, 1, 4],
    [3, 0, 0, 1, 0, 1, 0, 0, 1],
    [1, 1, 0, 1, 1, 1, 1, 0, 1],
    [0, 1, 0, 1, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 3, 1, 1],
    [3, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 3, 1, 1, 1, 1],
    [1, 0, 0, 1, 0, 1, 0, 0, 4],
    ['I', 1, 3, 1, 0, 1, 1, 1, 1],
]

N = len(LABERINTO)
INICIO = (8, 0)
META = (0, 0)
PUNTOS_MINIMOS = 23

MOVIMIENTOS = [
    (-1, 0, '↑', 'arriba'),
    (0, 1, '→', 'derecha'),
    (1, 0, '↓', 'abajo'),
    (0, -1, '←', 'izquierda')
]


def puntos_de(celda):
    return celda if celda in (3, 4) else 0


def es_valido(f, c, visitado):
    return (
        0 <= f < N
        and 0 <= c < N
        and LABERINTO[f][c] != 0
        and not visitado[f][c]
    )


def mostrar_matriz(matriz, titulo):
    print(titulo)
    print('      ' + ' '.join(str(j) for j in range(N)))
    print('     ' + '-' * (2 * N + 1))
    for i, fila in enumerate(matriz):
        print(f'  {i} | ' + ' '.join(str(x) for x in fila))
    print()


def buscar_salida(f, c, puntos, camino, visitado, minimo, est, traza):
    est['nodos'] += 1

    if (f, c) == META:
        if puntos >= minimo:
            if traza:
                print(f'  >>> Llegó a F con {puntos} puntos (>= {minimo}): ¡CAMINO VÁLIDO!')
            return True

        est['rechazados'] += 1
        if traza:
            print(f'  >>> Llegó a F con {puntos} puntos (< {minimo}): no sirve, retrocede')
        return False

    for df, dc, flecha, nombre in MOVIMIENTOS:
        nf, nc = f + df, c + dc

        if es_valido(nf, nc, visitado):
            nuevos = puntos + puntos_de(LABERINTO[nf][nc])
            visitado[nf][nc] = True
            camino.append((nf, nc))

            if traza:
                print(
                    f'  Avanza {flecha} {nombre:<9} -> ({nf},{nc})  '
                    f'valor={LABERINTO[nf][nc]}  puntos={nuevos}'
                )

            if buscar_salida(
                nf, nc, nuevos, camino, visitado, minimo, est, traza
            ):
                return True

            camino.pop()
            visitado[nf][nc] = False

            if traza:
                print(f'  Retrocede desde ({nf},{nc}) -> vuelve a ({f},{c})')

    return False


def resolver(minimo=PUNTOS_MINIMOS, traza=False):
    visitado = [[False] * N for _ in range(N)]
    visitado[INICIO[0]][INICIO[1]] = True
    camino = [INICIO]
    est = {'nodos': 0, 'rechazados': 0}

    exito = buscar_salida(
        INICIO[0], INICIO[1], puntos_de('I'),
        camino, visitado, minimo, est, traza
    )

    return exito, camino, est


def matriz_solucion(camino):
    matriz = [
        ['.' if x != 0 else 0 for x in fila]
        for fila in LABERINTO
    ]

    for k in range(len(camino) - 1):
        (f, c), (g, d) = camino[k], camino[k + 1]
        flecha = next(
            fl for df, dc, fl, _ in MOVIMIENTOS
            if (f + df, c + dc) == (g, d)
        )
        matriz[f][c] = flecha

    matriz[INICIO[0]][INICIO[1]] = 'I'
    matriz[META[0]][META[1]] = 'F'

    return matriz


def main():
    ap = argparse.ArgumentParser(
        description='El ratón en el laberinto (backtracking)'
    )
    ap.add_argument(
        '--minimo', type=int, default=PUNTOS_MINIMOS,
        help='puntos mínimos exigidos al llegar a F (por defecto 23)'
    )
    ap.add_argument(
        '--traza', action='store_true',
        help='mostrar cada avance y retroceso del algoritmo'
    )
    args = ap.parse_args()

    print('=' * 52)
    print('   EL RATÓN EN EL LABERINTO - BACKTRACKING')
    print('=' * 52)

    mostrar_matriz(
        LABERINTO, 'LABERINTO ORIGINAL (I = inicio, F = llegada):'
    )

    print(
        f'Inicio I = {INICIO}   Llegada F = {META}   '
        f'Puntos mínimos = {args.minimo}\n'
    )

    if args.traza:
        print('PROCESO DE BÚSQUEDA:')

    exito, camino, est = resolver(args.minimo, args.traza)

    if args.traza:
        print()

    if exito:
        puntos = sum(
            puntos_de(LABERINTO[f][c])
            for f, c in camino
        )

        print(
            f'✔ ¡EL RATÓN LOGRÓ SALIR! Puntos acumulados: {puntos} '
            f'(mínimo exigido: {args.minimo})'
        )

        mostrar_matriz(
            matriz_solucion(camino),
            'MATRIZ CON EL CAMINO A TOMAR:'
        )

        print('Recorrido (fila, columna):')
        print(textwrap.fill(
            ' -> '.join(f'({f},{c})' for f, c in camino),
            width=76
        ))

        bonos = [
            (f, c, LABERINTO[f][c])
            for f, c in camino
            if puntos_de(LABERINTO[f][c])
        ]

        print(
            '\nCeldas con puntos recogidas:',
            ', '.join(f'({f},{c})={v}' for f, c, v in bonos)
        )
        print(f'Pasos: {len(camino) - 1}')

    else:
        print(
            f'✘ EL RATÓN NO LOGRÓ SALIR: ningún camino de I a F '
            f'alcanza {args.minimo} puntos.'
        )

    print(
        f'\nEstadísticas: {est["nodos"]} celdas visitadas en la búsqueda, '
        f'{est["rechazados"]} caminos llegaron a F pero con pocos puntos.'
    )


if __name__ == '__main__':
    main()
