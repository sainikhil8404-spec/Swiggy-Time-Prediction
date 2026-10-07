import pickle
import streamlit as st
import pandas as pd

model = pickle.load(open('Time Predection.pkl', 'rb'))
df = pd.read_csv('swiggy_demographic.csv')

st.image(
    r"D:\all sai\innomatics\ML\projects\image\image_99ef8f1f.jpg",
    width=700
)

st.title(
    'Swiggy Delivery Time Prediction',
    text_alignment='center'
)

st.text(
    'Lets predict the time taken by swiggy to deliver the order based on the given details'
)

# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------

if "started" not in st.session_state:
    st.session_state.started = False

if "prediction_done" not in st.session_state:
    st.session_state.prediction_done = False


# ---------------------------------------------------
# START BUTTON
# ---------------------------------------------------

if not st.session_state.started:

    if st.button(
        'Click here to predict the delivery time',
        use_container_width=True
    ):
        st.session_state.started = True
        st.rerun()


# ---------------------------------------------------
# INPUT FORM
# ---------------------------------------------------

if st.session_state.started:


    st.header("Rider Details")
    col4,col5,col6 = st.columns(3)

    with col4:
        age = st.number_input(
            "Age",
            min_value=float(df["age"].min()),
            max_value=float(df["age"].max()),
            value=float(df["age"].min())
        )

        ratings = st.number_input(
            "Ratings",
            min_value=float(df["ratings"].min()),
            max_value=float(df["ratings"].max()),
            value=float(df["ratings"].min()),
            step=0.1
    )

    with col5:
        vehicle_condition = st.number_input(
            "Vehicle Condition",
            min_value=float(df["vehicle_condition"].min()),
            max_value=float(df["vehicle_condition"].max()),
            value=float(df["vehicle_condition"].min())
        )

        multiple_deliveries = st.number_input(
            "Multiple Deliveries",
            min_value=float(df["multiple_deliveries"].min()),
            max_value=float(df["multiple_deliveries"].max()),
            value=float(df["multiple_deliveries"].min())
        )

    with col6:
        festival = st.selectbox(
            "Is Festival",
            df["festival"].unique()
        )



    
    st.header("Order Details")

    col7,col8,col9 = st.columns(3)
    with col7:
        type_of_order = st.selectbox(
            "Type of Order",
            df["type_of_order"].unique()
        )

        type_of_vehicle = st.selectbox(
            "Type of Vehicle",
            df["type_of_vehicle"].unique()
        )

    with col8:
        weather = st.selectbox(
            "Weather",
            df["weather"].unique()
        )

        traffic = st.selectbox(
            "Traffic",
            df["traffic"].unique()
        )

    with col9:
        city_type = st.selectbox(
            "City Type",
            df["city_type"].unique()
        )



    st.header("Location Details")

    col10,col11,col12 = st.columns(3)
    with col10:
        city_name = st.selectbox(
            "City Name",
            df["city_name"].unique()
        )

            
        distance = st.number_input(
            "Distance",
            min_value=float(df["distance"].min()),
            value=float(df["distance"].min()),
            step=0.1
        )


    with col11:
        restaurant_longitude = st.number_input(
            "Restaurant Longitude",
            value=float(df["restaurant_longitude"].min()),
            format="%.6f"
        )

        delivery_latitude = st.number_input(
            "Delivery Latitude",
            value=float(df["delivery_latitude"].min()),
            format="%.6f"
        )

    with col12:
        
        restaurant_latitude = st.number_input(
            "Restaurant Latitude",
            value=float(df["restaurant_latitude"].min()),
            format="%.6f"
        )

        delivery_longitude = st.number_input(
            "Delivery Longitude",
            value=float(df["delivery_longitude"].min()),
            format="%.6f"
        )



    st.header("Time Details")

    col13,col14,col15 = st.columns(3)

    with col13:
        order_month = st.selectbox(
            "Order Month",
            df["order_month"].unique()
        )
        order_time_of_day = st.selectbox(
            "Order Time of Day",
            df["order_time_of_day"].unique()
        )

        pickup_time_minutes = st.number_input(
            "Pickup Time (Minutes)",
            min_value=float(df["pickup_time_minutes"].min()),
            max_value=float(df["pickup_time_minutes"].max()),
            value=float(df["pickup_time_minutes"].min())
        )

    with col14:
        order_day_of_week = st.selectbox(
            "Order Day of Week",
            df["order_day_of_week"].unique()
        )

        order_time_hour = st.number_input(
            "Order Time Hour",
            min_value=float(df["order_time_hour"].min()),
            max_value=float(df["order_time_hour"].max()),
            value=float(df["order_time_hour"].min())
        )


    with col15:

        order_day = st.number_input(
            "Order Day",
            min_value=float(df["order_day"].min()),
            max_value=float(df["order_day"].max()),
            value=float(df["order_day"].min())
        )

    

        is_weekend = st.selectbox(
            "Is Weekend",
            [0, 1]
        )

    
    

    predict_button = st.button(
        "Predict Delivery Time",
        use_container_width=True
    )


# ---------------------------------------------------
# PREDICTION
# ---------------------------------------------------

    if predict_button:

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

            'festival': [festival],

            'city_type': [city_type],
            'city_name': [city_name],

            'order_time_of_day': [order_time_of_day],
            'order_day_of_week': [order_day_of_week],

            'order_day': [order_day],
            'order_month': [order_month],

            'is_weekend': [is_weekend],

            'pickup_time_minutes': [pickup_time_minutes],
            'order_time_hour': [order_time_hour],

            'distance': [distance]
        })

        prediction = model.predict(input_data)

        prediction_value = float(prediction[0])

        st.session_state.prediction_done = True


        # ---------------------------------------------------
        # RESULT
        # ---------------------------------------------------

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

        progress = float(
            min(prediction_value / 90, 1.0)
        )

        st.progress(progress)

        st.caption(
            f"Estimated delivery time: "
            f"{prediction_value:.2f} minutes"
        )


        # ---------------------------------------------------
        # PREDICT AGAIN
        # ---------------------------------------------------

        if st.button(
            "Predict Again",
            use_container_width=True
        ):

            st.session_state.prediction_done = False
            st.rerun()