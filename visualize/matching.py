from pathlib import Path

import pandas as pd

CurrentPath = Path(__file__).resolve().parent
BasePath = CurrentPath.parent


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
    result = merged[
        ["ego_id", "u_x", "v", "t", "x1", "x2", "x3", "age_diff", "city_equal", "school_equal", "university_equal"]]
    result.rename(columns={'u_x': 'u'}, inplace=True)
    result.to_csv("full_test.csv", index=False)


if __name__ == "__main__":
    main()
