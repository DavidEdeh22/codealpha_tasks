# 🌍 WHO Disease Outbreak News Web Scraper (2020–2025)

> **A professional web scraping project developed as part of the CodeAlpha Data Analytics Internship.**

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![Selenium](https://img.shields.io/badge/Selenium-Web%20Automation-green?logo=selenium)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-HTML%20Parsing-orange)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-purple?logo=pandas)

---

## 📖 Project Overview

The **World Health Organization (WHO) Disease Outbreak News (DON)** website publishes official reports on disease outbreaks and public health emergencies across the world. While these reports contain valuable information for researchers, healthcare professionals, epidemiologists, and data analysts, they are presented as individual web pages rather than as a structured dataset suitable for analysis.

This project demonstrates how to build a **professional Python web scraper** that automatically extracts outbreak reports from the WHO Disease Outbreak News website between **2020 and 2025**.

Because the website loads its content dynamically using JavaScript, **Selenium** is used to render the webpage before **BeautifulSoup** extracts the required information from the rendered HTML.

The final output is a structured dataset that can be used for **Exploratory Data Analysis (EDA)**, **data visualization**, and future **healthcare analytics projects**.

---

## 🎯 Project Objectives

This project was developed to:

* Learn professional web scraping techniques using Python.
* Understand how to inspect and navigate HTML structures.
* Scrape dynamically rendered websites using Selenium.
* Parse HTML efficiently using BeautifulSoup.
* Automate pagination across multiple pages.
* Build a reusable and structured dataset.
* Apply good software engineering practices such as modular programming, logging, exception handling, and progress tracking.
* Produce a clean dataset for downstream data analysis.

---

## 💼 Business Problem

Public health organizations continuously publish disease outbreak reports to keep governments, researchers, healthcare professionals, and the public informed about emerging health threats.

However, these reports are typically presented as individual web pages rather than as structured datasets that can easily be analysed.

As a result, answering questions such as:

* Which diseases were reported most frequently?
* Which countries experienced the highest number of outbreak reports?
* How did outbreak reporting change over time?
* Which months recorded the highest number of reported outbreaks?

requires manually collecting data from numerous pages.

This project automates that process by converting publicly available WHO outbreak reports into a structured dataset suitable for healthcare analytics.

---

## 🌍 Why This Project Matters

Structured outbreak data can support:

* Public health surveillance
* Epidemiological research
* Healthcare data analytics
* Disease trend analysis
* Academic research
* Dashboard development
* Healthcare decision support

As both a **pharmacist** and an **aspiring healthcare data analyst**, this project demonstrates the application of data analytics techniques to real-world healthcare information.

---

## 🛠 Technologies Used

| Technology        | Purpose                                   |
| ----------------- | ----------------------------------------- |
| Python            | Core programming language                 |
| Selenium          | Render JavaScript-driven webpages         |
| BeautifulSoup     | Parse rendered HTML                       |
| Pandas            | Data cleaning and manipulation            |
| tqdm              | Progress tracking                         |
| webdriver-manager | Automatic ChromeDriver management         |
| Logging           | Execution monitoring and debugging        |
| VS Code           | Development environment                   |
| Git & GitHub      | Version control and project documentation |

---

## 🔄 Project Workflow

```text
Start
   │
   ▼
Launch Chrome Browser
   │
   ▼
Open WHO Disease Outbreak News Website
   │
   ▼
Render Dynamic Content using Selenium
   │
   ▼
Capture Rendered HTML
   │
   ▼
Parse HTML with BeautifulSoup
   │
   ▼
Extract Report Information
   │
   ▼
Validate Extracted Records
   │
   ▼
Navigate Through All Pages
   │
   ▼
Stop Automatically at Year 2020
   │
   ▼
Create Pandas DataFrame
   │
   ▼
Remove Duplicate Records
   │
   ▼
Export Dataset to CSV
   │
   ▼
Project Complete
```

---

## 📂 Repository Structure

```
CodeAlpha_WHO_Disease_Outbreak_WebScraping/
│
├── data/
│   └── who_outbreak_reports.csv 
│
├── logs/
│   └── scraping.log
│
├── notebooks/
│   └── who_scraping.ipynb
│
├── scripts/
│   └── scraper.py
│
├── screenshots/
│   ├── homepage.png
│   ├── scraper_running.png
│   ├── scraper_completed_preview.png
│   └── csv_preview.png
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

## ⚙ Installation

Clone the repository:

```bash
git clone https://github.com/DavidEdeh22/CodeAlpha_WHO_Disease_Outbreak_WebScraping.git
```

Navigate into the project directory:

```bash
cd CodeAlpha_WHO_Disease_Outbreak_WebScraping
```

Install all required packages:

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Project

Run the scraper using:

```bash
python scripts/scraper.py
```

During execution, the scraper will:

* Launch Chrome automatically.
* Open the WHO Disease Outbreak News website.
* Render JavaScript content.
* Extract outbreak reports.
* Automatically navigate through all relevant pages.
* Display progress while scraping.
* Save logs to the `logs` folder.
* Export the final dataset as:

```
data/who_outbreak_reports.csv
```

Once the script completes successfully, the dataset will be ready for exploratory data analysis and visualization.

---

# 📊 Dataset Description

The scraper extracts one record for each Disease Outbreak News report published by the World Health Organization (WHO).

The final dataset contains the following fields:

| Column               | Description                                                        |
| -------------------- | ------------------------------------------------------------------ |
| **report_title**     | Title of the outbreak report published by WHO                      |
| **publication_date** | Official publication date of the report                            |
| **report_url**       | Direct URL to the original WHO report                              |
| **disease**          | Disease name derived from the report title                         |
| **country**          | Country or region derived from the report title (where applicable) |
| **year**             | Publication year extracted from the publication date               |
| **month**            | Publication month extracted from the publication date              |

These derived fields make the dataset more suitable for exploratory data analysis and visualization.

---

# 🔍 HTML Inspection and Website Analysis

Before developing the scraper, the website's HTML structure was carefully inspected using the browser's Developer Tools.

An initial inspection of the page source revealed that the outbreak reports were **not present in the raw HTML**.

This indicated that the website loads its content dynamically using JavaScript after the initial page request.

To address this challenge:

* Selenium was used to render the webpage.
* The rendered HTML was captured using `driver.page_source`.
* BeautifulSoup then parsed the fully rendered HTML.
* Relevant report elements were identified using CSS selectors.

This approach ensured reliable extraction of outbreak reports from the rendered webpage.

---

# ⚙ Scraping Methodology

The scraping workflow consists of the following stages:

### 1. Browser Automation

Chrome is launched using Selenium WebDriver.

---

### 2. Page Rendering

The WHO Disease Outbreak News webpage is fully rendered before extraction begins.

---

### 3. HTML Parsing

BeautifulSoup parses the rendered HTML into an object that can be searched efficiently.

---

### 4. Data Extraction

For every outbreak report, the scraper extracts:

* Report Title
* Publication Date
* Report URL

Additional fields such as **Year**, **Month**, **Disease**, and **Country** are then derived.

---

### 5. Pagination

The scraper automatically navigates through every available page containing outbreak reports.

Scraping continues until reports older than **2020** are encountered.

This prevents unnecessary requests while ensuring the project remains within its defined scope.

---

### 6. Data Validation

Each extracted record is validated before being stored.

Checks include:

* Missing titles
* Missing dates
* Missing URLs

Invalid records are skipped.

---

### 7. Logging

Execution details are recorded throughout the scraping process.

Examples include:

* Browser initialization
* Number of reports extracted
* Pagination progress
* Export completion
* Errors and warnings

This makes debugging significantly easier.

---

### 8. CSV Export

After successful extraction and cleaning, the final dataset is exported as:

```text
data/raw/who_outbreak_reports.csv
```

The dataset is then ready for downstream analysis.

---

# 🧹 Data Cleaning

After extraction, several preprocessing steps are performed before exporting the dataset.

These include:

* Removing duplicate reports
* Filtering reports between **2020 and 2025**
* Creating Year and Month columns
* Standardizing extracted text
* Resetting the DataFrame index

These steps improve dataset quality and analytical usability.

---

# 📈 Project Output

The final output of this project is a structured CSV dataset containing WHO Disease Outbreak News reports published between **2020 and 2025**.

This dataset can be used for:

* Exploratory Data Analysis (EDA)
* Healthcare dashboards
* Disease trend analysis
* Public health research
* Power BI visualizations
* SQL projects
* Machine learning experiments

---

# ⚠ Challenges Encountered

Several technical challenges were encountered during the project.

## Dynamic Website Rendering

The WHO website loads outbreak reports using JavaScript.

As a result, the report data was unavailable in the initial page source.

This challenge was addressed by rendering the webpage using Selenium before parsing the HTML.

---

## Pagination

The outbreak reports span multiple pages.

Automatic pagination was implemented to navigate through each page until the defined year range was reached.

---

## Data Consistency

Not every report follows exactly the same title format.

To keep the project simple and maintainable, the **Disease** and **Country** fields were derived directly from the report titles where possible.

These fields may require minor manual refinement for certain reports.

---

# 🛡 Ethical Considerations

This project was developed solely for educational and analytical purposes.

To promote responsible web scraping practices:

* Only publicly available information was collected.
* No authentication or restricted resources were accessed.
* Polite request delays were introduced between page navigations.
* The scraper was designed to minimize unnecessary requests to the WHO website.

---

# 📷 Project Preview

Example screenshots included in this repository:

* WHO Disease Outbreak News homepage
* Selenium browser during execution
* Progress tracking in the terminal
* Preview of the exported CSV dataset

These screenshots provide a visual overview of the scraping workflow.

---

# 🚀 Future Improvements

Possible enhancements include:

* Exporting data to SQL databases
* JSON export support
* Automatic scheduled scraping
* Cloud deployment
* Docker containerization
* Interactive Power BI dashboard
* NLP analysis of outbreak report content
* Automated email notifications for newly published reports
* Integration into an end-to-end healthcare analytics pipeline

---

# 📚 Key Learnings

This project provided valuable experience in:

* Python programming
* Web scraping best practices
* Selenium browser automation
* HTML inspection
* BeautifulSoup parsing
* Dynamic website handling
* Exception handling
* Logging
* Data validation
* Modular programming
* Healthcare data collection
* Preparing datasets for analytics

---

# 🙏 Acknowledgements

Special appreciation to:

* **CodeAlpha** for providing this internship project.
* The **World Health Organization (WHO)** for making Disease Outbreak News publicly accessible.
* The open-source Python community for developing the libraries used in this project.

---

# 👨‍💻 Author

**David Edeh**

Pharmacist | Data Analyst | Healthcare Analytics Enthusiast

I am passionate about applying data analytics to solve real-world healthcare problems. My interests include healthcare analytics, public health, SQL, Python, Power BI, and data visualization.

📧 Email: edehdavid22@gmail.com

💼 LinkedIn: https://www.linkedin.com/in/david-edeh-84aa65232

🌐 Portfolio: https://davidedeh22.github.io/

🐙 GitHub: https://github.com/DavidEdeh22

---

## ⭐ If you found this project helpful, consider giving it a star!

Thank you for visiting this repository.
