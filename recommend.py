import pandas as pd

# 读取站点数据
df = pd.read_csv("station.csv")

def get_best_station(df, peak_time=False):
    res = []
    for idx, row in df.iterrows():
        if peak_time:
            # 高峰期：优先排队、距离
            score = (row["排队时长min"] * 0.4 +
                     row["距离km"] * 0.3 +
                     row["电价"] * 0.2 +
                     (2-row["有便利店"]-row["有洗车服务"])*0.1)
        else:
            # 平峰期：优先价格、距离
            score = (row["电价"] * 0.4 +
                     row["距离km"] * 0.3 +
                     row["排队时长min"] * 0.2 +
                     (2-row["有便利店"]-row["有洗车服务"])*0.1)
        res.append(round(score,2))
    df["综合得分"] = res
    # 得分越低越优质
    return df.sort_values("综合得分").head(2)

# 平峰推荐
print("===== 平峰时段最优站点推荐 =====")
print(get_best_station(df,peak_time=False))

# 高峰推荐
print("\n===== 高峰时段最优站点推荐 =====")
print(get_best_station(df,peak_time=True))