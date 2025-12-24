# 🎅 XmasGiftRecommender

**XmasGiftRecommender** is a smart gift recommendation engine powered by Natural Language Processing (NLP). Unlike traditional keyword search, this application understands the *meaning* behind your description to find the perfect gift from thousands of Amazon products.
Built with **Streamlit** and **Sentence Transformers**.

---

## ⚙️ Prerequisites

- **Python Version:** Ensure you have Python 3.11 or newer installed on your system. To check your Python version, open your terminal or command prompt and run:

  ```bash
  python --version
  ```
  OR

  ```bash
  python3 --version
  ```
- If the command returns a version number starting with 3.11 or higher (e.g., Python 3.11.2), you’re good to go. If not, you’ll need to install or update Python.

- Install Python 3.11 (if needed):

  - **Windows:** You can use the Windows Package Manager (winget) to install it:

    ```bash
    winget install -e --id Python.Python.3.11
    ```

    You can also use Chocolatey, if you have it installed on your system:

    ```bash
    choco install python311 -y
    ```
    
  - **macOS:** You can use Homebrew to install it:
 
    ```bash
    brew install python@3.11
    ```
 
  - **Linux:** On Linux, you can install Python 3.11 using your distribution's package manager. For example, on Ubuntu:

    ```bash
    sudo apt update && sudo apt install python3.11 -y
    ```

---

## ✨ Features

* **🧠 Semantic Search:** Uses a pre-trained Transformer model (`paraphrase-multilingual-MiniLM-L12-v2`) to match user descriptions with product nuances.
* **💰 Smart Budgeting:** Filter products dynamically based on a selected price range (from 1€ to 500€).
* **🎯 Relevance Scoring:** Displays a compatibility score (e.g., "95% Match") to show how well a product fits the description.
* **🛡️ Quality Filter:** Automatically hides irrelevant results (low similarity score) to ensure high-quality recommendations.
* **❄️ Interactive UI:** Festive interface with snow effects and responsive design.

## 🛠️ Tech Stack

* **Python 3.11**
* **Streamlit** (Frontend & UI)
* **Pandas** (Data Manipulation)
* **Sentence-Transformers** (Embeddings & Semantic Search)

---

## 🚀 Installation & Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/lucadani7/XmasGiftRecommender.git
   cd XmasGiftRecommender
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Ensure that the `amazon.csv` dataset is placed in the root directory of the project. (Note: The dataset requires columns: product_name, about_product, discounted_price, img_link).

4. Run the app:
   ```bash
   streamlit run main.py
   ```

---

## 🧠 How it Works
1. Preprocessing: The app loads the Amazon dataset and converts prices from INR to EUR (we consider 1 EUR = 105 INR).
2. Vectorization: It generates vector embeddings for the product descriptions using the Sentence Transformer model.
3. Cosine Similarity: When a user queries (e.g., "gift for a gamer"), the app calculates the mathematical distance between the query and all products.
4. Ranking: Products are filtered by budget and sorted by their similarity score.

---

## 📄 License

This project is licensed under the Apache-2.0 License.
