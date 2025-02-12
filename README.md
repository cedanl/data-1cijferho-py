<p align="center"><img src="src/assets/npuls_logo.png" alt="CEDA"></p>
<h1 align="center">Npuls-CEDA | data-1cijferho-py</h1>

<div align="center"> <strong>🚀 1 Cijfer HO Data Transformation Tool 🛠️</strong>
    <br> Python project for processing raw 1 Cijfer HO data from Dutch higher education institutions. 
    <br>
    <sub>Ideal for data analysts, researchers, and education professionals working with DUO datasets</sub> </div> 

<br>

<div align="center">
  <h3>
    <a href="https://community-data-ai.npuls.nl/groups/view/44d20066-53a8-48c2-b4e9-be348e05d273/project-center-for-educational-data-analytics-ceda">
      Website
    </a>
    <span> | </span>
    <a href="https://github.com/cedanl/data-1chijfer-py#features">
      Features
    </a>
    <span> | </span>
    <a href="https://github.com/cedanl/data-1chijfer-py#download-and-installation">
      Downloads
    </a>
    <span> | </span>
    <a href="https://github.com/cedanl/data-1chijfer-py#development">
      Development
    </a>
    <span> | </span>
    <a href="https://github.com/cedanl/data-1chijfer-py#contribution">
      Contribution
    </a>
  </h3>
</div>

<div align="center">
  <sub>The ultimate 1 Cijfer HO data processing tool. Built with ❤︎ by
    <a href="https://github.com/cedanl">CEDA</a> and
    <a href="https://github.com/cedanl/data-1chijfer-py/graphs/contributors">
      contributors
    </a>
    .
  </sub>
</div>

<br />

# 🔍 Purpose
This project is designed to transform raw 1 Cijfer HO (Een Cijfer Hoger Onderwijs) data from DUO (Dienst Uitvoering Onderwijs) for higher education institutions in the Netherlands. It processes ASCII files and decode files to produce structured, analyzable data.

## Key Features

- 🚀 Efficient processing of 1 Cijfer HO ASCII files
- 🔒 Secure handling of sensitive educational data
- 🧪 Data validation and quality checks
- 📦 Streamlined data transformation pipeline
- 🐳 Docker containerization for consistent environments
- 🚢 Easy deployment and scalability
- 🔍 Comprehensive logging for data processing steps

## Demo

Check out the demo of the app in action:



This GIF demonstrates the data transformation process and user interface of the Streamlit application.

## Ideal For

- Educational Researchers
- Data Analysts in Higher Education
- Policy Makers in Dutch Education Sector
- IT Departments of Dutch Universities

# 📁 Project Structure

```
├───data
│   ├───input
│   └───output
├───src
│   ├───assets
│   ├───config
│   ├───backend
│   └───frontend
│       ├───Files
│       ├───Home
│       └───Modules

```


## Directory Descriptions

### 📂 data

- input: Store raw 1 Cijfer HO ASCII files and decode files from DUO.
- output: Save processed and transformed data ready for analysis.

### 📂 src

- assets: Contains static files like images and documentation.
- config: Configuration files for data processing and application settings.
- backend: Core logic for ASCII file parsing and data transformation.
- frontend: Streamlit interface for data upload, processing, and visualization.
  - Files: Components for handling 1 Cijfer HO file uploads.
  - Home: Main dashboard for data processing status and results.
  - Modules: Reusable components for data visualization and reporting.

# 🌟 How to Use This Project

## For CEDA Members

1. Clone the repository
2. Install dependencies using `uv`
3. Configure environment variables for data paths
4. Run the Streamlit app to start processing 1 Cijfer HO data

## For External Contributors

1. Fork the repository
2. Set up a local development environment
3. Contribute improvements to data processing algorithms or UI

## Quick Start

```
git clone https://github.com/cedanl/data-1chijfer-py.git
cd data-1chijfer-py
tv run streamlit run src/main.py

```

# 🛠 Project Features

- Automated parsing of 1 Cijfer HO ASCII files
- Decoding of data using provided decode files
- Data validation and error reporting
- Streamlit interface for easy data upload and processing
- Visualization of processed data and statistics

# 📋 Development Checklist

- [ ] Implement ASCII file parser
- [ ] Develop decode file interpreter
- [ ] Create data validation modules
- [x] Build Streamlit interface for file upload and processing
- [ ] Implement data visualization components
- [ ] Set up automated testing for data processing accuracy
- [ ] Add screenrecording of the app to the README

# 🤝 Contributing
Please read CONTRIBUTING.md for details on our code of conduct and process for submitting pull requests.

Thank you to all the people who have already contributed to data-1chijfer-py[[contributors](https://github.com/cedanl/data-1chijfer-py/graphs/contributors)].

[![](https://github.com/asewnandan.png?size=50)](https://github.com/asewnandan)
[![](https://github.com/tin900.png?size=50)](https://github.com/tin900)
