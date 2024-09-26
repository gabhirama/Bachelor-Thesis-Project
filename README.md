# Bachelor Thesis Project AG47005
## Evapotranspiration-Prediction-using-Machine-Learning
### Author: Abhirama Gorti, Indian Institute of Technology Kharagpur
_Supervisor: Dr. D. R. Mailapalli_

_Date: November 28, 2023_

## Project Overview
This project focuses on predicting crop evapotranspiration (ET) using advanced machine learning (ML) and deep learning (DL) algorithms. Accurate evapotranspiration estimation is crucial for efficient irrigation management, helping farmers apply the right amount of water for optimal crop growth.

Traditional empirical models like **FAO-56 Penman-Monteith** have been widely used for estimating reference evapotranspiration (ETo). However, recent advancements in ML offer an opportunity to develop more accurate predictive models that consider a broader set of features and geographic diversity. This project compares traditional methods with modern ML/DL techniques such as **Random Forest (RF), Support Vector Machines (SVMs), Feedforward Neural Networks (FFNs), Convolutional Neural Networks (CNNs), and Long Short-Term Memory (LSTM) networks**.

## Key Features
1. Data Collection and Preprocessing:

Collected meteorological data from 25 stations across India.
Features include temperature, humidity, wind speed, solar radiation, and sunshine hours.
Data was also validated using UC Davis Lysimeter data for performance comparison.

2. ML and DL Models Used:

Random Forest (RF)
Support Vector Machines (SVM)
Feedforward Neural Networks (FFN)
Convolutional Neural Networks (CNN)
Bidirectional Long Short-Term Memory (LSTM)

3. Model Evaluation Metrics:

Mean Squared Error (MSE)
R-squared (R²)
Performance was evaluated using both Indian meteorological data and UC Davis data to assess the generalizability of the models.

4. Ensemble Model:

An ensemble model was developed to improve accuracy in combining predictions from individual models.
Different ensembling strategies, such as averaging and weighted averaging, were tested.

## Results
**Model Performance:**
The ML and DL models demonstrated robust performance, with R² values reaching above 75% compared to the FAO-56 Penman-Monteith method.
The ensemble model improved the accuracy further by combining the strengths of individual models.

**Challenges:**
Geographic limitations in data sources impacted the accuracy of predictions when applied to new regions like UC Davis.
There is a need for better ensembling techniques to handle model biases and prediction diversity.
