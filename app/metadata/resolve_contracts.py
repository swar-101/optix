import pandas as pd

def resolve_contracts(master_df: pd.DataFrame, symbol):
    # print(master_df.columns)
    # print(master_df["expiry"].unique()[:20])
    # print(
    #     master_df[
    #         master_df["name"] == "NIFTY"
    #         ][["name", "expiry", "instrumenttype"]].head(20)
    # )

    expiry = "12MAY2026"

    contracts = master_df[
        (master_df["name"] == symbol) &
        (master_df["exch_seg"] == "NFO") &
        (master_df["instrumenttype"] == "OPTIDX") &
        (master_df["expiry"] == expiry)
        ]

    return contracts