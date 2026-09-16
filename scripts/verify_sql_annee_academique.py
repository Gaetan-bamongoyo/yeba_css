"""Vérifie la cohérence des données de la mission année académique."""

import os
import sys

import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from collections import defaultdict

from catalog.data.sql_annee_academique import DATASET, FINAL_OFFICIAL_LIST

YEAR = "2025-2026"


def main():
    etudiants = {row["id"]: row for row in DATASET["etudiants"]}
    filieres = {row["id"]: row["nom"] for row in DATASET["filieres"]}
    inscriptions_year = [
        row for row in DATASET["inscriptions"] if row["annee_academique"] == YEAR
    ]

    # Sanity: notes and paiements only reference inscription_id
    for row in DATASET["notes"]:
        assert "inscription_id" in row and "etudiant_id" not in row
    for row in DATASET["paiements"]:
        assert "inscription_id" in row and "etudiant_id" not in row

    notes_by_inscription = defaultdict(list)
    for row in DATASET["notes"]:
        notes_by_inscription[row["inscription_id"]].append(row["note"])

    payments_by_inscription = defaultdict(int)
    for row in DATASET["paiements"]:
        payments_by_inscription[row["inscription_id"]] += row["montant"]

    print("M1 total etudiants:", len(etudiants))
    print("M2 inscriptions 2025-2026:", len(inscriptions_year))

    averages = {}
    for ins in inscriptions_year:
        sid = ins["etudiant_id"]
        student_notes = notes_by_inscription[ins["id"]]
        averages[sid] = sum(student_notes) / len(student_notes)

    avg_pass = [sid for sid in averages if averages[sid] >= 10]
    print("M5 avg >= 10:", len(avg_pass))

    no_elim = []
    for sid in avg_pass:
        ins = next(i for i in inscriptions_year if i["etudiant_id"] == sid)
        if min(notes_by_inscription[ins["id"]]) >= 5:
            no_elim.append(sid)
    print("M6 no note < 5:", len(no_elim))

    admitted = []
    for sid in no_elim:
        ins = next(i for i in inscriptions_year if i["etudiant_id"] == sid)
        total = payments_by_inscription[ins["id"]]
        if total >= 500:
            admitted.append(sid)
    print("M8 admitted:", len(admitted))

    def row_for(sid):
        student = etudiants[sid]
        ins = next(i for i in inscriptions_year if i["etudiant_id"] == sid)
        return {
            "matricule": student["matricule"],
            "nom_complet": f"{student['nom']} {student['postnom']} {student['prenom']}",
            "filiere": filieres[ins["filiere_id"]],
            "promotion": ins["promotion"],
            "moyenne": round(averages[sid], 2),
            "total_paye": payments_by_inscription[ins["id"]],
        }

    computed = sorted(
        [row_for(sid) for sid in admitted],
        key=lambda r: (r["filiere"], -r["moyenne"]),
    )
    print("Computed final list:")
    for row in computed:
        print(" ", row)

    assert len(computed) == len(FINAL_OFFICIAL_LIST)
    for expected, actual in zip(FINAL_OFFICIAL_LIST, computed):
        assert expected["matricule"] == actual["matricule"]
        assert expected["moyenne"] == actual["moyenne"]
        assert expected["total_paye"] == actual["total_paye"]
    print("OK — notes et paiements liés à inscription_id")


if __name__ == "__main__":
    main()
