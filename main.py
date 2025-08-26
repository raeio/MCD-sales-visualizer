import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st


fileLoc=st.sidebar.file_uploader("Upload your Excel file", type=["xlsx", "xls"])
reqDF=[]   
storeId=st.sidebar.number_input("Store Code",step=1)
avgDays=st.sidebar.slider("Average Days",1,31)
trendDays=st.sidebar.slider("Trend Days",1,31)
st.sidebar.title("Last year sales")
lyData=st.sidebar.number_input("Total Sales",step=1)
lyInStoreSales=st.sidebar.number_input("Instore sales",step=1)
lyMDSsales=lyData-lyInStoreSales
st.sidebar.title("Last GC")
totalGcly=st.sidebar.number_input("GC",step=1)
lyInstoreGC=st.sidebar.number_input("Instore GC",step=1)
lyMDS=totalGcly-lyInstoreGC
st.sidebar.title("Plan")
planTotalSales=st.sidebar.number_input("Total Sales plan",step=1)
ISplan=st.sidebar.number_input("Instore Sale",step=1)
MDSplan=planTotalSales-ISplan
planTGC=st.sidebar.number_input("Total GC plan",step=1)
planIsGC=st.sidebar.number_input("Instore GC plan",step=1)
planMdsGC=planTGC-planIsGC

if st.sidebar.button("Get"):
    tabsNames=pd.ExcelFile(fileLoc).sheet_names
    for i in range(len(tabsNames)):
        data=pd.read_excel(fileLoc,skiprows=3,sheet_name=tabsNames[i])
        colNames=data.columns.tolist()
        reqCol=[]
        for j in colNames:
            if j=="Store code" or j=="Store Code":
                reqCol.append(j)
            if j=="Store Name" or j=="Store name":
                reqCol.append(j)
            if j=="total" or j=="Total":
                reqCol.append(j)

        result=data[data["Store code"]==storeId]
        result=result[reqCol]
        result["Tab name"]=tabsNames[i]
        reqDF.append(result)


    finialDF=pd.concat(reqDF)
    # print(finialDF)
    totalSalesDataDF=pd.DataFrame({
        "CY":finialDF[finialDF["Tab name"]=="SOUTH Sales"]["Total"],
        "LY":lyData,
        "Comps":(((((finialDF[finialDF["Tab name"]=="SOUTH Sales"]["Total"]/avgDays)*trendDays)-lyData)*100)/lyData),
        "Avg":(finialDF[finialDF["Tab name"]=="SOUTH Sales"]["Total"]/avgDays),
        "Trending":((finialDF[finialDF["Tab name"]=="SOUTH Sales"]["Total"]/avgDays)*trendDays)
    })


    inStoreSalesDF=pd.DataFrame({
        "CY":finialDF[finialDF["Tab name"]=="Instore SOUTH Sales"]["Total"],
        "LY":lyInStoreSales,
        "Comps":(((((finialDF[finialDF["Tab name"]=="Instore SOUTH Sales"]["Total"]/avgDays)*trendDays)-lyInStoreSales)*100)/lyInStoreSales),
        "Avg":(finialDF[finialDF["Tab name"]=="Instore SOUTH Sales"]["Total"]/avgDays),
        "Trending":((finialDF[finialDF["Tab name"]=="Instore SOUTH Sales"]["Total"]/avgDays)*trendDays)
    })


    MDSsales=pd.DataFrame({
        "CY":finialDF[finialDF["Tab name"]=="MDS SOUTH Sales"]["Total"],
        "LY":lyMDSsales,
        "Comps":(((((finialDF[finialDF["Tab name"]=="MDS SOUTH Sales"]["Total"]/avgDays)*trendDays)-lyMDSsales)*100)/lyMDSsales),
        "Avg":(finialDF[finialDF["Tab name"]=="MDS SOUTH Sales"]["Total"]/avgDays),
        "Trending":((finialDF[finialDF["Tab name"]=="MDS SOUTH Sales"]["Total"]/avgDays)*trendDays)
    })


    totalGC=pd.DataFrame({
        "CY":finialDF[finialDF["Tab name"]=="SOUTH GC"]["Total"],
        "LY":totalGcly,
        "Comps":(((((finialDF[finialDF["Tab name"]=="SOUTH GC"]["Total"]/avgDays)*trendDays)-totalGcly)*100)/totalGcly),
        "Avg":(finialDF[finialDF["Tab name"]=="SOUTH GC"]["Total"]/avgDays),
        "Trending":((finialDF[finialDF["Tab name"]=="SOUTH GC"]["Total"]/avgDays)*trendDays)
    })


    instoreGC=pd.DataFrame({
        "CY":finialDF[finialDF["Tab name"]=="Instore SOUTH GC"]["Total"],
        "LY":lyInstoreGC,
        "Comps":(((((finialDF[finialDF["Tab name"]=="Instore SOUTH GC"]["Total"]/avgDays)*trendDays)-lyInstoreGC)*100)/lyInstoreGC),
        "Avg":(finialDF[finialDF["Tab name"]=="Instore SOUTH GC"]["Total"]/avgDays),
        "Trending":((finialDF[finialDF["Tab name"]=="Instore SOUTH GC"]["Total"]/avgDays)*trendDays)
    })

    
    MDSgc=pd.DataFrame({
        "CY":finialDF[finialDF["Tab name"]=="Mds SOUTH GC"]["Total"],
        "LY":lyMDS,
        "Comps":(((((finialDF[finialDF["Tab name"]=="Mds SOUTH GC"]["Total"]/avgDays)*trendDays)-lyMDS)*100)/lyMDS),
        "Avg":(finialDF[finialDF["Tab name"]=="Mds SOUTH GC"]["Total"]/avgDays),
        "Trending":((finialDF[finialDF["Tab name"]=="Mds SOUTH GC"]["Total"]/avgDays)*trendDays)
    })


    
    TSfinDF=pd.DataFrame({
        "Plan":planTotalSales,
        "Actual":totalSalesDataDF["Trending"],
        "ACH%":(totalSalesDataDF["Trending"]/planTotalSales)*100,
        "Comps":totalSalesDataDF["Comps"]
    })
    ISfinDF=pd.DataFrame({
        "Plan":ISplan,
        "Actual":inStoreSalesDF["Trending"],
        "ACH%":(inStoreSalesDF["Trending"]/ISplan)*100,
        "Comps":inStoreSalesDF["Comps"]
    })
    MDSfinDF=pd.DataFrame({
        "Plan":MDSplan,
        "Actual":MDSsales["Trending"],
        "ACH%":(MDSsales["Trending"]/MDSplan)*100,
        "Comps":MDSsales["Comps"]
    })
    TGCfinDF=pd.DataFrame({
        "Plan":planTGC,
        "Actual":totalGC["Trending"],
        "ACH%":(totalGC["Trending"]/planTGC)*100,
        "Comps":totalGC["Comps"]
    })
    IsGCfinDF=pd.DataFrame({
        "Plan":planIsGC,
        "Actual":instoreGC["Trending"],
        "ACH%":(instoreGC["Trending"]/planIsGC)*100,
        "Comps":instoreGC["Comps"]
    })
    MDSGCfinDF=pd.DataFrame({
        "Plan":planMdsGC,
        "Actual":MDSgc["Trending"],
        "ACH%":(MDSgc["Trending"]/planMdsGC)*100,
        "Comps":MDSgc["Comps"]
    })


    st.title("Total Sale")
    st.dataframe(TSfinDF,use_container_width=True)
    categories = ['Plan', 'Actual']
    values = [int(TSfinDF["Plan"]),int(TSfinDF["Actual"])]
    colors = ['blue', 'red']
    fig1, ax1 = plt.subplots()
    plt.bar(categories, values, color=colors)
    plt.title("Total Sales", fontsize=14)
    plt.ylabel("Sales", fontsize=12)
    st.pyplot(fig1)

    st.title("Instore Sale")
    st.dataframe(ISfinDF,use_container_width=True)
    categories = ['Plan', 'Actual']
    values = [int(ISfinDF["Plan"]),int(ISfinDF["Actual"])]
    colors = ['blue', 'red']
    fig2, ax2 = plt.subplots()
    plt.bar(categories, values, color=colors)
    plt.title("Total Sales", fontsize=14)
    plt.ylabel("Sales", fontsize=12)
    st.pyplot(fig2)

    st.title("MDS")
    st.dataframe(MDSfinDF,use_container_width=True)
    categories = ['Plan', 'Actual']
    values = [int(MDSfinDF["Plan"]),int(MDSfinDF["Actual"])]
    colors = ['blue', 'red']
    fig3, ax3 = plt.subplots()
    plt.bar(categories, values, color=colors)
    plt.title("Total Sales", fontsize=14)
    plt.ylabel("Sales", fontsize=12)
    st.pyplot(fig3)

    st.title("TOtal GC")
    st.dataframe(TGCfinDF,use_container_width=True)
    categories = ['Plan', 'Actual']
    values = [int(TGCfinDF["Plan"]),int(TGCfinDF["Actual"])]
    colors = ['blue', 'red']
    fig4, ax4 = plt.subplots()
    plt.bar(categories, values, color=colors)
    plt.title("Total Sales", fontsize=14)
    plt.ylabel("Sales", fontsize=12)
    st.pyplot(fig4)

    st.title("Instore GC")
    st.dataframe(IsGCfinDF,use_container_width=True)
    categories = ['Plan', 'Actual']
    values = [int(IsGCfinDF["Plan"]),int(IsGCfinDF["Actual"])]
    colors = ['blue', 'red']
    fig5, ax5 = plt.subplots()
    plt.bar(categories, values, color=colors)
    plt.title("Total Sales", fontsize=14)
    plt.ylabel("Sales", fontsize=12)
    st.pyplot(fig5)

    st.title("MDS GC")
    st.dataframe(MDSGCfinDF,use_container_width=True)
    categories = ['Plan', 'Actual']
    values = [int(MDSGCfinDF["Plan"]),int(MDSGCfinDF["Actual"])]
    colors = ['blue', 'red']
    fig6, ax6 = plt.subplots()
    plt.bar(categories, values, color=colors)
    plt.title("Total Sales", fontsize=14)
    plt.ylabel("Sales", fontsize=12)
    st.pyplot(fig6)
