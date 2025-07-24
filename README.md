# Pokedex Terminal App  Pokédex

<div align="center">
  
 ![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)

 
</div>

A feature-rich, terminal-based Pokedex application written in Python. It uses the PokéAPI to fetch detailed data for any Pokémon and displays it in a beautifully formatted, colorful, and interactive interface.

*// ![Pokedex Demo GIF](assets/pokedex_demo.gif) //*

---

## ✨ Features

* **ASCII Art Display**: Each Pokémon's official artwork is rendered as colorful ASCII art directly in the terminal.
* **Detailed Data**: Fetches and displays a wide range of information, including:
    * Base Stats (with visual bars)
    * Types, Height & Weight
    * Pokédex Descriptions
    * Breeding & Growth data (Egg Groups, Gender Ratio, etc.)
* **Full Evolution Chain**: Dynamically fetches and displays the Pokémon's complete evolution line.
* **Interactive Menu**: A themed, interactive main menu for a polished user experience.
* **Colored Output**: Uses `colorama` for a vibrant and readable interface, with colors that adapt to stats and information type.

---

## 🚀 Tech Stack

* **Python 3.11**
* **Requests**: For making HTTP requests to the PokéAPI.
* **Colorama**: For cross-platform colored terminal text.
* **ascii-magic**: For converting images from URLs into ASCII art.

---

## ⚙️ Setup and Usage

Follow these steps to run the application on your local machine.

### 1. Prerequisites

Make sure you have the following installed:
* [Python](https://www.python.org/) (developed with version 3.13)
* [Git](https://git-scm.com/)

### 2. Clone the Repository

Open your terminal, navigate to the directory where you want to save the project, and run:
```bash
git clone https://github.com/Vor7reX/Pokedex-Terminal-App.git
cd Pokedex-Terminal-App
```

### 3. Create and Activate Virtual Environment

It's highly recommended to use a virtual environment.

```bash
# Create the environment
py -m venv venv

# Activate it (on Windows)
.\venv\Scripts\activate
```

### 4. Install Dependencies

Install all required libraries from the `requirements.txt` file with a single command:
```bash
pip install -r requirements.txt
```

### 5. Run the Application

Once the setup is complete, you can start the Pokedex:
```bash
python pokedex.py
```
Enter a Pokémon name or type `esci` to exit.
