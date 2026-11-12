"""Titanic survival dashboard. Run: streamlit run titanic_dashboard.py"""

from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

DATA = Path(__file__).with_name("data") / "titanic.csv"
SCENE = Path(__file__).with_name("titanic_3d.html")
SHIP = Path(__file__).with_name("assets") / "titanic-departure.jpg"
PAINTING = Path(__file__).with_name("assets") / "titanic-stower.jpg"
SEX = {"male": "Male", "female": "Female"}
EMBARKED = {"C": "Cherbourg", "Q": "Queenstown", "S": "Southampton", "Unknown": "Unknown"}
PARTY = {"alone": "Alone", "family": "With family"}
CABIN = {"known": "Recorded", "unknown": "Not recorded"}
OUTCOME = {1: "Survived", 0: "Died"}
AGE_LABELS = ["0–10", "11–20", "21–30", "31–40", "41–50", "51–60", "61–80"]
GOLD = "#d4af37"
ICE = "#9ec3db"
CREAM = "#f4efe4"
DIED = "#5d7388"
CARD = "#102033"


def prepare(df):
    out = df.copy()
    out["Embarked"] = out["Embarked"].fillna("Unknown")
    out["Fare"] = out["Fare"].fillna(0)
    out["party"] = (out["SibSp"].fillna(0) + out["Parch"].fillna(0)).gt(0).map({True: "family", False: "alone"})
    out["cabin_known"] = out["Cabin"].fillna("").str.strip().ne("").map({True: "known", False: "unknown"})
    return out


def apply_filters(df, sexes, classes, ports, ages, keep_missing_age, outcomes, fares, parties, cabins):
    out = df[
        df["Sex"].isin(sexes)
        & df["Pclass"].isin(classes)
        & df["Embarked"].isin(ports)
        & df["Survived"].isin(outcomes)
        & df["Fare"].between(fares[0], fares[1])
        & df["party"].isin(parties)
        & df["cabin_known"].isin(cabins)
    ]
    known_age = out["Age"].between(ages[0], ages[1])
    return out[known_age | (out["Age"].isna() if keep_missing_age else False)]


def themed(chart, height=280):
    return (
        chart.properties(height=height, background=CARD)
        .configure_view(strokeWidth=0)
        .configure_axis(
            labelColor=CREAM,
            titleColor=GOLD,
            gridColor="#1b3348",
            domainColor="#1b3348",
            labelFontSize=12,
        )
        .configure_legend(labelColor=CREAM, title=None, orient="bottom")
    )


def _selfcheck():
    sample = pd.DataFrame(
        {
            "Sex": ["male", "female", "female"],
            "Pclass": [1, 3, 3],
            "Embarked": ["S", "C", "C"],
            "Age": [22.0, None, 40.0],
            "Survived": [0, 1, 1],
            "Fare": [10.0, 20.0, 80.0],
            "party": ["alone", "family", "alone"],
            "cabin_known": ["unknown", "known", "unknown"],
        }
    )
    got = apply_filters(sample, ["female"], [3], ["C"], (0, 30), True, [1], (0, 50), ["family"], ["known"])
    assert len(got) == 1 and pd.isna(got.iloc[0]["Age"])


_selfcheck()

st.set_page_config(page_title="Titanic Survival", page_icon="⚓", layout="wide", initial_sidebar_state="expanded")
st.markdown(
    """
    <style>
    .stApp { background: #071422; color: #f4efe4; }
    header[data-testid="stHeader"] { background: transparent; }
    [data-testid="stSidebar"] { background: #0c1928; border-right: 1px solid rgba(212,175,55,.45); }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p { color: #f4efe4 !important; }
    [data-testid="stMetric"] {
      background: linear-gradient(180deg, #16304a 0%, #102033 100%);
      border: 1px solid rgba(212,175,55,.35);
      border-top: 3px solid #d4af37;
      padding: 12px 16px 8px;
      border-radius: 4px;
    }
    [data-testid="stMetricLabel"] { color: #d4af37 !important; letter-spacing: .06em; text-transform: uppercase; }
    [data-testid="stMetricValue"], [data-testid="stMetricDelta"] { color: #f4efe4 !important; }
    h1, h2, h3 { color: #f4efe4 !important; font-family: Georgia, "Palatino Linotype", serif; }
    [data-testid="stCaptionContainer"] p { color: #c9b896 !important; }
    [data-testid="stVegaLiteChart"] { border: 1px solid rgba(212,175,55,.28); border-radius: 4px; }
    </style>
    """,
    unsafe_allow_html=True,
)

df = prepare(pd.read_csv(DATA))
fare_max = int(df["Fare"].max()) + 1
ship_rate = df["Survived"].mean()

with st.sidebar:
    st.header("Filters")
    st.caption("Every tile on the page uses this selection.")
    sexes = st.multiselect("Sex", list(SEX), default=list(SEX), format_func=SEX.get)
    outcomes = st.multiselect("Outcome", list(OUTCOME), default=list(OUTCOME), format_func=OUTCOME.get)
    parties = st.multiselect("Travel party", list(PARTY), default=list(PARTY), format_func=PARTY.get)
    cabins = st.multiselect("Cabin on the manifest", list(CABIN), default=list(CABIN), format_func=CABIN.get)
    st.divider()
    classes = st.multiselect("Class", [1, 2, 3], default=[1, 2, 3], format_func=lambda c: f"Class {c}")
    ports = st.multiselect("Port of embarkation", list(EMBARKED), default=list(EMBARKED), format_func=EMBARKED.get)
    ages = st.slider("Age", 0, 80, (0, 80))
    keep_missing_age = st.checkbox("Include passengers with unknown age", value=True)
    fares = st.slider("Fare", 0, fare_max, (0, fare_max))

view = apply_filters(df, sexes, classes, ports, ages, keep_missing_age, outcomes, fares, parties, cabins)

st.title("Titanic Survival")
st.write(
    "Passenger-level survival for the 1912 voyage. Filter the ship, then compare the selection with everyone on board."
)
photo, painting = st.columns(2, gap="large")
photo.image(str(SHIP), use_container_width=True, caption="RMS Titanic leaving Southampton, 10 April 1912. Public domain.")
painting.image(str(PAINTING), use_container_width=True, caption="Willy Stöwer, Untergang der Titanic, 1912. Public domain.")
components.html(SCENE.read_text(encoding="utf-8"), height=400)

if view.empty:
    st.warning("No passengers match these filters.")
    st.stop()

rate = view["Survived"].mean()
survived = int(view["Survived"].sum())
died = len(view) - survived
median_age = view["Age"].median()
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Aboard", f"{len(view):,}")
k2.metric("Survived", f"{survived:,}")
k3.metric("Died", f"{died:,}")
k4.metric("Rate", f"{rate:.1%}", f"{rate - ship_rate:+.1%} vs all")
k5.metric("Median age", "—" if pd.isna(median_age) else f"{median_age:.0f}")

st.subheader("Survival")
st.caption("First-class women survived far more often than men in third class. The grouped bars show that cut directly.")
by_class = (
    view.groupby("Pclass")["Survived"].mean().mul(100).round(1).rename("rate").reset_index()
)
by_class["class"] = by_class["Pclass"].map(lambda c: f"Class {c}")
by_sex = view.groupby("Sex")["Survived"].mean().mul(100).round(1).rename("rate").reset_index()
by_sex["sex"] = by_sex["Sex"].map(SEX)
left, right = st.columns(2)
left.altair_chart(
    themed(
        alt.Chart(by_class)
        .mark_bar(color=GOLD, cornerRadiusTopLeft=2, cornerRadiusTopRight=2)
        .encode(
            x=alt.X("class:N", title=None, sort=["Class 1", "Class 2", "Class 3"]),
            y=alt.Y("rate:Q", title="Survival %", scale=alt.Scale(domain=[0, 100])),
            tooltip=[alt.Tooltip("class:N", title="Class"), alt.Tooltip("rate:Q", format=".1f", title="Survival %")],
        )
    ),
    use_container_width=True,
)
right.altair_chart(
    themed(
        alt.Chart(by_sex)
        .mark_bar(color=ICE, cornerRadiusTopLeft=2, cornerRadiusTopRight=2)
        .encode(
            x=alt.X("sex:N", title=None, sort=["Female", "Male"]),
            y=alt.Y("rate:Q", title="Survival %", scale=alt.Scale(domain=[0, 100])),
            tooltip=[alt.Tooltip("sex:N", title="Sex"), alt.Tooltip("rate:Q", format=".1f", title="Survival %")],
        )
    ),
    use_container_width=True,
)

matrix = view.groupby(["Pclass", "Sex"], as_index=False)["Survived"].mean()
matrix["rate"] = matrix["Survived"] * 100
matrix["class"] = matrix["Pclass"].map(lambda c: f"Class {c}")
matrix["sex"] = matrix["Sex"].map(SEX)
st.altair_chart(
    themed(
        alt.Chart(matrix)
        .mark_bar(cornerRadiusTopLeft=2, cornerRadiusTopRight=2)
        .encode(
            x=alt.X("class:N", title=None, sort=["Class 1", "Class 2", "Class 3"]),
            xOffset="sex:N",
            y=alt.Y("rate:Q", title="Survival %", scale=alt.Scale(domain=[0, 100])),
            color=alt.Color(
                "sex:N",
                sort=["Female", "Male"],
                scale=alt.Scale(domain=["Female", "Male"], range=[GOLD, ICE]),
            ),
            tooltip=[
                alt.Tooltip("class:N", title="Class"),
                alt.Tooltip("sex:N", title="Sex"),
                alt.Tooltip("rate:Q", format=".1f", title="Survival %"),
            ],
        ),
        height=320,
    ),
    use_container_width=True,
)

st.subheader("Who was aboard")
aged = view.dropna(subset=["Age"]).copy()
band_col, port_col = st.columns(2)
if aged.empty:
    band_col.info("No recorded ages in this selection.")
else:
    aged["band"] = pd.cut(aged["Age"], bins=[0, 10, 20, 30, 40, 50, 60, 80], labels=AGE_LABELS)
    aged["outcome"] = aged["Survived"].map(OUTCOME)
    bands = aged.groupby(["band", "outcome"], observed=False).size().reset_index(name="passengers")
    bands["band"] = bands["band"].astype(str)
    band_col.altair_chart(
        themed(
            alt.Chart(bands)
            .mark_bar()
            .encode(
                x=alt.X("band:N", sort=AGE_LABELS, title=None),
                y=alt.Y("passengers:Q", stack="zero", title="Passengers"),
                color=alt.Color(
                    "outcome:N",
                    sort=["Survived", "Died"],
                    scale=alt.Scale(domain=["Survived", "Died"], range=[GOLD, DIED]),
                ),
                tooltip=["band", "outcome", "passengers"],
            )
        ),
        use_container_width=True,
    )

by_port = view.groupby("Embarked")["Survived"].mean().mul(100).round(1).rename("rate").reset_index()
by_port["port"] = by_port["Embarked"].map(EMBARKED)
port_col.altair_chart(
    themed(
        alt.Chart(by_port)
        .mark_bar(color=GOLD, cornerRadiusTopLeft=2, cornerRadiusTopRight=2)
        .encode(
            x=alt.X("port:N", title=None, sort=["Cherbourg", "Queenstown", "Southampton", "Unknown"]),
            y=alt.Y("rate:Q", title="Survival %", scale=alt.Scale(domain=[0, 100])),
            tooltip=[alt.Tooltip("port:N", title="Port"), alt.Tooltip("rate:Q", format=".1f", title="Survival %")],
        )
    ),
    use_container_width=True,
)

st.subheader("Passenger list")
st.caption(f"{len(view):,} of {len(df):,} passengers. Use the table search to find a name.")
show = view.assign(
    Sex=view["Sex"].map(SEX),
    Class=view["Pclass"],
    Port=view["Embarked"].map(EMBARKED),
    Party=view["party"].map(PARTY),
    Outcome=view["Survived"].map(OUTCOME),
)[["Name", "Sex", "Class", "Age", "Fare", "Port", "Party", "Outcome"]]
st.dataframe(
    show,
    use_container_width=True,
    height=380,
    hide_index=True,
    column_config={
        "Age": st.column_config.NumberColumn("Age", format="%.0f"),
        "Fare": st.column_config.NumberColumn("Fare", format="%.2f"),
    },
)
