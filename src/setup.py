import flet as ft


def before_main_ui(page: ft.Page):
    page.title = "IsaacProj"
    page.decoration = ft.BoxDecoration(
        border=ft.Border.all(3, ft.Colors.SURFACE_CONTAINER_HIGHEST)
    )
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    
    page.window.width = 600
    page.window.height = 360
    page.window.resizable = False
    page.window.maximizable = False
    page.window.title_bar_hidden = True
    
    page.update()