import flet as ft
from datetime import datetime
from notifications import simple_notification

# Date Stuff
def get_date() -> str:
    """Returns a formatted `date` + `time` string."""
    now = datetime.now()
    formatted = now.strftime("%Y-%m-%d %H:%M:%S")
    return formatted

# Theme Stuff
def theme_swap(theme_btn: ft.AnimatedSwitcher, page: ft.Page):
    """Swaps the `page` theme."""
    icon_btn: ft.IconButton = theme_btn.content
    if page.theme_mode == ft.ThemeMode.DARK:
        page.theme_mode = ft.ThemeMode.LIGHT
        icon_btn.icon = ft.Icons.LIGHT_MODE
    else:
        page.theme_mode = ft.ThemeMode.DARK
        icon_btn.icon = ft.Icons.DARK_MODE
    theme_btn.update()
    
# Clipboard Stuff
async def copy_to_clipboard(value: str, page: ft.Page):
    await page.clipboard.set(value)
    simple_notification("Content copied to clipboard!", page)