"""Fonctions de calendrier."""


def est_bissextile(annee: int) -> bool:
    return annee % 400 == 0 or (annee % 4 == 0 and annee % 100 != 0)
