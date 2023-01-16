import regex


class Checker:
    PATTERNS = {
        "email":
            r"^\S+@\S+\.\S+$",
        "full_name": r"([a-zA-Z]+\s+){2,}",
        "date":
            r"^(1[0-2]|0?[1-9])/(3[01]|[12][0-9]|0?[1-9])/"
            r"(?:[0-9]{2})?[0-9]{2}$|"
            r"^(3[01]|[12][0-9]|0?[1-9])/(1[0-2]|0?[1-9])/"
            r"(?:[0-9]{2})?[0-9]{2}$|"
            r"^(?:[0-9]{2})?[0-9]{2}-(1[0-2]|0?[1-9])-"
            r"(3[01]|[12][0-9]|0?[1-9])$",
        "number":
            r"^(\w?\$)?\s*\d{1,3}(,\d{3})*(\.\d+)?$|"
            r"^(\w?\$)?\s*\d+$|"
            r"^(\w?\$)?\s*\d{1,3}(\.\d{3})*(\,\d+)?$|"
            r"^(\w?\$)?\s*\d+(\,\d+)?$"
    }

    def _compile_pattern(self, item):
        return regex.compile(self.PATTERNS[item])

    def email(self, email_string: str):
        email_pattern = self._compile_pattern("email")
        if email_pattern.match(str(email_string)):
            return True
        return False

    def date(self, date_string: str):
        date_pattern = self._compile_pattern("date")
        if date_pattern.match(str(date_string)):
            return True
        return False

    def full_name(self, fname_string: str):
        fname_pattern = self._compile_pattern("full_name")
        if fname_pattern.match(str(fname_string) + " "):
            return True
        return False

    def number(self, number_string: str):
        if isinstance(number_string, float):  # Nan
            return True
        if number_string.isdigit():
            return True
        try:
            float(number_string)
            return True
        except ValueError:
            pass
        if number_string.replace(",", "").replace(".", "").isdigit():
            number_pattern = self._compile_pattern("number")
            if number_pattern.match(str(number_string)):
                return True
            return False
        return False
