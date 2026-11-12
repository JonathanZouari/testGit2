# Titanic survival dashboard

Interactive Streamlit view of the 891-passenger Titanic dataset in `data/titanic.csv`.

The page uses a navy-and-gold ship theme. The sidebar filters sex, outcome, travel party, cabin record, class, embarkation port, age, and fare. Cards and charts follow that selection and compare the survival rate with the full ship.

Photos in `assets/` are public-domain images of the ship leaving Southampton and Willy Stöwer's 1912 painting.

Needs `streamlit`, `pandas`, and `altair` (`altair` is installed with Streamlit).

```bash
python -m streamlit run titanic_dashboard.py
```

Streamlit prints the local URL when it starts. The default port is 8501.

`titanic_3d.html` is the 3D iceberg scene.

## הדשבורד ב-`titanic.py`

בפורק נשאר גם דשבורד סינון נפרד. הוא צריך `streamlit`, `pandas` ו-`plotly`.

```bash
python -m streamlit run titanic.py
```
