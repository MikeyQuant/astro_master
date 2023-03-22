import skychart as sch
from datetime import datetime
import streamlit as st
from streamlit_js_eval import get_geolocation
import plotly.express as px
import pandas as pd
import geocoder

st.sidebar.header("Astronomy Labs:")
mode=st.sidebar.radio("Select Lab:",["Scale of the Universe","To Scale","Finding Your Way","Sky Safari Scavenger Hunt","Circumpolar Stars","Where Does Space Begin?","Evidence of Ninth Planet","Discovering Asterisms","Astrobites","Measuring Brightness","Our Galaxy","Cosmic Minute"])
if mode=="Discovering Asterisms":
    st.write("The following is an Asterism Generator. You can generate random asterisms or create your own.")
    loc = get_geolocation()
    st.write("Location:")
    try:
        st.write(loc["coords"])
        lat = loc["coords"]["latitude"]
        lon = loc["coords"]["longitude"]
    except:
        lat = 41.6909512
        lon = -70.3370139

    # entering the location name


    # printing address

    t = datetime.now()
    obs_loc = (lat, lon)
    option = st.radio("Select Constellation Generator Mode:",
                      ["Burst Generator", "Custom Constellation", "Random Generator"])

    n = int(st.number_input("Enter number of constellations desires", value=1,step=1))
    nn = int(st.number_input("Enter number of lines per constellation", value=5,step=1))
    st.write("The slider below allows you to filter out less bright stars as to be able to generate asterisms in low visibility conditions")
    # Base dataframe
    filt = st.slider("Max Magnitude Shown", -1.0, 10.0, 5.0, .1)

    df = sch.visible_hipparcos(obs_loc, t)
    dfo = df[df['Vmag'] < filt]
    df = dfo.reset_index()
    st.write(df)

    # DataFrame of stars that will be shown

    import random

    # Load constellation data
    dc_const = sch.load_constellations()

    dc_const = {}
    lst = df["hip"].to_list()
    if option == "Burst Generator":

        for i in range(n):
            dc_const[str(i)] = []
            random.shuffle(lst)

            for ii in range(nn):
                dc_const[str(i)].append([lst[0], lst[random.randrange(0, len(lst))]])

    elif option == "Custom Constellation":
        cst = {}
        names = []
        st.header("Custom Constellations")
        st.write(
            "For each line making up a constellation, enter in the HIP of the stars you'd like to connect (use table above).")
        for i in range(n):
            st.subheader("Constellation {}".format(i + 1))
            names.append(st.text_input("What is the name of your constellation?", "Constellation {}".format(i + 1), key=i))
            dc_const[names[i]] = []
            c1, c2 = st.columns(2)
            for ii in range(nn):
                c1.write("Line {}".format(ii + 1))
                c2.write(":")
                dc_const[names[i]].append([c1.selectbox("select star #", df["hip"], key=str(ii) + str(i)),
                                           c2.selectbox("select star #", df["hip"], key=str(ii) + str(i) + "2")])

    elif option == "Random Generator":

        for i in range(n):
            dc_const[str(i)] = []
            random.shuffle(lst)

            for ii in range(nn):
                if ii == 0:
                    first = lst[0]
                    last = lst[random.randrange(0, len(lst))]

                    dc_const[str(i)].append([lst[0], last])
                elif ii == nn - 1:
                    dc_const[str(i)].append([last, first])
                else:
                    orgin = last
                    last = lst[random.randrange(0, len(lst))]

                    dc_const[str(i)].append([orgin, last])

    # st.write(dc_const)
    # Show only Ursa Major and Cassiopeia constellations
    # dc_const = {'UMa': dc_const['UMa'],
    # 'Cas': dc_const['Cas']}


    fig, ax, df_show = sch.draw_chart(dfo, dfo, dc_const, alpha=1)
    st.pyplot(fig)
    if st.button("re-run"):
        st._rerun()
elif mode=="Scale of the Universe":
    file = open("/Users/mikebelliveau/Desktop/Python/Astronomy/astronomy-lab-1/astro_scale.txt", "r").read()

    ls = []
    for m in file.split("\n"):
        st.write(m)
        data = {}
        ob = m.split(":")[0]
        base = (m.split(":")[1].split("x")[0].replace(" ", ""))
        exp = (m.split(":")[1].split("^")[1].replace(" m", ""))
        n = float(base + "E+" + exp)
        data["distance"] = n
        data["object"] = ob
        ls.append(data)
    for k, v in data.items():
        print(k, v, type(v))
    df = pd.DataFrame(ls)
    d1 = []
    for dis, obj in zip(df["distance"], df["object"]):
        d2 = []
        d2.append(obj)
        for dis2, obj2 in zip(df["distance"], df["object"]):
            d2.append(dis2 / dis)
        d1.append(d2)
    dfm = pd.DataFrame(d1, columns=["Measured"] + [x for x in df["object"]])
    st.header("Distance Ratio Matrix")
    st.write(
        "The table below shows how many times one distance can fit into another distance. Simply put, the numbers represent the distance of the objects in the column names divided by the distance of the object in the Measured column ")
    st.write(dfm)
    objects = []
    st.header("Distance Illustration")
    st.write("Select distances to Graph")
    for o in df["object"]:
        y = st.checkbox(o, True, key=o)
        if y:
            objects.append(o)
    st.header(" ")
    dff = df[df["object"].isin(objects)]
    log = st.checkbox("Use Log Scale?", True)
    fig = px.bar(dff, x="object", y="distance", color="object", log_y=log)
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig)
elif mode=="Measuring Brightness":
    #st.set_page_config(layout="wide")
    st.header("Measuring Brightness")
    st.subheader("Datetime of observation: March 13th 2023, 2:59PM - 5:59PM")
    st.subheader(f"Coordinates: 41.7057, -70.2286")
    st.header("Guessing Leo's Magnitudes")
    c2 = st.beta_columns(3)
    c2[1].image("IMG_0133.jpg")

    d = [["Ras Elased Australis", 4.1, 3.0], ["Ras Elased Borealis", 5.3, 4.9], ["Adhafera", 4.6, 3.4],
         ["Algieba", 2.0, 3.5], ["Eta Leonis", 4.0, 3.5], ["Regulus", 1.2, 1.4], ["Chertan", 3.2, 3.3],
         ["Zosma", 2.2, 2.5], ["Denebola", 1.9, 2.1]]
    df = pd.DataFrame(d, columns=["Star", "Guessed Magnitude", "Actual Magnitude"])
    df["Guess Delta"] = abs(df["Actual Magnitude"] - df["Guessed Magnitude"])
    st.header("My Guesses")

    st.dataframe(df)
    fig = px.scatter(df, x="Actual Magnitude", y="Guessed Magnitude", size="Guess Delta", hover_name="Star")
    st.plotly_chart(fig)
    st.write(
        "Upon observation of my guesses, it is apparent that I am worse at guessing stars in the 3-4 Magnitude range than any other. The size of the dots in the above scatterplot shows the absolute difference between my guess and the actual magnitude. This shows that with the exception of Chertan, it is difficult to guess stars at the middle range of magnitudes of a constellation.")
    c = st.beta_columns(3)
    ii = 0
    for x in range(129, 133):
        if x == 130:
            continue

        c[ii].image(f"IMG_0{x}.png")
        ii += 1
    st.write(
        "Venus and a Full Moon have are significantly brighter than Sirius. This is due to their close proximity to earth. If we were to observe the absolute magnitude, Sirius would be the brightest object.")

    st.header("Apparent vs Absolute Magnitude")
    st.write(
        "In principal, if a star is less than 10 parsecs away from Earth, its apparent magnitude will be higher than its absolute magnitude. This is because the further you are from an object, the less light can be observed. Conversley, if a star is further than 10 parsecs, its absolute magnitude will be greater than its apparent magnitude.")
elif mode=="Circumpolar Stars":
    g = geocoder.ip('me')

    st.header("Circumpolar Stars")
    st.subheader("Datetime of observation: March 13th 2023, 2:59PM - 5:59PM")
    st.subheader(f"Coordinates: 41.7057, -70.2286")

    cs=st.beta_columns(3)
    print(cs)
    for i in range(120,123):
        ii=i-120

        cs[ii].image(f"IMG_0{i}.png")
    st.subheader("Analysis")
    st.write("This was a very interesting lab because I learned something through my own findings. As you can see in the pictures, as time goes on"
             " the constelation Ursa Major rotates counter clockwise. However, the star Polaris, which is in Ursa Minor, remains fixed. With the movement of the stars occuring because of earths rotation,"
             " the only explaination for why Polaris remains fixed is that Polaris is the North Star. in order to make sense of this. Imagine there is a literal pole sticking out of the North pole. This pole would be pointing strait to Polaris at all times because Polaris is perpendicular to the axis of rotaion."
             )
elif mode=="Our Galaxy":
    st.header("Our Galaxy")
    st.subheader("Datetime of observation: March 13th 2023, 2:59PM - 5:59PM")
    st.subheader(f"Coordinates: 41.7057, -70.2286")
    st.header("My Observation")
    st.write("""I observed the Milky Way in the night sky with my eyes. It was a beautiful sight, with a bright, hazy band of stars stretching across the sky. I could see many clusters of stars, some bright and some dim. There were also several regions of bright and dark nebulosity visible, particularly near the center of the Milky Way. The Milky Way appeared to be most prominent in the southern sky, and it seemed to be brightest in the direction of Sagittarius. The overall shape of the Milky Way was curved, with a central bulge towards the center.""")
    st.header("Comparison to WSH")
    st.write("""Walter Scott Houston's observations of the Milky Way were similar to my own. He noticed a bright, hazy band of stars stretching across the sky, with many clusters of stars and several regions of bright and dark nebulosity. He also observed that the Milky Way was most prominent in the southern sky, and brightest in the direction of Sagittarius. He also noted the overall curved shape of the Milky Way, with a central bulge towards the center. In addition, he wrote about how thin the disk of our galaxy really is, and how closely packed the stars are within it. We both also noted the straightness of the Milky Way's band, and how it seemed to be following a purposeful straight line across the sky. Finally, we both discussed the importance of the Milky Way in human culture, with Walter Scott Houston recounting a folk tale about two star-crossed lovers.""")

elif mode=="Cosmic Minute":
    st.video("https://youtu.be/G1T4kN4-tUQ")

elif mode=="To Scale":
    st.video("https://youtu.be/30ZwDOnvkNE")
elif mode=="Finding Your Way":
    st.video("https://youtu.be/yAXeAbZqyJg")
elif mode=="Astrobites":
    st.video("https://youtu.be/Rhp84ylramk")
elif mode=="Sky Safari Scavenger Hunt":
    st.video("https://youtu.be/zk54YK21LU0")
elif mode=="Where Does Space Begin?":
    st.video("https://youtu.be/CY9rW4qr6Qk")
elif mode=="Evidence of Ninth Planet":
    st.video("https://youtu.be/T-KppwRdmVc")