import pandas as pd
import checkers as chks


class PdChecker:

    def __init__(self,
                 pd_df,
                 clean=True) -> None:
        if clean:
            # Trim DataFrame and replace empty strings with NA
            df_obj = pd_df.select_dtypes(['object'])
            pd_df[df_obj.columns] = df_obj.apply(
                lambda x: x.str.strip().replace("", None))
        self.pd_df = pd_df

    def _rule_switcher(self, checker_string):
        switcher = {
            "email": chks.Checker().email,
            "full_name": chks.Checker().full_name,
            "date": chks.Checker().date,
            "number": chks.Checker().number,
        }
        return switcher.get(checker_string, None)

    def pd_sniffer(self, checker_string: str):
        rule = self._rule_switcher(checker_string)
        rows = self.pd_df.shape[0]
        columns = list(self.pd_df.select_dtypes(include=['object']))

        rule_result = [[], []]
        for column in columns:
            perc = sum(self.pd_df[column].apply(rule))/rows
            if perc == 0:
                continue
            rule_result[0].append(column)
            rule_result[1].append(perc)
        df_rr = pd.DataFrame(rule_result).transpose()
        df_rr.columns = ["column", "perc"]
        return df_rr.sort_values(
            by=df_rr.columns[1], ascending=False).reset_index(drop=True)

    def get_suspect_values(self,
                           column: str,
                           checker_string: str,
                           inverse=False):
        rule = self._rule_switcher(checker_string)
        if inverse:
            return self.pd_df[self.pd_df[column].apply(rule)]
        return self.pd_df[~self.pd_df[column].apply(rule)]
