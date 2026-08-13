import os
import sys
import shutil
import subprocess
from pathlib import Path
from decouple import config

# --- CONFIGURAÇÃO DE SEGURANÇA ---
FORCAR = False


def resetar_projeto():
    print("⚠️  ATENÇÃO: Este script vai apagar as migrations locais e resetar o banco de dados!")

    if not FORCAR:
        confirmacao = input("Tem certeza que deseja continuar? (digite 's' para confirmar): ")
        if confirmacao.lower() != 's':
            print("❌ Operação cancelada pelo usuário.")
            sys.exit(0)

    # CORREÇÃO DA PASTA: Como o script está em 'tools/', subimos 2 níveis para chegar à raiz
    BASE_DIR = Path(__file__).resolve().parent.parent

    print(f"🎯 Raiz detectada do projeto: {BASE_DIR}")

    # 1. Limpando os arquivos de Migrations locais
    print("\n🧹 Apagando arquivos de migrations...")
    contador_migrations = 0

    for path in BASE_DIR.rglob('migrations'):
        # PROTEÇÃO CRÍTICA: Ignora completamente qualquer pasta de ambiente virtual (.venv ou venv)
        if ".venv" in path.parts or "venv" in path.parts:
            continue

        if path.is_dir():
            for arquivo in path.iterdir():
                # Mantém apenas o __init__.py e ignora a pasta __pycache__
                if arquivo.is_file() and arquivo.name != '__init__.py':
                    try:
                        arquivo.unlink()
                        contador_migrations += 1
                    except Exception as e:
                        print(f"Não foi possível apagar {arquivo}: {e}")

            # Limpa o cache do python da pasta migrations local
            pycache = path / '__pycache__'
            if pycache.exists():
                shutil.rmtree(pycache)

    print(f"   -> {contador_migrations} arquivos de migração locais removidos.")

    # 2. Deletando/Resetando o Banco de Dados na Raiz
    db_path = BASE_DIR / "db.sqlite3"

    if db_path.exists():
        print("\n🗄️  Apagando o banco de dados SQLite...")
        try:
            db_path.unlink()
            print("   -> Banco db.sqlite3 deletado com sucesso.")
        except Exception as e:
            print(f"❌ Erro ao deletar o banco: {e}")
            exit(0)
    else:
        print("\nℹ️  Banco db.sqlite3 não encontrado localmente na raiz.")

    print("\n✅ Sistema resetado com sucesso e pronto para uso!")

    # 3. Gerando e aplicando migrações
    print("\n🔄 Gerando migrações...")
    subprocess.run(["task", "makemigrations"], cwd=BASE_DIR, check=True)
    
    print("\n🔄 Aplicando migrações...")
    subprocess.run(["task", "migrate"], cwd=BASE_DIR, check=True)
    
    print("\n✅ Migrações geradas e aplicadas com sucesso!")

    # 4. Restaurando as Fixtures (Backup)
    print("\n📥 Restaurando dados das fixtures...")

    # NOME_FIXTURE = "users_profiles_v2"
    # fixture_path = BASE_DIR / "user" / "fixtures" / f"{NOME_FIXTURE}.json"
    NOME_FIXTURE = "base_data"
    fixture_path = BASE_DIR / "cdr" / "fixtures" / f"{NOME_FIXTURE}.json"
    fixture_restaurada = False

    try:
        # Executa o loaddata capturando a saída para analise
        resultado = subprocess.run(
            ["uv", "run", "manage.py", "loaddata", str(fixture_path), "--ignorenonexistent"],
            cwd=BASE_DIR,
            check=True,
            capture_output=True,
            text=True
        )
        print(resultado.stdout)
        if "Installed 0 object(s)" in resultado.stdout or "No fixture data found" in resultado.stderr:
            print("⚠️ Nenhuma fixture foi instalada (arquivo vazio ou não encontrado).")
        else:
            print("✅ Dados restaurados com sucesso a partir das fixtures!")
            fixture_restaurada = True

    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao tentar restaurar a fixture: {e}")

    # Fallback: Se a fixture NÃO foi restaurada com sucesso, cria o superusuário
    if not fixture_restaurada:
        print("\n👤 Fixture não restaurada. Criando superusuário padrão...")
        try:
            subprocess.run(
                ["task", "createsuperuser"],
                cwd=BASE_DIR,
                env={
                    **os.environ,
                    "DJANGO_SUPERUSER_EMAIL": config("DJANGO_SUPERUSER_EMAIL"),
                    "DJANGO_SUPERUSER_PASSWORD": config("DJANGO_SUPERUSER_PASSWORD"),
                },
                check=True
            )
            print("✅ Superusuário criado com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao criar superusuário: {e}")


if __name__ == "__main__":
    resetar_projeto()
