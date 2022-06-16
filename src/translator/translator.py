class Translator:

    @staticmethod
    def translate_seconds(seconds_subexpression: str) -> str:
        if Translator.__is_star_expression(seconds_subexpression):
            return "every second"
        if Translator.__has_slash_in_expression(seconds_subexpression):
            return Translator.__get_slash_translation(seconds_subexpression)
        if Translator.__is_list_expression(seconds_subexpression):
            return Translator.__get_list_translation(seconds_subexpression)
        return Translator.__get_range_translation(seconds_subexpression)

    @staticmethod
    def __is_star_expression(subexpression: str) -> bool:
        return "*" == subexpression

    @staticmethod
    def __is_slashed_star_expression(subexpression: str) -> bool:
        return "*/" in subexpression or "0/" in subexpression

    @staticmethod
    def __has_slash_in_expression(subexpression: str) -> bool:
        return "/" in subexpression

    @staticmethod
    def __is_list_expression(subexpression: str) -> bool:
        return "," in subexpression

    @staticmethod
    def __is_range_expression(subexpression: str) -> bool:
        return "-" in subexpression

    @staticmethod
    def __get_element_description(element: str) -> str:
        if Translator.__is_range_expression(element):
            arguments = element.rsplit("-")
            return f"{arguments[0]} through {arguments[1]}"
        return element

    @staticmethod
    def __get_list_translation(subexpression: str) -> str:
        list_values = subexpression.rsplit(",")
        translation_msg = "at "
        for value in list_values:
            element_desc = Translator.__get_element_description(value)
            if list_values[-1] == value:
                translation_msg += f"and {element_desc} seconds past the minute"
                break
            translation_msg += f"{element_desc}, "
        return translation_msg

    @staticmethod
    def __get_slash_translation(subexpression: str) -> str:
        arguments = subexpression.rsplit("/")
        if Translator.__is_slashed_star_expression(subexpression):
            return f"every {arguments[1]} seconds"
        return f"every {arguments[1]} seconds, starting at second {arguments[0]} past the minute"

    @staticmethod
    def __get_range_translation(subexpression: str) -> str:
        return f"seconds {Translator.__get_element_description(subexpression)} past the minute"

