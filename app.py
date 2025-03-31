import streamlit as st
import pickle
import numpy as np

pipe = pickle.load(open('pipe.pkl','rb'))
df = pickle.load(open('df.pkl','rb'))
st.title("Laptop predictor")


company = st.selectbox('brand',df['Company'].unique())

type = st.selectbox('Type',df['TypeName'].unique())

Ram = st.selectbox('RAM(in GB)',[2,4,6,8,12,16,24,32,64])

weight = st.number_input('weight of the Laptops')

touchscreen = st.selectbox('TouchScreen',['yes','no'])

ips = st.selectbox('ips',['no','yes'])

Screen_size = st.number_input('Screen size')

resolution = st.selectbox('Screen Resolution',['1920x1080','1366x768','1600x1900','3840x2160','3200x1800','2880x1800','2560x1600','2560x1440','2304x1440'])


Cpu = st.selectbox('Cpu',df['CPU brand'].unique())

hdd = st.selectbox('HDD(in GB)',[0,128,256,512,1024,2048])

ssd = st.selectbox("SSD (in GB)",[0,8,128,256,512,1024])

Gpu = st.selectbox('Gpu',df['Gpu brand'].unique())

os = st.selectbox('OS',df['os'].unique())

if st.button('Predict Price'):

    if touchscreen == 'yes':
        touchscreen = 1
    else:
        touchscreen = 0

    if ips == 'yes':
        ips = 1
    else:
        ips = 0

    x_res = int(resolution.split('x')[0])
    y_res = int(resolution.split('x')[1])
    ppi = ((x_res**2) + (y_res**2))**0.5/Screen_size

    query = np.array([company,type,Ram,weight,touchscreen,ips,ppi,Cpu,hdd,ssd,Gpu,os])

    query = query.reshape(1,12)
    st.title("The predicted price of this Configuration is  :"+ str(int(np.exp(pipe.predict(query)))))


=======
import streamlit as st
import pickle
import numpy as np

pipe = pickle.load(open('pipe.pkl','rb'))
df = pickle.load(open('df.pkl','rb'))
st.title("Laptop predictor")


company = st.selectbox('brand',df['Company'].unique())

type = st.selectbox('Type',df['TypeName'].unique())

Ram = st.selectbox('RAM(in GB)',[2,4,6,8,12,16,24,32,64])

weight = st.number_input('weight of the Laptops')

touchscreen = st.selectbox('TouchScreen',['yes','no'])

ips = st.selectbox('ips',['no','yes'])

Screen_size = st.number_input('Screen size')

resolution = st.selectbox('Screen Resolution',['1920x1080','1366x768','1600x1900','3840x2160','3200x1800','2880x1800','2560x1600','2560x1440','2304x1440'])


Cpu = st.selectbox('Cpu',df['CPU brand'].unique())

hdd = st.selectbox('HDD(in GB)',[0,128,256,512,1024,2048])

ssd = st.selectbox("SSD (in GB)",[0,8,128,256,512,1024])

Gpu = st.selectbox('Gpu',df['Gpu brand'].unique())

os = st.selectbox('OS',df['os'].unique())

if st.button('Predict Price'):

    if touchscreen == 'yes':
        touchscreen = 1
    else:
        touchscreen = 0

    if ips == 'yes':
        ips = 1
    else:
        ips = 0

    x_res = int(resolution.split('x')[0])
    y_res = int(resolution.split('x')[1])
    ppi = ((x_res**2) + (y_res**2))**0.5/Screen_size

    query = np.array([company,type,Ram,weight,touchscreen,ips,ppi,Cpu,hdd,ssd,Gpu,os])

    query = query.reshape(1,12)
    st.title("The predicted price of this Configuration is  :"+ str(int(np.exp(pipe.predict(query)))))


>>>>>>> 650a217338d940b391a65e00a2b383cd8b74efaa
