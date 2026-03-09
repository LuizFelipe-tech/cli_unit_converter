import questionary

from config import enums


def main_menu():
    category_display_names: dict[enums.Category, str] = {}
    for category in enums.Category:
        category_display_names[category] = category.display_name
    option = questionary.select(
        "Which category do you want to convert?", list(category_display_names.values())
        ).ask()
    key_category = next(k for k, v in category_display_names.items() if v == option)
    return key_category

def process_menu_selection(option_selected: str) -> None:
    """Processes the user's menu selection and routes to the appropriate handler."""
    units_keys = enums.UnitConverter.get_keys_by_category(option_selected)
    return get_units(units_keys)


def get_units(keys):
    units_list = []
    for key in keys:
        units_list.append(key)
    while True:
        unit_to_convert = questionary.select('Select the unit to be converted', units_list).ask()
        unit_convert = questionary.select('Select the unit to convert', units_list).ask()
        if unit_to_convert is unit_convert:
            print('Suas opções não podem ser idênticas.')
            continue
        return unit_to_convert, unit_convert
