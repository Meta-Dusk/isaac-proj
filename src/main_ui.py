import asyncio, os, tempfile
import flet as ft

from components import (minimize_button, exit_button, theme_button, preset_appbar,
                        preset_input_field, preset_output_container, encrypt_button,
                        decrypt_button, simple_popup_menu_item)
from encryption import fernet_generate_key, fernet_decrypt, fernet_encrypt
from notifications import simple_notification
from loader import ensure_config_exists, append_to_config_file, CONFIG_FILE, CONFIG_ROOT, _LOG_FILE
from typing import Optional
from pathlib import Path


async def main_ui(page: ft.Page):
    # == Initial Setup ==
    ensured_config: bool = False
    await page.window.center()
    key = fernet_generate_key()
    # print(f"Key has been randomized: {key}")
    
    # Attempt to write to config directory
    try:
        ensure_config_exists()
        ensured_config = True
    except Exception:
        simple_notification(
            content=ft.Text(
                "Insufficient Write Persmissions! Please start the app as Administrator",
                color=ft.Colors.ERROR
            ),
            page=page, duration=5000
        )
    
    # == Helpers ==
    def text_component(string: Optional[str] = None) -> str:
        """
        Lets you edit or get the text component of the `output_container`.
        """
        container: ft.Container = output_container.content
        column: ft.Column = container.content
        text: ft.Text = column.controls[0]
        if string:
            text.value = string
            text.update()
        return text.value
    
    # == Event Handlers ==
    def theme_swap():
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
        value = text_component()
        await page.clipboard.set(value)
        simple_notification("Content copied to clipboard!", page)
    
    def encrypt_data(_):
        text_field: ft.TextField = input_field.content
        value: str = text_field.value
        token = fernet_encrypt(value, key)
        text_component(token)
        simple_notification("Data encrypted!", page)
        if ensured_config and output_popup_item.checked:
            if append_to_config_file(token):
                print("Successfully written to output.")
    
    def decrypt_data(_):
        text_field: ft.TextField = input_field.content
        value: str = text_field.value
        recovered = fernet_decrypt(value, key)
        text_component(recovered)
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
    output_popup_item = simple_popup_menu_item(
        text="Output Text File", icon=ft.Icons.OUTPUT,
        on_click=toggle_text_output, color=ft.Colors.PRIMARY,
        checked=False
    )
    popup_menu_btn = ft.PopupMenuButton(
        items=[
            simple_popup_menu_item(
                text="Open Output", icon=ft.Icons.FILE_OPEN,
                on_click=lambda _: os.startfile(CONFIG_FILE),
                color=ft.Colors.PRIMARY
            ),
            simple_popup_menu_item(
                text="Open Output Directory", icon=ft.Icons.FOLDER_OPEN,
                on_click=lambda _: os.startfile(CONFIG_ROOT),
                color=ft.Colors.PRIMARY
            ),
            output_popup_item,
            simple_popup_menu_item(
                text="Open Log File", icon=ft.Icons.FILE_OPEN,
                on_click=lambda _: os.startfile(_LOG_FILE),
                color=ft.Colors.SECONDARY
            ),
            simple_popup_menu_item(
                text="Open Log Directory", icon=ft.Icons.FOLDER_OPEN,
                on_click=lambda _: os.startfile(Path(tempfile.gettempdir())),
                color=ft.Colors.SECONDARY
            ),
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
            expand=True, spacing=8, run_spacing=8
        ), bgcolor=ft.Colors.SURFACE_CONTAINER_LOWEST,
        alignment=ft.Alignment.CENTER, padding=16, border_radius=8
    )
    form = ft.WindowDragArea(content=form_column, expand=True, maximizable=False)
    
    # Page Parameters
    page.add(form)
    page.appbar = appbar
    # page.on_resize = lambda _: print(f"Window resized with dimensions: {page.width} x {page.height}")
    