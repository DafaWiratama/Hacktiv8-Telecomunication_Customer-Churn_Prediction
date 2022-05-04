import pandas as pd
from streamlit_echarts import st_echarts
import streamlit as st
import requests

st.set_page_config(layout="wide", page_title="Telco - Churn Prediction")

ENDPOINT = "https://telco-customer-churn-h8-api.herokuapp.com/v1"


# ENDPOINT = "http://10.10.10.13:5000/v1"


@st.cache()
def get_probability(input_data):
    url_params = ''
    for key, value in input_data.items():
        url_params += f'{key}={value}&'
    response = requests.get(f'{ENDPOINT}/inference?{url_params}').json()
    return response['probability']


@st.cache
def get_options():
    return requests.get(f'{ENDPOINT}/options').json()['categories']


def batch_inference(file):
    return requests.post(f'{ENDPOINT}/batch_inference', files={'file': file})


options = get_options()

help = {
    'CustomerID': 'A unique ID that identifies each customer.',
    'gender': 'The customer’s gender: Male, Female',
    'Age': 'The customer’s current age, in years, at the time the fiscal quarter ended.',
    'SeniorCitizen': 'Indicates if the customer is 65 or older: Yes, No',
    'Partner': 'Indicates if the customer is married: Yes, No',
    'Dependents': 'Indicates if the customer lives with any dependents: Yes, No. Dependents could be children, parents, grandparents, etc.',
    'NumberofDependents': 'Indicates the number of dependents that live with the customer.',
    'PhoneService': 'Indicates if the customer subscribes to home phone service with the company: Yes, No',
    'MultipleLines': 'Indicates if the customer subscribes to multiple telephone lines with the company: Yes, No',
    'InternetService': 'Indicates if the customer subscribes to Internet service with the company: No, DSL, Fiber Optic, Cable.',
    'OnlineSecurity': 'Indicates if the customer subscribes to an additional online security service provided by the company: Yes, No',
    'OnlineBackup': 'Indicates if the customer subscribes to an additional online backup service provided by the company: Yes, No',
    'DeviceProtection': 'Indicates if the customer subscribes to an additional device protection plan for their Internet equipment provided by the company: Yes, No',
    'TechSupport': 'Indicates if the customer subscribes to an additional technical support plan from the company with reduced wait times: Yes, No',
    'StreamingTV': 'Indicates if the customer uses their Internet service to stream television programing from a third party provider: Yes, No. The company does not charge an additional fee for this service.',
    'StreamingMovies': 'Indicates if the customer uses their Internet service to stream movies from a third party provider: Yes, No. The company does not charge an additional fee for this service.',
    'Contract': 'Indicates the customer’s current contract type: Month-to-Month, One Year, Two Year.',
    'PaperlessBilling': 'Indicates if the customer has chosen paperless billing: Yes, No',
    'PaymentMethod': 'Indicates how the customer pays their bill: Bank Withdrawal, Credit Card, Mailed Check',
    'MonthlyCharges': 'Indicates the customer’s current total monthly charge for all their services from the company.',
    'TotalCharges': 'Indicates the customer’s total charges, calculated to the end of the quarter specified above.',
    'Tenure': 'Indicates the total amount of months that the customer has been with the company.',
    'Churn': 'Yes = the customer left the company this quarter. No = the customer remained with the company. Directly related to Churn Value.',
}

form = {
    'gender': 'Male',
    'SeniorCitizen': 0,
    'Partner': 'No',
    'Dependents': 'No',
    'tenure': 1,
    'PhoneService': 'Yes',
    'MultipleLines': 'No',
    'InternetService': 'Fiber optic',
    'OnlineSecurity': 'No',
    'OnlineBackup': 'No',
    'DeviceProtection': 'No',
    'TechSupport': 'No',
    'StreamingTV': 'No',
    'StreamingMovies': 'No',
    'Contract': 'Month-to-month',
    'PaperlessBilling': 'Yes',
    'PaymentMethod': 'Electronic check',
    'MonthlyCharges': 20.05,
    'TotalCharges': 20.2
}

st.title('Welcome to the Customer Churn Prediction App!')
col_1, col_2, ttt = st.columns([1, 1, 2])

col_1.markdown('<h2 style="height:78px">Personal</h2>', unsafe_allow_html=True)
col_2.markdown('<div style="height:78px"></div>', unsafe_allow_html=True)
ttt.markdown('<h2 style="height:102px">Analysis</h2>', unsafe_allow_html=True)

form['gender'] = col_1.selectbox('Gender', options['gender'], help=help['gender'])
form['SeniorCitizen'] = col_2.selectbox('Senior Citizen', [0, 1], format_func=lambda x: 'Yes' if x == 1 else 'No', help=help['SeniorCitizen'])
form['Partner'] = col_1.selectbox('Partner', options['Partner'], options['Partner'].index('No'), help=help['Partner'])
form['Dependents'] = col_2.selectbox('Dependents', options['Dependents'], help=help['Dependents'])

col_1.markdown('<h2 style="height:78px">Payment</h2>', unsafe_allow_html=True)
col_2.markdown('<div style="height:78px"></div>', unsafe_allow_html=True)

form['PaymentMethod'] = col_1.selectbox('Payment Method', options['PaymentMethod'], help=help['PaymentMethod'])
form['PaperlessBilling'] = col_2.selectbox('Paperless Billing', options['PaperlessBilling'], options['PaperlessBilling'].index('No'),
                                           help=help['PaperlessBilling'])
form['MonthlyCharges'] = col_1.number_input('Monthly Charges', min_value=0, help=help['MonthlyCharges'])
form['TotalCharges'] = col_2.number_input('Total Charges', min_value=0, help=help['TotalCharges'])

col_1, col_2, col_3, col_4 = st.columns(4)

col_1.markdown('<h2 style="height:78px">Contract</h2>', unsafe_allow_html=True)
col_2.markdown('<h2 style="height:78px">Service</h2>', unsafe_allow_html=True)
col_3.markdown('<div style="height:78px"></div>', unsafe_allow_html=True)
col_4.markdown('<div style="height:78px"></div>', unsafe_allow_html=True)

form['Tenure'] = col_1.number_input('Tenure', min_value=1, max_value=int(12 * 15), value=1, step=1, help=help['Tenure'])
form['Contract'] = col_1.selectbox('Contract', options['Contract'], help=help['Contract'])

form['PhoneService'] = col_2.selectbox('Phone Service', options['PhoneService'], help=help['PhoneService'])
if form['PhoneService'] == 'Yes':
    option = options['MultipleLines'].copy()
    option.remove('No phone service')
    form['MultipleLines'] = col_2.selectbox('Multiple Lines', option, help=help['MultipleLines'])
else:
    form['MultipleLines'] = 'No phone service'

form['InternetService'] = col_2.selectbox('Internet Service', options['InternetService'], options['InternetService'].index('No'), help=help['InternetService'])

if form['InternetService'] == 'No':
    form['OnlineSecurity'] = 'No internet service'
    form['OnlineBackup'] = 'No internet service'
    form['DeviceProtection'] = 'No internet service'
    form['TechSupport'] = 'No internet service'
    form['StreamingTV'] = 'No internet service'
    form['StreamingMovies'] = 'No internet service'
else:
    option = options['OnlineSecurity'].copy()
    option.remove('No internet service')
    form['OnlineSecurity'] = col_3.selectbox('Online Security', option, help=help['OnlineSecurity'])
    form['OnlineBackup'] = col_3.selectbox('Online Backup', option, help=help['OnlineBackup'])
    form['DeviceProtection'] = col_3.selectbox('Device Protection', option, help=help['DeviceProtection'])
    form['TechSupport'] = col_4.selectbox('Tech Support', option, help=help['TechSupport'])
    form['StreamingTV'] = col_4.selectbox('Streaming TV', option, help=help['StreamingTV'])
    form['StreamingMovies'] = col_4.selectbox('Streaming Movies', option, help=help['StreamingMovies'])

with ttt:
    probability = get_probability(form)
    if probability < 33:
        color = '#30FF6B'
    elif probability < 66:
        color = '#00BCFF'
    else:
        color = '#FF4B4B'

    option = {
        "series": [{
            "name": "Churn",
            "type": 'gauge',
            "startAngle": 180,
            "endAngle": 0,
            "progress": {
                "show": "true"
            },
            "radius": '100%',
            "itemStyle": {
                "color": color,
                "shadowColor": f'{color}AA',
                "shadowBlur": 10,
                "shadowOffsetX": 2,
                "shadowOffsetY": 2,
                "radius": '55%',
            },
            "detail": {
                "valueAnimation": "true",
                "formatter": '{value}%',
                "backgroundColor": color,
                "borderColor": '#999',
                "borderWidth": 4,
                "width": '60%',
                "lineHeight": 20,
                "height": 20,
                "borderRadius": 188,
                "offsetCenter": [0, '40%'],
            },
            "data": [{
                "value": probability,
                "name": 'Churn Probability'
            }]
        }]
    }

    st_echarts(options=option, key="1")
    st.markdown(f"""
        <div style='margin-top:-100px'>
            <h6>Customer Analysis</h6>
            <p>From The <b>'Customer Information'</b> our model predict that customer have <b>{probability}%</b> Chance of being <b>'Churn'</b></p>
        </div>
        """, unsafe_allow_html=True)

st.markdown('---')
st.title('Batch Customer Churn Prediction')

col_1_a, col_2 = st.columns([2, 2])
file = col_2.file_uploader('Upload your file', type='csv')
col_1_a.markdown("""
if you working with large amount of data,  
you can use batch prediction just download the CSV template and fill it with your data
""")

col_1, col_2, col_3 = st.columns([2, 1, 1])
col_2.download_button('Download Template', data=open('res/template.csv', 'r').read(), file_name='template.csv')

if file is not None:
    response = batch_inference(file)
    file.seek(0)

    if response.status_code == 200:
        df = pd.read_csv(file)
        df['Churn Probability'] = response.json()['probabilities']
        st.write(df)
        csv = df.to_csv(index=False)
        col_3.download_button('Download Result', data=csv, file_name='churn_probability.csv')
