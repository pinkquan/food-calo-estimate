import pandas as pd
from sklearn.linear_model import LinearRegression

excel_file = '../metadata/density.xls'
xls = pd.read_excel(excel_file, sheet_name=None)


def train_model_per_sheet():
    regression_models = {}
    for sheet_name, df in xls.items():
        if 'volume(cm^3)' not in df.columns or 'weight(g)' not in df.columns:
            print(f"skip sheet {sheet_name}: missing required column.")
            continue
        df['weight(g)'] = df['weight(g)'].astype(str).str.replace(',', '.').astype(float)
        X = df[['volume(cm^3)']].values
        y = df['weight(g)'].values

        model = LinearRegression()
        model.fit(X, y)

        a = model.coef_[0]
        b = model.intercept_

        regression_models[sheet_name] = (round(a, 6), round(b, 6))
        print(f"{sheet_name}: weight = {a:.4f} * volume + {b:.4f}")
    return regression_models


def write_weights_to_file(regression_models):
    with open('../food-calo-estimate-system/models/regression_models.py', 'w') as f:
        f.write("# Hệ số hồi quy volume → weight theo từng loại thực phẩm\n")
        f.write("regression_models = {\n")
        for food_type, (a, b) in regression_models.items():
            f.write(f"    '{food_type}': ({a}, {b}),\n")
        f.write("}\n")


if __name__ == "__main__":
    regression_models = train_model_per_sheet()
    write_weights_to_file()
