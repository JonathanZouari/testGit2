# Titanic survival

<p>
  <img alt="Python 3" src="https://img.shields.io/badge/Python-3-0B1220?style=flat-square">
  <img alt="Streamlit" src="https://img.shields.io/badge/Streamlit-dashboard-FF4B4B?style=flat-square">
  <img alt="Plotly" src="https://img.shields.io/badge/Plotly-charts-3D4F7C?style=flat-square">
</p>

דשבורד אינטראקטיבי לנתוני הנוסעים של הטיטאניק. כל שורה ב-`data/titanic.csv` היא נוסע, עם מין, גיל, מחלקה, נמל עלייה, מחיר כרטיס ותוצאת ההישרדות. הקובץ הוא מאגר [Kaggle Titanic](https://www.kaggle.com/c/titanic) הציבורי של Data Science Dojo, 891 רשומות.

## התקנה

```bash
python -m pip install streamlit pandas plotly
```

## הרצה

מתוך תיקיית הפרויקט:

```bash
python -m streamlit run titanic.py
```

הדשבורד נפתח בדפדפן, בדרך כלל בכתובת `http://localhost:8501`.

## מה יש במסך

- **סרגל סינון:** מין, מחלקה (1st / 2nd / 3rd), נמל עלייה (Cherbourg, Queenstown, Southampton), טווח גיל וטווח מחיר. אפשר לכלול גם נוסעים בלי גיל ידוע.
- **מדדים:** מספר נוסעים, שיעור הישרדות, גיל ממוצע וחציון מחיר הכרטיס. כולם מתעדכנים לפי הסינון.
- **גרפים:** הישרדות לפי מין, שיעור הישרדות לפי מחלקה, התפלגות גילאים, מחיר לפי מחלקה, ונוסעים לפי נמל. אפשר להתקרב, להזיז ולהוריד כל גרף כתמונה.
- **טבלה:** שם, מין, גיל, מחלקה, נמל, מחיר, גודל משפחה ותוצאה. אפשר לחפש, לבחור עמודות ולהוריד CSV.

על כל 891 הרשומות שיעור ההישרדות הוא 38.4%. בקרב הנשים הוא 74.2%.

## מבנה התיקייה

```text
testGit22/
├── titanic.py          # אפליקציית Streamlit
├── data/
│   └── titanic.csv     # 891 נוסעים
└── README.md
```
