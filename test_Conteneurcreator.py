import pytest
import platform
import subprocess
from conteneurcreator import is_docker_installed, create_container, container_count

# a) Test de la détection du système d'exploitation
def test_os_detection():
    system = platform.system()
    assert system in ["Linux", "Windows", "Darwin"], "Le système d'exploitation détecté n'est pas supporté."


# b) Test de la vérification de l'installation de Docker
def test_is_docker_installed(monkeypatch):
    # Simuler une exécution réussie de la commande "docker --version"
    def mock_run(*args, **kwargs):
        return subprocess.CompletedProcess(args, 0)
    
    # Utiliser monkeypatch pour remplacer subprocess.run par notre simulation
    monkeypatch.setattr(subprocess, "run", mock_run)
    
    # Docker est installé (mock_returncode == 0)
    assert is_docker_installed() == True

    # Simuler un FileNotFoundError quand Docker n'est pas installé
    def mock_run_file_not_found(*args, **kwargs):
        raise FileNotFoundError
    
    monkeypatch.setattr(subprocess, "run", mock_run_file_not_found)
    
    # Docker n'est pas installé
    assert is_docker_installed() == False


# c) Test de la création d'un conteneur avec simulation d'input
def test_create_container(monkeypatch):

    # Simuler les inputs de l'utilisateur
    inputs = iter(["1", "n"])  # Choix de l'Ubuntu et pas de volume persistant

    # Simuler input() pour remplacer les appels interactifs
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    # Simuler la commande subprocess.run pour éviter d'exécuter réellement des commandes Docker
    def mock_run(*args, **kwargs):
        # Imprimer pour voir si la commande est bien appelée
        print(f"Simulating subprocess.run with args: {args}")
        return subprocess.CompletedProcess(args, 0)

    monkeypatch.setattr(subprocess, 'run', mock_run)

    # Exécuter la fonction create_container
    create_container()

    # Vérifier que le compteur de conteneurs a été incrémenté
    assert container_count == 1
