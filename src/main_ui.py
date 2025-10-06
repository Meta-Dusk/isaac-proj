import asyncio
import flet as ft

from components import (minimize_button, exit_button, theme_button, preset_appbar,
                        preset_input_field, preset_output_container, encrypt_button,
                        decrypt_button)
from encryption import fernet_generate_key, fernet_decrypt, fernet_encrypt
from notifications import simple_notification


async def main_ui(page: ft.Page):
    # == Initial Setup ==
    await page.window.center()
    key = fernet_generate_key()
    print(f"Key has been randomized: {key}")
    
    # == Event Handlers ==
    def theme_swap(_):
        icon_btn: ft.IconButton = theme_btn.content
        if page.theme_mode == ft.ThemeMode.DARK:
            page.theme_mode = ft.ThemeMode.LIGHT
            icon_btn.icon = ft.Icons.LIGHT_MODE
        else:
            page.theme_mode = ft.ThemeMode.DARK
            icon_btn.icon = ft.Icons.DARK_MODE
        theme_btn.update()
    
    def minimize_window(_):
        page.window.minimized = True
        
    def toggle_text_output(e: ft.ControlEventHandler[ft.PopupMenuItem]):
        """`e` only has `name="click"` and `data: bool`"""
        output_popup_item.checked = e.data
        output_popup_item.update()
    
    async def copy_to_clipboard(_):
        switcher: ft.AnimatedSwitcher = output_container.content
        text: ft.Text = switcher.content
        await page.clipboard.set(text.value)
        simple_notification("Content copied to clipboard!", page)
    
    def encrypt_data(_):
        input: ft.TextField = input_field.content
        token = fernet_encrypt(input.value, key)
        switcher: ft.AnimatedSwitcher = output_container.content
        text: ft.Text = switcher.content
        text.value = token
        text.update()
        simple_notification("Data encrypted!", page)
    
    def decrypt_data(_):
        input: ft.TextField = input_field.content
        recovered = fernet_decrypt(input.value, key)
        switcher: ft.AnimatedSwitcher = output_container.content
        text: ft.Text = switcher.content
        text.value = recovered
        text.update()
        simple_notification("Data decrypted!", page)
    
    # == Controls ==
    # App Bar
    exit_btn = exit_button(
        lambda _: asyncio.create_task(
            coro=page.window.close(),
            name="Exit Button -> Closing Window"
        )
    )
    minimize_btn = minimize_button(minimize_window)
    theme_btn = theme_button(theme_swap)
    output_popup_item = ft.PopupMenuItem(
        content="Output Text File", checked=False, icon=ft.Icons.OUTPUT,
        on_click=toggle_text_output
    )
    popup_menu_btn = ft.PopupMenuButton(
        items=[
            ft.PopupMenuItem("Open Output", icon=ft.Icons.FILE_OPEN),
            ft.PopupMenuItem("Open Output Directory", icon=ft.Icons.FOLDER_OPEN),
            output_popup_item
        ], icon_color=ft.Colors.PRIMARY
    )
    appbar = preset_appbar([
        theme_btn, popup_menu_btn,
        ft.Container(padding=8),
        minimize_btn, exit_btn
    ])
    
    # Main Form
    input_field = preset_input_field()
    output_container = preset_output_container(copy_to_clipboard)
    
    encrypt_btn = encrypt_button(encrypt_data)
    decrypt_btn = decrypt_button(decrypt_data)
    
    btn_row = ft.Container(
        content=ft.Row(
            controls=[encrypt_btn, decrypt_btn],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            run_alignment=ft.MainAxisAlignment.CENTER,
            spacing=8, run_spacing=8
        ), bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        padding=16, border_radius=8, alignment=ft.Alignment.CENTER
    )
    
    form_column = ft.Container(
        content=ft.Column(
            controls=[input_field, output_container, btn_row],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            run_alignment=ft.MainAxisAlignment.CENTER,
            tight=True, spacing=8, run_spacing=8,
            scroll=ft.ScrollMode.AUTO
        ), bgcolor=ft.Colors.SURFACE_CONTAINER_LOWEST,
        alignment=ft.Alignment.CENTER, padding=16, border_radius=8
    )
    form = ft.WindowDragArea(content=form_column, expand=True, maximizable=False)
    
    # Page Parameters
    page.add(form)
    page.appbar = appbar
    # page.on_resize = lambda _: print(f"Window resized with dimensions: {page.width} x {page.height}")
    