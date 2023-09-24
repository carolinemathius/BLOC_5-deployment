# BLOC_5-deployment

**BLOC 5 - Jedha Certification - Getaround project**
This repository contains two applications: an API and a Streamlit dashboard for a car rental service similar to GetAround. The API provides pricing predictions for car owners, while the Streamlit dashboard offers data insights and visualizations related to rental delays and owner's revenue.

## Links for certification
[API App for Predictions](https://getaround-api-d08e0b37d9ea.herokuapp.com/docs#/Predictions/predict_predictions_post) : click on this link to access the API app.  
[Delay Analysis Dashboard](https://getaround-dashboard-d00ca7766cd3.herokuapp.com/) : click on this link to access the dashboard app.  
[Video presentation of the project](https://share.vidyard.com/watch/rWhYH39d5h3zEuDHRevBHQ?) : here is the video presentation of this project.

## Table of Contents

- [Overview](#overview)
- [Repository Structure](#repository-structure)
- [Getaround Rental Pricing Optimization API](#getaround-rental-pricing-optimization-api)
- [Streamlit Dashboard](#streamlit-dashboard)
- [Getting Started](#getting-started)
- [Contributing](#contributing)

## Overview

This project represents a comprehensive solution for optimizing rental pricing and analyzing rental delays in the car-sharing industry. It encompasses two main components:

**API**: An API that provides rental price predictions based on various car features and rental-related parameters. The API is designed to help car owners determine the most suitable rental price for their vehicles, enhancing their revenue.

**Streamlit Dashboard**: An interactive web-based dashboard that offers data insights and visualizations related to rental delays and their impact on owner revenue. Users can explore delay analysis, set custom thresholds, and gain a deeper understanding of how rental delays affect their business.

Both the API and Streamlit dashboard are *deployed online*, allowing easy access for users to leverage the functionalities and insights provided by this project.

## Repository Structure

```
BLOC_5-deployment/
│
├── README.md
│
├── API/
│ ├── Dockerfile
│ ├── Procfile
│ ├── api-app.py
│ ├── best_model.pkl
│ ├── heroky.yml
│ ├── preprocessor.pkl
│ ├── requirements.txt
│ └── runtime.txt
│
└── Dashboard/
├── Dockerfile
├── Procfile
├── heroku.yml
├── requirements.txt
├── runtime.txt
└── streamlit-app.py
```

## Getaround Rental Pricing Optimization API
The api-app.py script deploys a FastAPI-based API for predicting optimum rental prices for car owners on the Getaround platform. The API uses a pre-trained machine learning model to make predictions based on various features provided by car owners.

### Features
- **Prediction Endpoint**: Allows users to post data about their cars, including model, mileage, engine power, fuel type, and more, and receive a suggested optimum rental price in response.
- **Input Validation**: Ensures that input data adheres to specific constraints and formats, such as valid car models and numerical ranges.
- **Data Preprocessing**: Utilizes a pre-trained preprocessor to transform input data and make it compatible with the model.

### Usage
**Start the API**: Run the script using Uvicorn to start the API server.  
**Access the API Documentation**: Visit the API documentation by navigating to the root URL. The documentation provides details on available endpoints and how to use them.  
**Make Predictions**: Use the /predictions endpoint to post data about a car for rental price predictions. The API will respond with the suggested rental price.

[Link to the API App for Predictions](https://getaround-api-d08e0b37d9ea.herokuapp.com/docs#/Predictions/predict_predictions_post)

### Dependencies
- **FastAPI**: A modern web framework for building APIs with Python.
- **Joblib**: Used for loading the pre-trained machine learning model.
- **Pydantic**: For defining and validating input data using Python data classes.
- **Scikit-learn**: Provides tools for data preprocessing and machine learning.
- **Uvicorn**: A lightweight ASGI server to host the FastAPI application.


## Streamlit Dashboard

### Dashboard Features

- Data insights and visualizations related to rental delays and owner's revenue.
- Customizable parameters for threshold and scope.
- Interactive charts and tables.

### Dashboard Usage

To access and use the Streamlit dashboard, follow these steps:

1. Open a web browser.

2. Navigate to the deployed Streamlit dashboard URL : [Delay Analysis Dashboard](https://getaround-dashboard-d00ca7766cd3.herokuapp.com/)

3. Upon accessing the dashboard, you will see the following sections:

   - **Data Exploration**: This section provides an overview of the dataset, including a data sample and a visualization of check-in types.

   - **Delay Analysis**: Explore insights related to rental delays and their impact on the next driver.

   - **Threshold**: Understand how different threshold values affect the occurrence of problematic delays for various check-in types.

   - **Conclusion**: Summarizes the results and provides recommendations for threshold settings.

4. Customize Parameters:
   - In the "Threshold" section, you can customize delay threshold values for mobile and connect check-ins to see their impact on problematic delays. The dashboard will update accordingly.

5. Interactive Charts and Tables:
   - The Streamlit dashboard features interactive charts and tables that allow you to explore and analyze data insights dynamically.

6. Sidebar Navigation:
   - The sidebar provides quick navigation links to different sections of the dashboard, allowing you to jump directly to the desired content.


## Getting Started

To run the Getaround Rental Pricing Optimization API and Streamlit Dashboard locally, follow these steps:

#### Prerequisites

- Python 3.7 or higher installed on your system.

#### Installation

1. Clone this GitHub repository to your local machine:

   ```bash
   git clone https://github.com/your-username/BLOC_5-deployment.git
   ```

2. Navigate to the project directory:

   ```bash
   cd BLOC_5-deployment
   ```

3. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment:

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On macOS and Linux:

     ```bash
     source venv/bin/activate
     ```

5. Install the project dependencies:

   ```bash
   pip install -r API/requirements.txt
   pip install -r Dashboard/requirements.txt
   ```

#### Running the API Locally

1. Navigate to the API directory:

   ```bash
   cd API
   ```

2. Start the FastAPI server locally:

   ```bash
   uvicorn api-app:app --reload
   ```

   The API will be available at `http://localhost:8000`.

#### Running the Streamlit Dashboard Locally

1. Open a new terminal window and navigate to the Dashboard directory:

   ```bash
   cd ../Dashboard
   ```

2. Start the Streamlit app locally:

   ```bash
   streamlit run streamlit-app.py
   ```

   The Streamlit dashboard will be available in your web browser at `http://localhost:8501`.

Now you can interact with both the API and the Streamlit dashboard on your local machine.

**Note**: Make sure to replace `your-username` in the GitHub clone URL with your actual GitHub username.


## Contributing

This project is intended for personal or educational purposes, and contributions from external contributors are not actively sought or encouraged. It is primarily developed as part of a certification assignment and may not be actively maintained beyond its intended scope.  

Feel free to explore and use the project for your own learning and reference; however, external contributions, such as pull requests or issue submissions, are not expected or accepted at this time.  

Thank you for your understanding.

