import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px

with st.echo(code_location='below'):
    st.write('Prevalence of cannabis use in the past three months, self-reported, Canada, 2019. '
             'People shared information about their geography, sex, age group. Recreational cannabis consumption was '
             'legalaized in Canada on October 17, 2018. ')
    df = pd.read_csv("1310038301_territory.csv")
    gender = pd.read_csv("1310038301_gender.csv")
    age = pd.read_csv("1310038301_age.csv")
    df.drop(columns = ['DGUID','SCALAR_FACTOR','SCALAR_ID','VECTOR','COORDINATE','STATUS','TERMINATED','DECIMALS'])

    #BLOCK1

    mean_ter = df[(df['Self-reported cannabis use in the past three months'] == "Percentage of people")]
    mean_ter = mean_ter.groupby("GEO").mean()
    mean_ter.reset_index(level=0, inplace=True)
    sns.set(rc={'figure.figsize':(30.7,14.27)})
    order=['Canada', 'Alberta', 'British Columbia','Iqaluit (Nunavut)', 'Manitoba', 'New Brunswick', 'Newfoundland and Labrador', 'Nova Scotia', 'Ontario',
    'Prince Edward Island', 'Quebec', 'Saskatchewan', 'Whitehorse (Yukon)',  'Yellowknife (Northwest Territories)']
    Can_per = (float(mean_ter[mean_ter["GEO"] == "Canada"]["VALUE"]))
    matplotlib.rc_file_defaults()
    #ax1 = sns.set_style(style=None, rc=None )
    fig1, ax1 = plt.subplots(figsize=(30.7,14.27))
    sns.barplot(x='VALUE', y="GEO", data=mean_ter, orient='h', order=order, ax=ax1)
    ax1.set_title("Average percentage of users in Canada, provinces, and territories", fontdict= {'fontsize': 26})
    plt.xlabel("Percentage of users", fontdict= {'fontsize': 26})
    plt.ylabel("Province or territory", fontdict= {'fontsize': 26})
    ax2 = ax1.twinx()
    sns.lineplot(x=[Can_per-5, Can_per-5], y=[0,30.7], ax=ax2, markers=True, color="blue")
    ax3 = ax1.twinx()
    sns.lineplot(x=[Can_per+5, Can_per+5], y=[0, 30.7], ax=ax3, markers=True, color="blue")
    ax3.text(25.85, 28.85, '8 out of 13 territories are in 5% interval', fontsize=14)
    ax3.text(25.85, 29.85, 'Red line indicates the average in the country.', fontsize=14)
    plt.axvline(Can_per, color='red', linestyle=":")
    st.pyplot(fig1)

    #BLOCK2

    quat_ter = df[(df['Self-reported cannabis use in the past three months'] == "Number of people") & (df["GEO"] != "Canada") & (df["GEO"] != 'Iqaluit (Nunavut)') & (df["GEO"] != 'Yellowknife (Northwest Territories)') & (df["GEO"] != 'Whitehorse (Yukon)')]
    fig2 = px.scatter(quat_ter, x="GEO", y="VALUE", hover_data=["REF_DATE"], color="GEO", labels={'GEO': "Province or territory", 'REF_DATE':"Quarter", "VALUE": "Number of users" }, title="Number of users in provinces or territories, quarterly",)
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
    plt.title("Percentage of users per quarter in province or territory", size = 16)
    plt.text(2.05,33,"Nova Scotia, 32.8%")
    plt.text(0.75, 11.25, "Quebec, 10.3%")
    st.pyplot(fig3)

    #BLOCK4

    gen_dist = gender[gender['Self-reported cannabis use in the past three months'] == "Number of people"]
    gen_perc = gender[gender['Self-reported cannabis use in the past three months'] == "Percentage of people"]
    gen_perc=gen_perc.reset_index()
    gen_perc["NUM"] = gender[gender['Self-reported cannabis use in the past three months'] == "Number of people"]["VALUE"].values
    fig4=px.scatter(gen_perc, x="REF_DATE", y="VALUE", animation_frame="REF_DATE", animation_group="GEO",
                    size='NUM', color="GEO", hover_name="GEO", range_x=["2019-01", "2019-12"], range_y=[0, 40], title="Percentage of users among both sexes, quarterly",
                     labels={'REF_DATE':"Quarter", "VALUE": "Percentage of users", "NUM": "Number of users", "GEO": "Sex"})
    fig4.add_hline(12.1, line_width=1, fillcolor="red", opacity=0.2, annotation_text="Female, minimum",
                   annotation_position="bottom right")
    fig4.add_hline(22.3, line_width=1, fillcolor="blue", opacity=0.2, annotation_text="Male, maximum",
                   annotation_position="top right")

    st.plotly_chart(fig4)

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
    ax5[0, 0].pie(s1, labels=labels, normalize=True, radius=0.7, textprops={'fontsize': 8}, autopct='%1.1f%%', colors=colors)
    ax5[0, 0].set_title("Quarter 1", loc="center", fontsize="small", y=0.9)
    ax5[0, 1].pie(s2, labels=labels, normalize=True, radius=0.7, textprops={'fontsize': 8}, autopct='%1.1f%%', colors=colors)
    ax5[0, 1].set_title("Quarter 2", loc="center", fontsize="small", y=0.9)
    ax5[1, 0].pie(s3, labels=labels, normalize=True, radius=0.7, textprops={'fontsize': 8}, autopct='%1.1f%%', colors=colors)
    ax5[1, 0].set_title("Quarter 3", loc="center", fontsize="small", y=0.9)
    ax5[1, 1].pie(s4, labels=labels, normalize=True, radius=0.7, textprops={'fontsize': 8}, autopct='%1.1f%%', colors=colors)
    ax5[1, 1].set_title("Quarter 4", loc="center", fontsize="small", y=0.9)
    fig5.suptitle("Distribution of users by sex, quarterly")
    st.pyplot(fig5)

    #BLOCK6
    age_dist = age[age['Self-reported cannabis use in the past three months'] == "Percentage of people"]
    age_dist=age_dist.reset_index()
    age_dist["NUM"] = age[age['Self-reported cannabis use in the past three months'] == "Number of people"]["VALUE"].values
    fig6 = (px.scatter(age_dist, x="REF_DATE", y="VALUE", animation_frame="REF_DATE", animation_group="GEO",
                    size='NUM', color="GEO", hover_name="GEO", range_x=["2019-01", "2019-12"], range_y=[0, 40],
                    title="Percentage of users among different age groups, quarterly",
                    labels={'REF_DATE': "Quarter", "VALUE": "Percentage of users", "NUM": "Number of users", "GEO": "Age group"}))

    age_dist = age[age['Self-reported cannabis use in the past three months'] == "Percentage of people"]
    m6 = age_dist.groupby("REF_DATE").mean().reset_index()["VALUE"].mean()
    fig6.add_hline(float(m6), line_width=1, fillcolor="red", opacity=0.2, annotation_text="Average throughout the year", annotation_position="bottom right")
    st.plotly_chart(fig6)

    #BLOCK7
    age_dist = (age[age['Self-reported cannabis use in the past three months'] == "Number of people"]).rename(columns={"GEO":"Age group"})
    fig7=sns.relplot(x="REF_DATE", y="VALUE", hue="Age group", legend=False, col="Age group", height=4, kind="line", estimator=None, data=age_dist, linewidth=2.5, col_wrap=3)
    fig7.set_axis_labels("Quarter", "Number")
    fig7.fig.suptitle("Number of users among different age groups, quarterly",  x=0.5, y=1.05)
    fig7.add_legend(bbox_to_anchor=(0.9, 0.9), loc='upper left')
    i, j = 0, 0
    for ax in fig7.axes.flat:
        i+=1
        if i > 3:
            ax.axhline(y=600, linestyle=":")
    for ax in fig7.axes.flat:
        j+=1
        if j <= 3:
            ax.axhline(y=1000, linestyle="dashed")
    st.pyplot(fig7)