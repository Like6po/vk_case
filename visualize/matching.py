import random
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from tqdm import tqdm

CurrentPath = Path(__file__).resolve().parent
BasePath = CurrentPath.parent


class Config:
    GRAPHIC_LEN: int = 1000


def generate_random_hex():
    r = lambda: random.randint(0, 255)
    return '#%02X%02X%02X' % (r(), r(), r())


def main():
    attr = pd.read_csv(BasePath / "attr.csv")
    attr = attr.drop("sex", axis=1)

    test = pd.read_csv(BasePath / "test.csv")
    merged = pd.merge(test, attr, how="inner", left_on=["u", "ego_id"], right_on=["u", "ego_id"])
    merged = pd.merge(merged, attr, how="inner", left_on=["v", "ego_id"], right_on=["u", "ego_id"])
    merged["age_diff"] = abs(merged["age_x"] - merged["age_y"])
    merged["city_equal"] = merged["city_id_x"] == merged["city_id_y"]
    merged["school_equal"] = merged["school_x"] == merged["school_y"]
    merged["university_equal"] = merged["university_x"] == merged["university_y"]
    result = merged[["ego_id", "u_x", "v", "t", "x1", "x2", "x3", "age_diff", "city_equal", "school_equal", "university_equal"]]
    result.rename(columns={'u_x': 'u'}, inplace=True)
    result.to_csv("full_test.csv", index=False)
    #
    #
    # test["age_diff"] = np.nan
    # test["city_equal"] = np.nan
    # test["school_equal"] = np.nan
    # test["university_equal"] = np.nan
    #
    # for index, row in tqdm(test.iterrows(), total=test.shape[0]):
    #     ego_id = int(row["ego_id"])
    #     u = int(row["u"])
    #     v = int(row["v"])
    #
    #     attr_u = attr[(attr["u"] == u) & (attr["ego_id"] == ego_id)]
    #     attr_v = attr[(attr["u"] == v) & (attr["ego_id"] == ego_id)]
    #     if attr_v.empty or attr_u.empty:
    #         continue
    #
    #     u_age = attr_u.iloc[0]["age"]
    #     v_age = attr_v.iloc[0]["age"]
    #     if u_age != -1 and v_age != -1:
    #         test.at[index, "age_diff"] = abs(u_age - v_age)
    #
    #     u_city = attr_u.iloc[0]["city_id"]
    #     v_city = attr_v.iloc[0]["city_id"]
    #     if u_city != -1 and v_city != -1:
    #         test.at[index, "city_equal"] = u_city == v_city
    #
    #     u_school = attr_u.iloc[0]["school"]
    #     v_school = attr_v.iloc[0]["school"]
    #     if u_school != -1 and v_school != -1:
    #         test.at[index, "school_equal"] = u_school == v_school
    #
    #     u_university = attr_u.iloc[0]["university"]
    #     v_university = attr_v.iloc[0]["university"]
    #     if u_university != -1 and v_university != -1:
    #         test.at[index, "university_equal"] = u_university == v_university
    #
    # print(test.head(10))
    #
    # test.to_csv("full.csv")


if __name__ == "__main__":
    main()
