# Application of Sentiment Analysis in E-Commerce Recommendation Systems

Try out the web app [here](https://share.streamlit.io/weiaun96/ecommerce-recommendation-web-app/main/web_app.py)!

## Introduction

This project was done as my capstone project during my masters degree with Asia Pacific University. With the title of 'Application of Sentiment Analysis in E-Commerce Recommendation Systems', this project presents an application of sentiment analysis into the recommendation mechanism in the e-commerce domain.

## Problem Statement

Spam and irrelevant reviews online can mislead and force buyers to make purchases they would not have made otherwise. By including the sentiment scoring of product reviews as quantification of explicit feedback, it can combine with other implicit feedback like clicks or views in the recommendation engine to help recommend better products to the customers.

## Dataset

The dataset used for this project is an Amazon outdoors product reviews dataset made available public by Amazon on their AWS repository. You may access the repository [here](https://s3.amazonaws.com/amazon-reviews-pds/readme.html). The dataset have a total of almost 2.3 million observations with 15 variables.

## Exploratory Data Analysis
### Sales Seasonality
![image](https://github.com/weiaun96/ecommerce-recommendation-web-app/blob/main/Images/Distribution%20of%20Reviews%20through%20the%20months.png)
- Sales seasonality follows the weather season; summer is arriving in July and August. So people are buying their outdoors product to prepare for their recreational summer activities.
- Dec and Jan shows higher-than-average sales; year end are shopping peak seasons with Christmas/Black Friday etc.

### Amazon Vine
![image](https://github.com/weiaun96/ecommerce-recommendation-web-app/blob/main/Images/Distribution%20of%20Vine%20Voices.png)
- 99.9% of the reviews are not having Vine status. Amazon Vine is a program that invites reviewers to post their reviews on the Amazon platform. In return, the Vine members, also known as Vine Voices, get free products from participating vendors. Since this is an invitation-only program, only the most trusted reviews on Amazon are invited, which explains the skewness of the distribution in the dataset.

### Verified Purchases
![image](https://github.com/weiaun96/ecommerce-recommendation-web-app/blob/main/Images/Distribution%20of%20Verified%20Purchases.png)
- 88.0% of the reviews have been verified as actual purchases.
- It is important that the product review data observations are actual purchases and do not belong as a fake review.

![image](https://github.com/weiaun96/ecommerce-recommendation-web-app/blob/main/Images/drop%20verified%20purchases.png)
- To reduce the possibility of having fake reviews, only verified purchases are included for the further development in the study.

### Distribution of Star Ratings
![image](https://github.com/weiaun96/ecommerce-recommendation-web-app/blob/main/Images/Distribution%20of%20Ratings%20(Pie).png)
- 62.3% of the reviews are having a rating of 5 while another 18.1% have a rating of 4.
- These 2 ratings combined to make up 80.4% of the dataset. This shows the overall satisfaction towards the products by the customers. These rating scores will play an important role in further implementation of the study because these rating scores will be integrated with sentiment scoring to form recommendation scores, which will be used to generate recommendations for the new users.

## Missing Value Treatment and Dropping Variables
- Obervations with missing datapoints are dropped from the dataset. Less relevant variables like marketplace and product category etc are also dropped from the dataset to allow lesser memory consumption and faster runtime.

## Sentiment Scoring
- The Valence Aware Dictionary for Sentiment Reasoning (VADER) library from the NLTK family is used in this sentiment scoring, where it can analyze sentiment through scoring in 4 different classes which are positive, negative, neutral and compound. 
- In this case, the compound scoring method is used and it have a scoring scale of -1 to 1, where -1 indicates the most negative sentiment, and +1 is the most positive with 0 as neutral sentiment


## Recommendation Scoring & Search Engine
### Rescaling the VADER score
![Rescaling VADER Score](https://github.com/weiaun96/ecommerce-recommendation-web-app/blob/main/Images/Rescaling%20VADER%20score.jpg)
- Since the compound score from VADER scales from -1 to 1, rescaling is needed to generate a 50% weightage in recommendation score. This is done by using the rescaling formula so that when we have the sentiment score in the 0 to 5 scale and also the rating score having a maximum score of 5, they will both add up to have a maximum recommendation score of 10.

### Collaborative Filtering Recommendation
- The customer ids and the product ids are mapped into a map matrix. Then, K-nearest neighbor model is used to calculate the feature similarity distance between a target item with others in the matrix, which in this case, returning K-nearest products as the most similar product recommendations.

### Search Engine
- The recommendation model is supplemented with a search engine-like tool to allow customers to search for their relevant products. This search engine finds relevant products by matching the search terms with the product titles, where it can only generate search results when there is a match.

### Web App
Finally, the search tool is deployed into a web app using Streamlit to allow easy access to users. You may try it out with the web app [here](https://share.streamlit.io/weiaun96/ecommerce-recommendation-web-app/main/web_app.py)!
