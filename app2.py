import streamlit as st
import stanza

# Lataa Stanza vain kerran
if "nlp" not in st.session_state:
    stanza.download('fi')
    st.session_state.nlp = stanza.Pipeline(lang='fi', processors='tokenize,lemma')

nlp = st.session_state.nlp

# Komponentit ryhmittäin
ryhmat = {
    "Vitamiinit": ["A-vitamiini", "B1", "B2", "B6", "B12", "C-vitamiini", "D-vitamiini", "E-vitamiini", "K-vitamiini", "folaatti", "niasiini", "karotenoidit"],
    "Kivennäisaineet": ["kalsium", "rauta", "sinkki", "jodi", "magnesium", "natrium", "fosfori", "seleeni", "kalium"],
    "Makroravinteet": ["energia", "rasva", "proteiini", "hiilihydraatti", "alkoholi"],
    "Rasvahapot": ["EPA", "DHA", "linolihappo", "alfalinoleenihappo", "trans", "n-3", "n-6"],
    "Sokerit": ["glukoosi", "fruktoosi", "galaktoosi", "laktoosi", "sakkaroosi", "maltoosi"],
    "Muut": ["tryptofaani", "kolesteroli", "sterolit", "kuitu"]
}

# 🔍 Valitse ryhmä
valittu_ryhma = st.selectbox("Valitse komponenttiryhmä", list(ryhmat.keys()))
komponentit = ryhmat[valittu_ryhma]

# 📋 Näytä kaikki komponentit collapsible-tyylillä
with st.expander("📋 Näytä kaikki komponentit"):
    kaikki = [item for sublist in ryhmat.values() for item in sublist]
    st.write(", ".join(kaikki))

# 📝 Syötä hakusana
hakusana = st.text_input("🔍 Syötä hakusana (taivutusmuoto sallittu)")

# 🔍 Lemmatointi ja haku
if hakusana:
    doc = nlp(hakusana)
    lemmat = {word.lemma.lower() for sentence in doc.sentences for word in sentence.words}
    osumat = [k for k in komponentit if any(l in k.lower() for l in lemmat)]
    if osumat:
        st.success(f"Löytyi {len(osumat)} osumaa:")
        for o in osumat:
            st.write(f"• {o}")
    else:
        st.warning("Ei osumia. Kokeile toista muotoa tai ryhmää.")

st.markdown("---")
st.caption("Tietolähde: komponentit-data2.pdf")

