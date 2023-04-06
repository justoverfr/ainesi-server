import json
import datetime


def open_file(filepath):
    """
    Ouvre un fichier et retourne son contenu.

    Args:
        filepath str: chemin du fichier

    Returns:
        str: contenu du fichier
    """
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


def save_file(filepath, content):
    """
    Enregistre le contenu dans un fichier.
    """
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)


def load_json(filepath):
    """
    Ouvre un fichier json et retourne son contenu.

    Args:
        filepath str: chemin du fichier

    Returns:
        dict: contenu du fichier json
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as infile:
            return json.load(infile)
    except Exception as oops:
        return None


def save_json(filepath, payload):
    """
    Enregistre une charge utile (payload) au format JSON dans un fichier.

    Args:
        filepath (str): Le chemin du fichier dans lequel enregistrer la charge utile.
        payload (dict): Un dictionnaire représentant la charge utile à enregistrer.
    """
    with open(filepath, 'w', encoding='utf-8') as outfile:
        json.dump(payload, outfile, ensure_ascii=False,
                  sort_keys=True, indent=2)


def timestamp_to_datetime(unix_time):
    """
    Convertit un temps Unix en une chaîne de caractères représentant la date et l'heure dans un format spécifique.

    Args:
        unix_time (int): Un temps Unix représentant le nombre de secondes depuis le 1er janvier 1970 à minuit, heure UTC.

    Returns:
        str: Une chaîne de caractères représentant la date et l'heure dans le format suivant : "weekday, month day, year at hour:minuteAM/PM timezone".
            weekday : nom du jour de la semaine (ex: "Monday")
            month : nom du mois (ex: "January")
            day : numéro du jour du mois (ex: "01")
            year : année (ex: "2023")
            hour : heure (format 12 heures) (ex: "01")
            minute : minute (ex: "30")
            AM/PM : indicateur AM ou PM selon l'heure (ex: "PM")
            timezone : fuseau horaire (ex: "UTC")
    """
    return datetime.datetime.fromtimestamp(unix_time).strftime("%A, %B %d, %Y at %I:%M%p %Z")
