
# Streamlit App : Outil personnalisé pour le Multi en 4
import streamlit as st
import itertools
import pandas as pd

st.set_page_config(page_title="Combinaisons Multi en 4", layout="wide")
st.title("🎯 Outil Multi en 4 - Turf Optimisateur")
st.markdown("Ce simulateur gère vos combinaisons hippiques en fonction des cotes, performances récentes (musique) et de la forme des chevaux.")

# Chargement manuel des chevaux
data = st.text_area("Entrez les données des chevaux (nom, cote, musique, forme) :", 
    '''Cheval A,4.1,1p2p3p,8
Cheval B,5.5,0p0p2p,6
Cheval C,10.0,3p3p1p,7
Cheval D,3.8,2p1p1p,9
Cheval E,13.0,5p4p6p,4
Cheval F,7.2,4p2p3p,6
Cheval G,18.0,0p9p0p,2
Cheval H,2.9,1p1p2p,10
Cheval I,8.5,3p5p4p,5
Cheval J,12.0,4p7p6p,3''')

if data:
    lignes = data.strip().split("\n")
    chevaux = []
    for ligne in lignes:
        try:
            nom, cote, musique, forme = ligne.split(",")
            chevaux.append({"nom": nom.strip(), "cote": float(cote), "musique": musique.strip(), "forme": int(forme)})
        except ValueError:
            st.warning(f"Format invalide pour la ligne : {ligne}")

    def calculer_score(cheval):
        score_cote = max(0, 20 - cheval["cote"])
        score_musique = sum([5 - int(p[0]) if p[0].isdigit() else 0 for p in cheval["musique"].split("p") if p])
        return score_cote + score_musique + cheval["forme"]

    import pandas as pd
    df = pd.DataFrame(chevaux)
    df["score"] = df.apply(calculer_score, axis=1)
    df = df.sort_values(by="score", ascending=False).reset_index(drop=True)

    st.subheader("🏆 Classement des chevaux (Top 8)")
    st.dataframe(df.head(8))

    top_chevaux = df.head(8)
    combinaisons = list(itertools.combinations(top_chevaux["nom"], 4))

    resultats = []
    for combinaison in combinaisons:
        score_total = sum(top_chevaux[top_chevaux["nom"].isin(combinaison)]["score"])
        resultats.append({"combinaison": ", ".join(combinaison), "score_total": score_total})

    df_resultats = pd.DataFrame(resultats).sort_values(by="score_total", ascending=False)

    st.subheader("🔹 Meilleures combinaisons optimisées")
    st.dataframe(df_resultats.head(20))
