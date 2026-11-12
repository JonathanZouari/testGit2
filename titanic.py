"""Interactive Titanic survival dashboard."""

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

DATA_PATH = Path(__file__).resolve().parent / "data" / "titanic.csv"

CLASS_LABELS = {1: "1st", 2: "2nd", 3: "3rd"}
EMBARKED_LABELS = {"C": "Cherbourg", "Q": "Queenstown", "S": "Southampton"}


@st.cache_data
def load_data() -> pd.DataFrame:
    frame = pd.read_csv(DATA_PATH)
    frame["Class"] = frame["Pclass"].map(CLASS_LABELS)
    frame["Port"] = frame["Embarked"].map(EMBARKED_LABELS).fillna("Unknown")
    frame["Outcome"] = frame["Survived"].map({0: "Did not survive", 1: "Survived"})
    frame["Family size"] = frame["SibSp"] + frame["Parch"] + 1
    return frame


def apply_filters(frame: pd.DataFrame) -> pd.DataFrame:
    sexes = st.sidebar.multiselect("Sex", sorted(frame["Sex"].dropna().unique()), default=sorted(frame["Sex"].dropna().unique()))
    classes = st.sidebar.multiselect("Class", ["1st", "2nd", "3rd"], default=["1st", "2nd", "3rd"])
    ports = st.sidebar.multiselect("Port of embarkation", ["Cherbourg", "Queenstown", "Southampton", "Unknown"], default=["Cherbourg", "Queenstown", "Southampton", "Unknown"])

    age_min = int(frame["Age"].min(skipna=True))
    age_max = int(frame["Age"].max(skipna=True))
    age_range = st.sidebar.slider("Age", age_min, age_max, (age_min, age_max))
    include_missing_age = st.sidebar.checkbox("Include passengers with unknown age", value=True)

    fare_min = float(frame["Fare"].min())
    fare_max = float(frame["Fare"].max())
    fare_range = st.sidebar.slider("Fare (£)", fare_min, fare_max, (fare_min, fare_max))

    filtered = frame[
        frame["Sex"].isin(sexes)
        & frame["Class"].isin(classes)
        & frame["Port"].isin(ports)
        & frame["Fare"].between(fare_range[0], fare_range[1])
    ]
    age_match = frame["Age"].between(age_range[0], age_range[1])
    if include_missing_age:
        age_match = age_match | frame["Age"].isna()
    return filtered[age_match.loc[filtered.index]]


def metric_row(frame: pd.DataFrame) -> None:
    passengers = len(frame)
    survival = frame["Survived"].mean() if passengers else 0
    known_age = frame["Age"].dropna()
    left, middle_left, middle_right, right = st.columns(4)
    left.metric("Passengers", f"{passengers:,}")
    middle_left.metric("Survival rate", f"{survival:.1%}")
    middle_right.metric("Average age", f"{known_age.mean():.1f}" if len(known_age) else "—")
    right.metric("Median fare", f"£{frame['Fare'].median():.2f}" if passengers else "—")


def charts(frame: pd.DataFrame) -> None:
    if frame.empty:
        st.info("No passengers match these filters.")
        return

    survival_color = {"Survived": "#2E8B57", "Did not survive": "#C44536"}
    left, right = st.columns(2)

    by_sex = (
        frame.groupby(["Sex", "Outcome"], as_index=False)
        .size()
        .rename(columns={"size": "Passengers"})
    )
    left.plotly_chart(
        px.bar(
            by_sex,
            x="Sex",
            y="Passengers",
            color="Outcome",
            barmode="group",
            color_discrete_map=survival_color,
            title="Survival by sex",
        ),
        use_container_width=True,
    )

    by_class = (
        frame.groupby("Class", as_index=False)["Survived"]
        .mean()
        .rename(columns={"Survived": "Survival rate"})
    )
    by_class["Class"] = pd.Categorical(by_class["Class"], ["1st", "2nd", "3rd"], ordered=True)
    by_class = by_class.sort_values("Class")
    right.plotly_chart(
        px.bar(
            by_class,
            x="Class",
            y="Survival rate",
            text=by_class["Survival rate"].map(lambda value: f"{value:.0%}"),
            color="Class",
            title="Survival rate by class",
        ).update_layout(yaxis_tickformat=".0%", showlegend=False),
        use_container_width=True,
    )

    age_known = frame.dropna(subset=["Age"])
    lower, upper = st.columns(2)
    lower.plotly_chart(
        px.histogram(
            age_known,
            x="Age",
            color="Outcome",
            nbins=20,
            barmode="overlay",
            opacity=0.75,
            color_discrete_map=survival_color,
            title="Age distribution",
        ),
        use_container_width=True,
    )
    upper.plotly_chart(
        px.box(
            frame,
            x="Class",
            y="Fare",
            color="Outcome",
            category_orders={"Class": ["1st", "2nd", "3rd"]},
            color_discrete_map=survival_color,
            title="Fare by class",
        ),
        use_container_width=True,
    )

    by_port = (
        frame.groupby(["Port", "Outcome"], as_index=False)
        .size()
        .rename(columns={"size": "Passengers"})
    )
    st.plotly_chart(
        px.bar(
            by_port,
            x="Port",
            y="Passengers",
            color="Outcome",
            color_discrete_map=survival_color,
            title="Passengers by port of embarkation",
        ),
        use_container_width=True,
    )


def passenger_table(frame: pd.DataFrame) -> None:
    st.subheader("Passengers")
    columns = ["Name", "Sex", "Age", "Class", "Port", "Fare", "Family size", "Outcome"]
    st.dataframe(
        frame[columns].sort_values(["Class", "Name"]),
        use_container_width=True,
        hide_index=True,
    )


def main() -> None:
    st.set_page_config(page_title="Titanic", page_icon="🚢", layout="wide")
    st.title("Titanic survival")
    st.caption("Passenger records from the Kaggle Titanic dataset. Use the sidebar to filter the charts and the table.")

    frame = load_data()
    filtered = apply_filters(frame)
    metric_row(filtered)
    charts(filtered)
    passenger_table(filtered)


if __name__ == "__main__":
    main()
