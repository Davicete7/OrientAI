# OrientAI 🎓🤖

> **Transforming the uncertainty into a clear professional future.**

🚀 **Live App:** [https://orientai-deployment.streamlit.app/](https://orientai-deployment.streamlit.app/)

---

## 🧭 The Vision

Choosing a career at a young age is one of the most overwhelming decisions a person can make. Students face immense pressure from exams, often choosing their future based on outdated tests or peer pressure rather than true vocation.

**OrientAI** was born to change this. We use **Artificial Intelligence** to act as a digital mentor that truly "understands" the student, bridging the gap between high school and the professional world through data and empathy.

---

## ⚡ Quickstart

```bash
# 1. Clone the repository
git clone https://github.com/<org>/OrientAI.git
cd OrientAI

# 2. (Recommended) create a virtual environment
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up API keys
# Make sure to configure your API keys (e.g., in a .env file) to run the app correctly locally.

# 5. Run the app (from the project root)
python -m streamlit run src/main.py
```

The app opens automatically at **http://localhost:8501**

---

## 📁 Project Structure

```
OrientAI/
├── .gitignore
├── LICENSE
├── README.md               ← You are here
├── requirements.txt        ← Python dependencies
├── assets/
│   ├── icons/              Logo files
│   ├── presentations/      Mid-presentation slides
│   ├── reports/            Final report documents
│   └── surveys/            Survey templates
└── src/
    ├── __init__.py
    ├── main.py             ← Streamlit entry point
    ├── config.py           Constants & metadata
    ├── questions.py        Question banks (Q1 & Q2)
    ├── styles.py           Custom CSS injection
    ├── validation.py       Form validation logic
    ├── scoring.py          Derived features & labels
    ├── export.py           JSON build & file export
    ├── predict.py          Orange3 Model Prediction wrapper
    ├── models/
    │   ├── questionaire_1/ Orange3 models for Q1
    │   └── questionaire_2/ Orange3 models for Q2
    ├── components/
    │   ├── __init__.py
    │   ├── sidebar.py      Sidebar panel
    │   ├── hero.py         Hero banner
    │   ├── questionnaire.py  Form sections (gender, questions, satisfaction, submit)
    │   └── results.py      Post-submission results screen
    └── responses/          Auto-created; stores exported JSON files
```

---

## 🧠 How It Works

1. **The Dialogue:** The student completes a dynamic questionnaire powered by NLP (Natural Language Processing).
2. **The Analysis:** The AI engine processes the input, crossing it with academic requirements and professional trends.
3. **The Result:** A comprehensive "Future Report" with personalised academic recommendations.

## 🛠️ Tech Stack

* **LLM Integration:** Using state-of-the-art models to provide nuanced guidance.
* **Gen-Z Centric UI:** A fast experience designed for the students of today.
* **Ethical AI:** Recommendations are unbiased and purely focused on the student's best interest.

> *"The best way to predict the future is to create it."* — OrientAI is here to help students do exactly that.

---

**License:** Distributed under the Apache 2.0 License.
