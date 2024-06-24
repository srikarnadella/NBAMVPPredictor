import pandas as pd


mvpsdf = pd.read_csv("mvps.csv", encoding='utf-8')
playersdf = pd.read_csv("players.csv", encoding='utf-8')
teamsdf = pd.read_csv("teams.csv", encoding='utf-8')

#Other Data such as pts, ast, stl, blk are included in the players dataset
mvpsdf = mvpsdf[["Player", "Year", "Pts Won", "Pts Max", "Share"]]


#Data Cleaning
# Remove uneccessary columns and reformat the text
del playersdf["Rk"]

playersdf["Player"] = playersdf["Player"].str.replace("*","",regex=False)


#Method removes duplicates as in when a player changes teams mid season
def removedupes(df):
    if df.shape[0]==1:
        return df
    else:
        row = df[df["Tm"]=="TOT"]
        row["Tm"] = df.iloc[-1,:]["Tm"]
        return row

playersdf = playersdf.groupby(["Player", "Year"]).apply(removedupes)

playersdf.index = playersdf.index.droplevel()
playersdf.index = playersdf.index.droplevel()

#Combing mvp and players dataset
#outer merge if the data is not found in mvp it can still be added because there are players that arent in the mvp but not vice versa
combineddf = playersdf.merge(mvpsdf, how="outer", on=["Player", "Year"])


#Replace Nan's with Zeros
combineddf[["Pts Won", "Pts Max", "Share"]] = combineddf[["Pts Won", "Pts Max", "Share"]].fillna(0)

#Teamsdf where its all the cols except the ones with the word division 
teamsdf = teamsdf[~teamsdf["W"].str.contains("Division")].copy()

teamsdf["Team"] = teamsdf["Team"].str.replace("*", "", regex=False)


#There are differences in teh team names in the teamcsv and the players csv so we need to map them to be the same
nicknames = {}
with open("nicknames.csv") as f:
    lines = f.readlines()
    for line in lines[1:]:
        abbrev,name = line.replace("\n","").split(",")
        nicknames[abbrev] = name

combineddf["Team"] = combineddf["Tm"].map(nicknames)

cleaneddf = combineddf.merge(teamsdf, how="outer",on=["Team", "Year"])

del cleaneddf["Unnamed: 0_x"]
del cleaneddf["Unnamed: 0_y"]

cleaneddf = cleaneddf.apply(pd.to_numeric, errors='ignore')
cleaneddf["GB"] = pd.to_numeric(cleaneddf["GB"].str.replace("—","0"))


cleaneddf.to_csv("final.csv")
