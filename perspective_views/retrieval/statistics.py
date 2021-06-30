from perspective_views.plotting.data_frame_creation import create_df_variant


def get_log_statistics(log, file_format, log_information):
    """
    Computes Log Statisitcs from the Variant Dataframe in a log type insensitive Way
    """
    result = {}

    variants, case = create_df_variant(log, file_format, log_information)
    variants["Cases"] = variants["Cases"].apply(len)

    result["variant"] = (
        variants[["Cases", "Name"]]
        .sort_values("Cases", ascending=False)
        .to_dict(orient="records")
    )
    result["Nvariant"] = variants.shape[0]
    result["Nactivities"] = variants.apply(
        lambda x: len(x["variant"]) * x["Cases"], axis=1
    ).sum()

    case["variant"] = case["variant"].apply(len)

    result["case"] = (
        case[["variant", "Name"]]
        .sort_values("variant", ascending=False)
        .to_dict(orient="records")
    )
    result["Nunique_Activities"] = log["concept:name"].unique().size

    result["Ncase"] = case.shape[0]

    start_time = variants["Start"].min()
    end_time = variants["End"].max()

    result["StartTime"] = str(start_time)
    result["EndTime"] = str(end_time)
    result["TotalDuration"] = str(end_time - start_time)

    case_duration = case.apply(lambda x: x["End"] - x["Start"], axis=1)
    result["MedianCaseDuration"] = str(case_duration.median())
    result["MeanCaseDuration"] = str(case_duration.mean())
    result["MinCaseDuration"] = str(case_duration.min())
    result["MaxCaseDuration"] = str(case_duration.max())
    return result


def get_case_ids_by_activity(log, activity, file_format, log_information):
    variants, case = create_df_variant(log, file_format, log_information)
    return case[case["variant"].str.contains(activity, regex=False)]["Name"].tolist()
