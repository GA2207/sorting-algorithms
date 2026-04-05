import streamlit as st
import random
import time
import plotly.graph_objects as go
import plotly.express as px
from sorting import ALGORITHMS, Stats

st.set_page_config(page_title="Les Papyrus de Heron", page_icon="📜", layout="wide")

st.title("📜 Les Papyrus de Heron")
st.subheader("Outil de tri automatise - Interface Web")

# ======================== SIDEBAR ========================
st.sidebar.header("Configuration")

mode = st.sidebar.radio("Mode", ["Tri manuel", "Benchmark", "Courbes multi-tailles", "Compteur d'operations"])

# ======================== TRI MANUEL ========================
if mode == "Tri manuel":
    st.header("Tri manuel")

    col1, col2 = st.columns(2)
    with col1:
        algo_choix = st.selectbox("Algorithme", [name for _, (name, _) in ALGORITHMS.items()])
    with col2:
        ordre = st.radio("Ordre", ["Croissant", "Decroissant"], horizontal=True)

    input_mode = st.radio("Type de liste", ["Saisie manuelle", "Liste aleatoire"], horizontal=True)

    if input_mode == "Saisie manuelle":
        raw = st.text_input("Entrez des nombres separes par des espaces", "5 3 8 1 9 2 7 4 6 10")
        try:
            lst = [float(x) for x in raw.strip().split()]
        except ValueError:
            st.error("Entrez uniquement des nombres valides.")
            lst = []
    else:
        taille = st.slider("Taille de la liste", 10, 1000, 100)
        lst = [random.randint(1, 10000) for _ in range(taille)]
        st.code(f"Liste generee : {lst[:20]}{'...' if len(lst) > 20 else ''}")

    if lst and st.button("Trier", type="primary"):
        # trouver la fonction de tri
        sort_func = None
        for key, (name, func) in ALGORITHMS.items():
            if name == algo_choix:
                sort_func = func
                break

        copie = lst.copy()
        stats = Stats()
        start = time.time()
        result = sort_func(copie, stats)
        temps = time.time() - start

        if ordre == "Decroissant":
            result = result[::-1]

        col1, col2, col3 = st.columns(3)
        col1.metric("Temps", f"{temps:.6f}s")
        col2.metric("Comparaisons", f"{stats.comparaisons:,}")
        col3.metric("Echanges", f"{stats.echanges:,}")

        st.subheader("Resultat")
        if len(result) <= 50:
            st.write(f"**Input** : {lst}")
            st.write(f"**Output** : {result}")
        else:
            st.write(f"**Input** : {lst[:20]}... ({len(lst)} elements)")
            st.write(f"**Output** : {result[:20]}... ({len(result)} elements)")

        # graphique avant/apres
        fig = go.Figure()
        fig.add_trace(go.Bar(y=lst, name="Avant", marker_color="indianred", opacity=0.6))
        fig.add_trace(go.Bar(y=result, name="Apres", marker_color="lightseagreen", opacity=0.6))
        fig.update_layout(title=f"{algo_choix} - Avant / Apres", barmode="group", height=400)
        st.plotly_chart(fig, use_container_width=True)


# ======================== BENCHMARK ========================
elif mode == "Benchmark":
    st.header("Benchmark - Comparaison des performances")

    taille = st.slider("Taille de la liste", 100, 20000, 10000, step=100)

    if st.button("Lancer le benchmark", type="primary"):
        grosse_liste = [random.randint(1, 100000) for _ in range(taille)]

        resultats = []
        stats_all = []
        progress = st.progress(0)

        for i, (key, (name, sort_func)) in enumerate(ALGORITHMS.items()):
            liste_copie = grosse_liste.copy()
            stats = Stats()
            start = time.time()
            sort_func(liste_copie, stats)
            temps = time.time() - start
            resultats.append((name, temps))
            stats_all.append((name, stats))
            progress.progress((i + 1) / len(ALGORITHMS))

        resultats.sort(key=lambda x: x[1])

        # diagramme en barres
        noms = [r[0] for r in resultats]
        temps_list = [r[1] for r in resultats]

        fig = px.bar(x=noms, y=temps_list, color=noms,
                     labels={"x": "Algorithme", "y": "Temps (secondes)"},
                     title=f"Comparaison des performances ({taille} elements)")
        fig.update_layout(showlegend=False, height=500)
        st.plotly_chart(fig, use_container_width=True)

        # tableau
        st.subheader("Resultats detailles")
        for i, (name, temps) in enumerate(resultats, 1):
            stats = next(s for n, s in stats_all if n == name)
            st.write(f"**{i}. {name}** : {temps:.6f}s | Comparaisons: {stats.comparaisons:,} | Echanges: {stats.echanges:,}")

        plus_rapide = resultats[0]
        plus_lent = resultats[-1]
        if plus_rapide[1] > 0:
            ratio = plus_lent[1] / plus_rapide[1]
            st.success(f"{plus_rapide[0]} est environ {ratio:.0f}x plus rapide que {plus_lent[0]}")


# ======================== COURBES MULTI-TAILLES ========================
elif mode == "Courbes multi-tailles":
    st.header("Evolution du temps selon la taille")

    tailles = st.multiselect(
        "Tailles a tester",
        [100, 250, 500, 1000, 2000, 3000, 5000, 7500, 10000],
        default=[100, 500, 1000, 2000, 5000]
    )

    if tailles and st.button("Lancer l'analyse", type="primary"):
        tailles.sort()
        resultats = {name: [] for _, (name, _) in ALGORITHMS.items()}

        progress = st.progress(0)
        total = len(tailles) * len(ALGORITHMS)
        count = 0

        for taille in tailles:
            grosse_liste = [random.randint(1, 100000) for _ in range(taille)]
            for key, (name, sort_func) in ALGORITHMS.items():
                liste_copie = grosse_liste.copy()
                start = time.time()
                sort_func(liste_copie)
                temps = time.time() - start
                resultats[name].append(temps)
                count += 1
                progress.progress(count / total)

        # graphique courbes
        fig = go.Figure()
        for name, temps_list in resultats.items():
            fig.add_trace(go.Scatter(x=tailles, y=temps_list, mode="lines+markers", name=name))

        fig.update_layout(
            title="Evolution du temps de tri selon la taille de la liste",
            xaxis_title="Nombre d'elements",
            yaxis_title="Temps (secondes)",
            height=600
        )
        st.plotly_chart(fig, use_container_width=True)


# ======================== COMPTEUR D'OPERATIONS ========================
elif mode == "Compteur d'operations":
    st.header("Compteur de comparaisons et d'echanges")

    taille = st.slider("Taille de la liste", 100, 10000, 1000, step=100)

    if st.button("Analyser", type="primary"):
        grosse_liste = [random.randint(1, 100000) for _ in range(taille)]

        noms = []
        comparaisons = []
        echanges = []

        progress = st.progress(0)
        for i, (key, (name, sort_func)) in enumerate(ALGORITHMS.items()):
            liste_copie = grosse_liste.copy()
            stats = Stats()
            sort_func(liste_copie, stats)
            noms.append(name)
            comparaisons.append(stats.comparaisons)
            echanges.append(stats.echanges)
            progress.progress((i + 1) / len(ALGORITHMS))

        # graphique comparaisons
        fig1 = px.bar(x=noms, y=comparaisons, color=noms,
                      labels={"x": "Algorithme", "y": "Nombre de comparaisons"},
                      title=f"Nombre de comparaisons ({taille} elements)")
        fig1.update_layout(showlegend=False, height=450)
        st.plotly_chart(fig1, use_container_width=True)

        # graphique echanges
        fig2 = px.bar(x=noms, y=echanges, color=noms,
                      labels={"x": "Algorithme", "y": "Nombre d'echanges"},
                      title=f"Nombre d'echanges ({taille} elements)")
        fig2.update_layout(showlegend=False, height=450)
        st.plotly_chart(fig2, use_container_width=True)

        # tableau recap
        st.subheader("Tableau recapitulatif")
        for i in range(len(noms)):
            st.write(f"**{noms[i]}** : {comparaisons[i]:,} comparaisons | {echanges[i]:,} echanges")
