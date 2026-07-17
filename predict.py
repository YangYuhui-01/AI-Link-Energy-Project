import pandas as pd
from prophet import Prophet

df = pd.read_csv("flow.csv")
df["ds"] = pd.to_datetime(df["ds"])
df = df.rename(columns={"flow":"y"})

# 训练模型
model = Prophet(seasonality_mode="additive")
model.fit(df)

# 预测未来6个时间节点
future = model.make_future_dataframe(periods=6, freq="H")
forecast = model.predict(future)

# 输出关键预测结果
res = forecast[["ds","yhat","yhat_lower","yhat_upper"]].tail(6)
print("===== 未来时段客流预测结果 =====")
print(res)

# 智能定价策略
def get_price_strategy(flow):
    if flow < 30:
        return "低谷时段：电价下调0.03元，发放便利店满20-5优惠券"
    elif 30 <= flow <= 50:
        return "平稳时段：保持原价，常规服务"
    else:
        return "高峰时段：价格不变，开启排队预警，优先疏导车流"

# 获取最新预测客流并输出策略
last_flow = round(res.iloc[-1]["yhat"])
print("\n===== 智能运营策略建议 =====")
print(f"预测客流：{last_flow} 辆")
print(get_price_strategy(last_flow))