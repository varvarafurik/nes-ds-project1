import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly
import plotly.express as px
import plotly.graph_objects as go

with st.echo(code_location='below'):
    df = pd.read_csv("1310038301_territory.csv")
    gender = pd.read_csv("1310038301_gender.csv")
    age = pd.read_csv("1310038301_age.csv")
    df.drop(columns = ['DGUID','SCALAR_FACTOR','SCALAR_ID','VECTOR','COORDINATE','STATUS','TERMINATED','DECIMALS'])
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    #BLOCK1

    mean_ter = df[(df['Self-reported cannabis use in the past three months'] == "Percentage of people")]
    mean_ter = mean_ter.groupby("GEO").mean()
    mean_ter.reset_index(level=0, inplace=True)
    sns.set(rc={'figure.figsize':(25.7,14.27)})
    order=['Canada', 'Alberta', 'British Columbia','Iqaluit (Nunavut)', 'Manitoba', 'New Brunswick', 'Newfoundland and Labrador', 'Nova Scotia', 'Ontario',
    'Prince Edward Island', 'Quebec', 'Saskatchewan', 'Whitehorse (Yukon)',  'Yellowknife (Northwest Territories)']
    Can_per = (float(mean_ter[mean_ter["GEO"] == "Canada"]["VALUE"]))
    matplotlib.rc_file_defaults()
    #ax1 = sns.set_style(style=None, rc=None )
    fig1, ax1 = plt.subplots(figsize=(30.7,14.27))
    sns.barplot(x='VALUE', y="GEO", data=mean_ter, orient='h', order=order, ax=ax1)
    ax1.set_title("Average percentage of users in Canada, and province, territory", fontdict= { 'fontsize': 24, 'fontweight':'bold'})
    plt.xlabel("Percentage of users")
    plt.ylabel("Province or territory")
    ax2 = ax1.twinx()
    #mark=[[1, 5, 0], [1,5,25], [2, 5, 0], [2,5,25], [3, 5, 0], [3,5,25]]
    #marks = pd.DataFrame(mark, columns=['number', "perc1", "perc2"], dtype=float)
    sns.lineplot(x=[Can_per-5, Can_per-5], y=[0,30.7], ax=ax2, markers=True, color="blue")
    ax3 = ax1.twinx()
    sns.lineplot(x=[Can_per+5, Can_per+5], y=[0, 30.7], ax=ax3, markers=True, color="blue")
    ax3.text(25.85, 28.85, '8 out of 13 territories are in 5% interval', fontsize=12)
    ax3.text(25.85, 29.85, 'Red line indicates the average in the country', fontsize=12)
    plt.axvline(Can_per, color='red')
    st.pyplot(fig1)

    #BLOCK2

    quat_ter = df[(df['Self-reported cannabis use in the past three months'] == "Number of people") & (df["GEO"] != "Canada") & (df["GEO"] != 'Iqaluit (Nunavut)') & (df["GEO"] != 'Yellowknife (Northwest Territories)') & (df["GEO"] != 'Whitehorse (Yukon)')]
    fig2 = px.scatter(quat_ter, x="GEO", y="VALUE", hover_data=["REF_DATE"], color="GEO", labels={'GEO': "Province or territory", 'REF_DATE':"Quarter", "VALUE": "Number of users" })
    st.plotly_chart(fig2)

    #BLOCK3

    q1_ter = df[(df['Self-reported cannabis use in the past three months'] == "Percentage of people") & (df["GEO"] != "Canada") & (df["GEO"] != 'Iqaluit (Nunavut)') & (df["GEO"] != 'Yellowknife (Northwest Territories)') & (df["GEO"] != 'Whitehorse (Yukon)')]
    q1_ter = q1_ter.pivot("REF_DATE", "GEO", "VALUE")
    fig3 = plt.figure()
    ax3 = sns.lineplot(data=q1_ter, markers=True)
    ax3.get_legend().remove()
    plt.figlegend(bbox_to_anchor=(0.9, 0.9), loc='upper left')
    plt.xlabel("Quarter", size=12)
    plt.ylabel("Percentage of users", size=12)
    plt.title("Percentage of users per quarter in each province or territory", size = 16)
    st.pyplot(fig3)

    #BLOCK4

    fig4, ax4 = plt.subplots()
    gen_dist = gender[gender['Self-reported cannabis use in the past three months'] == "Number of people"]
   #gen_dist = gen_dist.groupby("GEO").mean()
    gen_dist.reset_index(level=0, inplace=True)
    sns.violinplot(y="VALUE", x="GEO", data=gen_dist, palette="Set2", split=True,
                    scale="count", inner="stick", estimator="mean",
                    scale_hue=False, bw=.2, ax=ax4, labels={'GEO': "Sex of users", "VALUE": "Number of users"}, title="Number of users for people of both sexex, quarterly")
    st.pyplot(fig4)

    #BLOCK5

    fig5, ax5 = plt.subplots(2, 2)
    q1,q2, q3, q4 = 5306.0, 4878.1, 5197.6, 5119.4
    s1 = [float(gen_dist[(gen_dist["REF_DATE"]=="2019-01") & (gen_dist["GEO"]=="Canada, females") & (gen_dist["UOM"]=="Number")]["VALUE"])/q1, float(gen_dist[(gen_dist["REF_DATE"]=="2019-01") & (gen_dist["GEO"]=="Canada, males") & (gen_dist["UOM"]=="Number")]["VALUE"])/q2]
    s2 = [float(gen_dist[(gen_dist["REF_DATE"] == "2019-04") & (gen_dist["GEO"] == "Canada, females") & (
                gen_dist["UOM"] == "Number")]["VALUE"]) / q2, float(gen_dist[(gen_dist["REF_DATE"] == "2019-04") & (
                gen_dist["GEO"] == "Canada, males") & (gen_dist["UOM"] == "Number")]["VALUE"]) / q2]
    s3 = [float(gen_dist[(gen_dist["REF_DATE"] == "2019-07") & (gen_dist["GEO"] == "Canada, females") & (
                gen_dist["UOM"] == "Number")]["VALUE"]) / q3, float(gen_dist[(gen_dist["REF_DATE"] == "2019-07") & (
                gen_dist["GEO"] == "Canada, males") & (gen_dist["UOM"] == "Number")]["VALUE"]) / q3]
    s4 = [float(gen_dist[(gen_dist["REF_DATE"] == "2019-10") & (gen_dist["GEO"] == "Canada, females") & (
                gen_dist["UOM"] == "Number")]["VALUE"]) / q4, float(gen_dist[(gen_dist["REF_DATE"] == "2019-10") & (
                gen_dist["GEO"] == "Canada, males") & (gen_dist["UOM"] == "Number")]["VALUE"]) / q4]
    labels="Female", "Male"
    colors=['#ff9999','#66b3ff']
    ax5[0, 0].pie(s1, labels=labels, normalize=True, radius=0.8, textprops={'fontsize': 8}, autopct='%1.1f%%', colors=colors)
    ax5[0, 0].set_title("Quarter 1", loc="center", fontsize="small")
    ax5[0, 1].pie(s2, labels=labels, normalize=True, radius=0.8, textprops={'fontsize': 8}, autopct='%1.1f%%', colors=colors)
    ax5[0, 1].set_title("Quarter 2", loc="center", fontsize="small")
    ax5[1, 0].pie(s3, labels=labels, normalize=True, radius=0.8, textprops={'fontsize': 8}, autopct='%1.1f%%', colors=colors)
    ax5[1, 0].set_title("Quarter 3", loc="center", fontsize="small")
    ax5[1, 1].pie(s4, labels=labels, normalize=True, radius=0.8, textprops={'fontsize': 8}, autopct='%1.1f%%', colors=colors)
    ax5[1, 1].set_title("Quarter 4", loc="center", fontsize="small")
    st.pyplot(fig5)

    #BLOCK6
    age_dist = age[age['Self-reported cannabis use in the past three months'] == "Percentage of people"]
    age_dist=age_dist.reset_index()
    age_dist["NUM"] = age[age['Self-reported cannabis use in the past three months'] == "Number of people"]["VALUE"].values
    print(age_dist)
    fig6=px.scatter(age_dist, x="REF_DATE", y="VALUE", animation_frame="REF_DATE", animation_group="GEO",
                    size='NUM', color="GEO", hover_name="GEO", range_x=["2019-01", "2019-12"], range_y=[0, 40])
    st.plotly_chart(fig6)
