import pickle
import streamlit as st
import pandas as pd

model = pickle.load(open('Time Predection.pkl', 'rb'))
df = pd.read_csv('swiggy_demographic.csv')

st.image(r"D:\all sai\innomatics\ML\projects\image\image_99ef8f1f.jpg",width=700)
st.title('Swiggy Delivery Time Prediction',text_alignment = 'center')
st.text('Lets predict the time taken by swiggy to deliver the order based on the given details')
col1, col2 = st.columns(2)
if st.button('Click here to predict the delivery time '):
# st.sidebar.title('Enter the details,Below')
    col3,col4,col5,col6 = st.columns(4)
    with col3:
        st.header("Rider Details")
        order_month = st.selectbox(
            "Order Month",
            df["order_month"].unique()
        )
        age = st.number_input(
            "Age",
            min_value=df["age"].min(),
            max_value=df["age"].max(),
            value=df["age"].min()
        )
        ratings = st.number_input(
            "Ratings",
            min_value=df["ratings"].min(),
            max_value=df["ratings"].max(),
            value=df["ratings"].min(),
            step=0.1
        )
        vehicle_condition = st.number_input(
            "Vehicle Condition",
            min_value=df["vehicle_condition"].min(),
            max_value=df["vehicle_condition"].max(),
            value=df["vehicle_condition"].min()
        )
        multiple_deliveries = st.number_input(
            "Multiple Deliveries",
            min_value=df["multiple_deliveries"].min(),
            max_value=df["multiple_deliveries"].max(),
            value=df["multiple_deliveries"].min()
        )
        festival = st.selectbox(
            "Is Festival",
            df["festival"].unique()
        )
    with col4:
        st.header("Order Details")
        type_of_order = st.selectbox(
            "Type of Order",
            df["type_of_order"].unique()
        )
        type_of_vehicle = st.selectbox(
            "Type of Vehicle",
            df["type_of_vehicle"].unique()
        )
        weather = st.selectbox(
            "Weather",
            df["weather"].unique()
        )
        traffic = st.selectbox(
            "Traffic",
            df["traffic"].unique()
        )
        city_type = st.selectbox(
            "City Type",
            df["city_type"].unique()
        )
    with col5:
        st.header("Location Details")
        city_name = st.selectbox(
            "City Name",
            df["city_name"].unique()
        )
        restaurant_latitude = st.number_input(
            "Restaurant Latitude",
            value=df["restaurant_latitude"].min(),
            format="%.6f"
        )
        restaurant_longitude = st.number_input(
            "Restaurant Longitude",
            value=df["restaurant_longitude"].min(),
            format="%.6f"
        )
        delivery_latitude = st.number_input(
            "Delivery Latitude",
            value=df["delivery_latitude"].min(),
            format="%.6f"
        )
        delivery_longitude = st.number_input(
            "Delivery Longitude",
            value=df["delivery_longitude"].min(),
            format="%.6f"
        )
        distance = st.number_input(
            "Distance",
            min_value=df["distance"].min(),
            value=df["distance"].min(),
            step=0.1
        )
    with col6:
        st.header("Time Details")
        order_time_of_day = st.selectbox(
            "Order Time of Day",
            df["order_time_of_day"].unique()
        )
        order_day_of_week = st.selectbox(
            "Order Day of Week",
            df["order_day_of_week"].unique()
        )

        order_day = st.number_input(
            "Order Day",
            min_value=df["order_day"].min(),
            max_value=df["order_day"].max(),
            value=df["order_day"].min()
        )
        order_time_hour = st.number_input(
            "Order Time Hour",
            min_value=df["order_time_hour"].min(),
            max_value=df["order_time_hour"].max(),
            value=df["order_time_hour"].min()
        )
        is_weekend = st.selectbox(
            "Is Weekend",
            [0, 1]
        )
        pickup_time_minutes = st.number_input(
            "Pickup Time (Minutes)",
            min_value=df["pickup_time_minutes"].min(),
            max_value=df["pickup_time_minutes"].max(),
            value=df["pickup_time_minutes"].min()
        )



        predict_button = st.button(
            "Predict Delivery Time",
            use_container_width=True
        )


    if predict_button:
        st.session_state.started = True


        input_data = pd.DataFrame({
                'age': [age],
                'ratings': [ratings],
                'restaurant_latitude': [restaurant_latitude],
                'restaurant_longitude': [restaurant_longitude],
                'delivery_latitude': [delivery_latitude],
                'delivery_longitude': [delivery_longitude],
                'weather': [weather],
                'traffic': [traffic],
                'vehicle_condition': [vehicle_condition],
                'type_of_order': [type_of_order],
                'type_of_vehicle': [type_of_vehicle],
                'multiple_deliveries': [multiple_deliveries],
                'festival' : [festival],
                'city_type': [city_type],
                'city_name': [city_name],
                'order_time_of_day': [order_time_of_day],
                'order_day_of_week': [order_day_of_week],
                'order_day': [order_day],
                "order_month": [order_month],
                'is_weekend': [is_weekend],
                'pickup_time_minutes': [pickup_time_minutes],
                'order_time_hour': [order_time_hour],
                'distance': [distance]
            })

        prediction = model.predict(input_data)

        prediction_value = float(prediction[0])

        st.markdown("## Delivery Prediction")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                    "Estimated Time",
                    f"{prediction_value:.2f} min"
            )

        with col2:
            st.metric(
                "Distance",
                f"{float(distance):.2f} km"
                )

        with col3:
                st.metric(
                    "Rider Rating",
                    f"{float(ratings):.1f}"
                )

        if prediction_value <= 30:
                category = "Fast Delivery"

        elif prediction_value <= 45:
                category = "Normal Delivery"

        elif prediction_value <= 60:
                category = "Slightly Longer Delivery"

        else:
                category = "Long Delivery Time"

        st.success(category)

        st.markdown("### Estimated Delivery Time")

        progress = float(min(prediction_value / 90, 1.0))

        st.progress(progress)

        st.caption(
                f"Estimated delivery time: {prediction_value:.2f} minutes"
            )

        st.button("Predict Again", on_click=lambda: st.experimental_rerun())
        st.session_state.started = True