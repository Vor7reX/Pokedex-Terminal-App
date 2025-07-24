import requests
import os
import ascii_magic
from colorama import init, Fore, Style

# Inizializza colorama
init(autoreset=True)

# --- Funzioni di Supporto ---

def print_stat_bar(stat_name, stat_value):
    """Stampa una barra di stato visiva e colorata."""
    if stat_value < 50: color = Fore.RED
    elif stat_value < 100: color = Fore.YELLOW
    else: color = Fore.GREEN
    
    bar_length = int((stat_value / 255) * 25)
    bar = '█' * bar_length + ' ' * (25 - bar_length)
    print(f"  {stat_name.ljust(15)}: {str(stat_value).ljust(3)} |{color}{bar}{Style.RESET_ALL}|")

def get_pokedex_description(species_data):
    """Estrae la prima descrizione in inglese disponibile dal JSON della specie."""
    for entry in species_data.get('flavor_text_entries', []):
        if entry['language']['name'] == 'en':
            return entry['flavor_text'].replace('\n', ' ').replace('\f', ' ')
    return "N/A"

def parse_gender_ratio(gender_rate):
    """Converte il gender_rate dell'API in un formato leggibile."""
    if gender_rate == -1:
        return "Senza sesso"
    female_perc = (gender_rate / 8) * 100
    male_perc = 100 - female_perc
    return f"M: {male_perc}% | F: {female_perc}%"

def parse_evolution_chain(chain_data):
    """Analizza ricorsivamente la catena evolutiva e la formatta in una stringa leggibile."""
    evolutions = []
    current_stage = chain_data['chain']
    
    while current_stage:
        species_name = current_stage['species']['name'].capitalize()
        evolutions.append(species_name)
        
        if current_stage['evolves_to']:
            details = current_stage['evolves_to'][0]['evolution_details'][0]
            trigger = details['trigger']['name'].replace('-', ' ')
            evolution_info = f" ({trigger.title()}"
            if details.get('min_level'):
                evolution_info += f" Lvl {details['min_level']}"
            if details.get('item'):
                evolution_info += f", {details['item']['name'].replace('-', ' ').title()}"
            evolution_info += ")"
            evolutions.append(Fore.YELLOW + "-->" + evolution_info)
            
            current_stage = current_stage['evolves_to'][0]
        else:
            break
            
    return " ".join(evolutions)

# --- Funzione Principale ---

def get_pokemon_data(pokemon_name):
    os.system('cls' if os.name == 'nt' else 'clear')
    pokemon_name = pokemon_name.lower()
    
    print(Fore.YELLOW + f"Ricerca di '{pokemon_name}'...")
    
    try:
        main_res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}")
        if main_res.status_code != 200:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(Fore.RED + f"Errore: Pokémon '{pokemon_name}' non trovato.")
            input(Fore.CYAN + "\nPremi Invio per continuare...")
            return
        main_data = main_res.json()

        species_res = requests.get(main_data['species']['url'])
        species_data = species_res.json()

        evo_res = requests.get(species_data['evolution_chain']['url'])
        evo_data = evo_res.json()

    except requests.exceptions.RequestException:
        print(Fore.RED + "Errore di connessione. Controlla la tua connessione a internet.")
        return

    os.system('cls' if os.name == 'nt' else 'clear')

    if main_data['sprites']['other']['official-artwork']['front_default']:
        try:
            output = ascii_magic.from_url(main_data['sprites']['other']['official-artwork']['front_default'])
            output.to_terminal(columns=50)
        except Exception:
            pass 

    print(Style.BRIGHT + Fore.YELLOW + f"\n--- {main_data['name'].upper()} | #{main_data['id']:03} ---")
    description = get_pokedex_description(species_data)
    print(Fore.CYAN + f'\n"{description}"')
    print(Style.BRIGHT + Fore.WHITE + "\n--- General Info ---")
    types = [t['type']['name'].capitalize() for t in main_data['types']]
    print(f"  {'Tipo'.ljust(18)}: {', '.join(types)}")
    print(f"  {'Altezza'.ljust(18)}: {main_data['height'] / 10} m")
    print(f"  {'Peso'.ljust(18)}: {main_data['weight'] / 10} kg")
    print(f"  {'Esperienza Base'.ljust(18)}: {main_data.get('base_experience', 'N/A')}")
    print(Style.BRIGHT + Fore.WHITE + "\n--- Breeding & Growth ---")
    egg_groups = [g['name'].capitalize() for g in species_data.get('egg_groups', [])]
    print(f"  {'Gruppi Uova'.ljust(18)}: {', '.join(egg_groups)}")
    gender_ratio = parse_gender_ratio(species_data.get('gender_rate', -1))
    print(f"  {'Rapporto Sesso'.ljust(18)}: {gender_ratio}")
    print(f"  {'Tasso di Cattura'.ljust(18)}: {species_data.get('capture_rate', 'N/A')}")
    growth_rate = species_data.get('growth_rate', {}).get('name', 'n/a').replace('-', ' ')
    print(f"  {'Tasso di Crescita'.ljust(18)}: {growth_rate.title()}")
    print(Style.BRIGHT + Fore.WHITE + "\n--- Evolution Chain ---")
    evolution_line = parse_evolution_chain(evo_data)
    print(f"  {evolution_line}")
    print(Style.BRIGHT + Fore.WHITE + "\n--- Base Stats ---")
    for stat in main_data['stats']:
        stat_name = stat['stat']['name'].replace('-', ' ').capitalize()
        base_stat = stat['base_stat']
        print_stat_bar(stat_name, base_stat)
    print(Style.BRIGHT + Fore.YELLOW + "--------------------------\n")


# --- NUOVA FUNZIONE PER IL MENU CON IL TITOLO IN ASCII ART ---
def display_main_menu():
    """Pulisce lo schermo e mostra il menu principale con il titolo in ASCII art."""
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Il tuo ASCII art per il titolo "POKEDEX"
    pokedex_title_art = f"""
{Style.BRIGHT + Fore.RED}
██████╗░░█████╗░██╗░░██╗███████╗██████╗░███████╗██╗░░██╗
██╔══██╗██╔══██╗██║░██╔╝██╔════╝██╔══██╗██╔════╝╚██╗██╔╝
██████╔╝██║░░██║█████═╝░█████╗░░██║░░██║█████╗░░░╚███╔╝░
██╔═══╝░██║░░██║██╔═██╗░██╔══╝░░██║░░██║██╔══╝░░░██╔██╗░
██║░░░░░╚█████╔╝██║░╚██╗███████╗██████╔╝███████╗██╔╝╚██╗
╚═╝░░░░░░╚════╝░╚═╝░░╚═╝╚══════╝╚═════╝░╚══════╝╚═╝░░╚═╝
"""
    
    print(pokedex_title_art)
    print(Style.BRIGHT + Fore.YELLOW + "\n============================================================")
    print(Style.BRIGHT + Fore.CYAN + "      Benvenuto nel Pokédex! Digita 'esci' per terminare.")
    print(Style.BRIGHT + Fore.YELLOW + "============================================================")


# --- LOOP PRINCIPALE MODIFICATO ---
if __name__ == "__main__":
    while True:
        # Mostra il menu ad ogni nuovo inserimento
        display_main_menu()
        
        # Chiede l'input all'utente
        user_input = input(Fore.GREEN + "\nInserisci il nome di un Pokémon > ")
        
        if user_input.lower() == 'esci':
            break
        if user_input:
            get_pokemon_data(user_input)
            # Aggiunge una pausa per permettere all'utente di leggere i dati
            input(Fore.CYAN + "\nPremi Invio per tornare al menu principale...")