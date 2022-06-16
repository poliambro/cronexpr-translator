from src.translator.enums import CronField, AllowedCharacters


class Translator:

    @staticmethod
    def translate_seconds_and_minutes(subexpression: str, field_type: CronField) -> str:
        field_name = str(field_type.name).lower()
        past_time = f" past the {str(CronField(field_type.value + 1).name).lower()}"
        if Translator.__is_star_expression(subexpression):
            return f"every {field_name}"
        if Translator.__has_slash_in_expression(subexpression):
            return Translator.__get_slash_translation(subexpression, field_name, past_time)
        if Translator.__is_list_expression(subexpression):
            return Translator.__get_list_translation(subexpression, field_name, past_time)
        return Translator.__get_range_translation(subexpression, field_name, past_time)

    @staticmethod
    def __is_star_expression(subexpression: str) -> bool:
        return AllowedCharacters.STAR.value == subexpression

    @staticmethod
    def __is_slashed_star_expression(subexpression: str) -> bool:
        return f"{AllowedCharacters.STAR.value}{AllowedCharacters.SLASH.value}" in subexpression or \
               f"0{AllowedCharacters.SLASH.value}" in subexpression

    @staticmethod
    def __has_slash_in_expression(subexpression: str) -> bool:
        return AllowedCharacters.SLASH.value in subexpression

    @staticmethod
    def __is_list_expression(subexpression: str) -> bool:
        return AllowedCharacters.LIST.value in subexpression

    @staticmethod
    def __is_range_expression(subexpression: str) -> bool:
        return AllowedCharacters.RANGE.value in subexpression

    @staticmethod
    def __get_element_description(element: str) -> str:
        if Translator.__is_range_expression(element):
            arguments = element.rsplit(AllowedCharacters.RANGE.value)
            return f"{arguments[0]} through {arguments[1]}"
        return element

    @staticmethod
    def __get_list_translation(subexpression: str, field_name: str, past_time: str = "") -> str:
        list_values = subexpression.rsplit(AllowedCharacters.LIST.value)
        translation_msg = "at "
        for value in list_values:
            element_desc = Translator.__get_element_description(value)
            if list_values[-1] == value:
                translation_msg += f"and {element_desc} {field_name}s{past_time}"
                break
            translation_msg += f"{element_desc}, "
        return translation_msg

    @staticmethod
    def __get_slash_translation(subexpression: str, field_name: str, past_time: str = "") -> str:
        arguments = subexpression.rsplit(AllowedCharacters.SLASH.value)
        slash_expr = f"every {arguments[1]} {field_name}s"
        if Translator.__is_slashed_star_expression(subexpression):
            return slash_expr
        return f"{slash_expr}, starting at {field_name} {arguments[0]}{past_time}"

    @staticmethod
    def __get_range_translation(subexpression: str, field_name: str, past_time: str = "") -> str:
        return f"{field_name}s {Translator.__get_element_description(subexpression)}{past_time}"
