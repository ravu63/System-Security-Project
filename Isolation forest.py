import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.ensemble import IsolationForest

data = pd.read_csv('marks.csv')
data.head(10)
sns.boxplot(data.marks)
random_state = np.random.RandomState(42)
model = IsolationForest(n_estimators=100, max_samples='auto', contamination=float(0.2), random_state=random_state)
model.fit(data[['marks']])
print(model.get_params())

data['scores'] = model.decision_function(data[['marks']])
data['anomaly_score'] = model.predict(data[['marks']])
data[data['anomaly_score'] == -1].head()
anomaly_count = len(data['anomaly_score'])

accuracy = 100 * list(data['anomaly_score']).count(-1) / anomaly_count
print("Accuracy of the model:", accuracy)
