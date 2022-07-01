# DSP-Dora-the-data-explorer

#DSP Cars Price Model diagram

![image](https://user-images.githubusercontent.com/74925493/176908419-887e60d2-51f5-48a8-8ada-68a7caae2f0d.png)

Working of our model:

We have created a Machine Learning model which can make predictions of Car prices based on it's features. Our UI webpage built on streamlit can take inputs from the user to make a real time on-demand prediction of a used car price. It is also possible to make inference batch predictions by uploading a file. The entered informations are sent to FastAPI which then calls the ML model to make a prediction. 
We can also use Airflow to ingest data from a source to another and make scheduled predictions on the database. The predictions are saved in the database and their history can be checked. Grafana is then connected to the Database and can monitor the distribution of our data and the predictions made. We have also set up the Alerts system in Grafana which can Fire alerts based on the incoming data features, and send us real time automated notifications on Teams.
