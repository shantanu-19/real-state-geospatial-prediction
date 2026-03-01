import xgboost as xgb
from sklearn.model_selection import train_test_split

# Assume 'df' has features: ['sqft', 'dist_to_metro', 'crime_index', 'school_rating']
X = df.drop('price', axis=1)
y = df['price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=1000)
model.fit(X_train, y_train)

# Save the model for the Streamlit app
model.save_model('models/price_model.json')