from partidas import run as run_partidas
from pontuacao import run as run_pontuacao
from mercado import run as run_mercado

def main():
    print("Iniciando pipeline de ingestão...")

    run_partidas()
    run_pontuacao()
    run_mercado()

    print("✅ Ingestão finalizada!")

if __name__ == "__main__":
    main()
    