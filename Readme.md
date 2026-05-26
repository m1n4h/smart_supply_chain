Smart Supply Chain Demand Forecasting System
This project is an intelligent, AI-powered system designed to predict product demand in a supply chain environment. By leveraging a Random Forest Machine Learning model, the system analyzes historical logistics data to provide real-time, data-driven forecasts that help managers optimize inventory levels, reduce waste, and improve operational efficiency.

🚀 System Overview & Functionality
The system acts as a Predictive Decision Support Tool. It uses historical data (weather, traffic, holidays) to "learn" patterns and then allows you to simulate future scenarios to predict demand.

Core Functionality:
Data Pipeline: Automates the ingestion of raw logistics CSV files and populates your PostgreSQL database.

Predictive Modeling: Uses a Random Forest regressor to analyze multiple variables (weather, traffic, holidays) and output a demand forecast.

Web Interface: A Django-based dashboard that provides real-time model inference based on URL parameters.

⚙️ Setup and Installation
Follow these steps to get the system running on your local machine.

Prerequisites
Python 3.x

PostgreSQL

pip

Installation Steps
Clone the Repository

Bash
git clone <your-repository-url>
cd smart_supply_chain
Setup Virtual Environment

Bash
python3 -m venv .venv
source .venv/bin/activate
Install Dependencies

Bash
pip install -r requirements.txt
Database Initialization
Ensure your PostgreSQL server is running and create a database named supply_chain_db.

Bash
python3 models.py
python3 manage.py makemigrations forecasting
python3 manage.py migrate
Train the Model & Run Server

Bash
# Run the automated pipeline to train the Random Forest model
python3 train_pipeline.py

# Start the application
python3 manage.py runserver
📊 How to Use & Test Scenarios
Once the server is running, you can query the system directly through your browser. The model takes external inputs to forecast expected demand.

Scenario A (Worst Case Logistics Chaos)
Test how demand drops during bad weather and heavy traffic:
http://127.0.0.1:8000/?weather=1&traffic=1&holiday=0

Scenario B (Peak Holiday Surge)
Check for stock risks during ideal conditions on a holiday:
http://127.0.0.1:8000/?weather=0&traffic=0&holiday=1

Stock Optimization Query
To check demand for bad weather on a non-holiday day:
http://127.0.0.1:8000/?weather=1&holiday=0

🧠 How the Model Makes Decisions
When you change the URL parameters, you are triggering an Inference Cycle:

Request Extraction: The Django views.py captures the weather, traffic, and holiday values from your URL request.

Data Structuring: The inputs are converted into a numerical array structure: [[weather, traffic, holiday]].

Inference: The script invokes model.predict([[1, 0, 1]]) using the binary demand_rf_model.pkl file generated during the training pipeline.

Ensemble Logic: The Random Forest algorithm aggregates decisions from dozens of "mini-decision trees" built during the training phase to output the most accurate demand forecast.

📁 Project Structure
/forecasting: Django app containing logic for data models and views.

/models.py: Database initialization script.

train_pipeline.py: Script to preprocess data and train the Random Forest model.

demand_rf_model.pkl: The serialized machine learning model (generated after running the pipeline).

🤝 Contribution
Contributions are welcome! Please fork the repository and submit a pull request for any new features or bug fixes.

📄 License
This project is licensed under the MIT License.