def validate_dates(start_date, end_date):
    # TODO 修正する
    # 30日間ではなくて、1ヶ月後の-1日目までか
    # 0320なら0419までがTreu。0420はFalse
    if (end_date - start_date).days >= 30:
        raise ValueError("開始日と終了日の間隔は1ヶ月未満にしてください。")
