import flet as ft
import asyncio


WINDOW_WIDTH = 600
WINDOW_HEIGHT = 360


def before_main_ui(page: ft.Page):
    """Call this function before showing the main UI."""
    page.title = "IsaacProj"
    page.decoration = ft.BoxDecoration(
        border=ft.Border.all(3, ft.Colors.SURFACE_CONTAINER_HIGHEST)
    )
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    
    page.window.width = WINDOW_WIDTH
    page.window.height = WINDOW_HEIGHT
    page.window.resizable = False
    page.window.maximizable = False
    page.window.title_bar_hidden = True
    
async def fix_stretched_window(
    page: ft.Page, *,
    center_page: bool = False
):
    """
    When launching a Flet desktop app, sometimes the window appears to be stretched.
    The fix? Just resize it. So, that's exactly what this does.
    """
    page.window.width = WINDOW_WIDTH * 1.1
    page.window.height = WINDOW_HEIGHT * 1.1
    page.window.update()
    await asyncio.sleep(1)
    page.window.width = WINDOW_WIDTH
    page.window.height = WINDOW_HEIGHT
    page.window.update()
    if center_page:
        await page.window.center()