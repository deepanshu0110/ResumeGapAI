# ResumeGapAI

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/streamlit-app-ff4b4b)
![License](https://img.shields.io/badge/license-MIT-green)
![Demo](https://img.shields.io/badge/demo-live-brightgreen)

Instantly find skills missing from your resume compared to a job description.

## 🔍 Live Demo

Visit: **https://resumegapai.streamlit.app**

No installation required — just paste your resume and a job description to get instant feedback.

## 📸 Screenshot

![ResumeGapAI screenshot](screenshot.png)

## ⚡ Quick Start

```bash
# Clone the repository
git clone https://github.com/deepanshu0110/ResumeGapAI.git
cd ResumeGapAI

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## 🧠 How It Works

ResumeGapAI uses TF-IDF vectorization with a background corpus to correctly weight rare, meaningful terms. It compares your resume against a job description and returns:

- **Corpus-Corrected Similarity** — the score to trust
- **Naive TF-IDF** — shown for transparency, fitted only on the two texts
- **Gap words** — skills present in the job description but missing from your resume

This helps you tailor your resume and prepare for interviews by highlighting exactly which skills to add or discuss.

## 🛠️ Tech Stack

- Python 3.10+
- **Streamlit** — UI framework
- **scikit-learn** — TF-IDF and cosine similarity

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/deepanshu0110/ResumeGapAI/issues).

## 🙏 Acknowledgements

Built as part of a 12-month structured Data Science & AI program — a curriculum for building production-ready AI tools.

Made with ❤️ by [Deepanshu](https://github.com/deepanshu0110)
