import flet as ft

from components import (minimize_button, exit_button, theme_button, preset_appbar,
                        preset_input_field, preset_output_container, encrypt_button,
                        decrypt_button, simple_popup_menu_item, preset_popup_menu_button)
from encryption import fernet_generate_key, fernet_decrypt, fernet_encrypt
from notifications import simple_notification
from loader import ensure_config_exists, append_to_config_file
from typing import Optional
from utilities import theme_swap, copy_to_clipboard
from layouts import default_column, default_container, default_drag_area, default_row


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
        output_popup_item.disabled = True
    
    # == Helpers ==
    def text_component(value: Optional[str] = None) -> str:
        """
        Lets you edit or get the text component of the `output_container`.
        """
        container: ft.Container = output_container.content
        column: ft.Column = container.content
        text: ft.Text = column.controls[0]
        if value:
            text.value = value
            text.update()
        return text.value
    
    def get_field_value() -> str:
        text_field: ft.TextField = input_field.content
        value: str = text_field.value
        return value
    
    # == Event Handlers ==
    async def copy_key(_):
        await copy_to_clipboard(key, page)
    
    async def output_clicked(_):
        value = text_component()
        await copy_to_clipboard(value, page)
    
    def encrypt_data(_):
        value = get_field_value()
        token = fernet_encrypt(value, key)
        text_component(token)
        simple_notification("Data encrypted!", page)
        if ensured_config and output_popup_item.checked:
            append_to_config_file(token)
    
    def decrypt_data(_):
        value = get_field_value()
        recovered = fernet_decrypt(value, key)
        text_component(recovered)
        simple_notification("Data decrypted!", page)
    
    # == Controls ==
    # App Bar
    exit_btn = exit_button(page)
    minimize_btn = minimize_button(page)
    theme_btn = theme_button(lambda _: theme_swap(theme_btn, page))
    output_popup_item = simple_popup_menu_item(
        text="Output Text File", icon=ft.Icons.OUTPUT,
        color=ft.Colors.PRIMARY, checked=False
    )
    popup_menu_btn = preset_popup_menu_button([
        output_popup_item,
        simple_popup_menu_item(
            text="Copy Key to Clipboard", icon=ft.Icons.COPY,
            color=ft.Colors.TERTIARY, on_click=copy_key
        )
    ])
    appbar = preset_appbar([
        theme_btn, popup_menu_btn,
        ft.Container(padding=8),
        minimize_btn, exit_btn
    ])
    
    # Main Form
    input_field = preset_input_field()
    output_container = preset_output_container(output_clicked)
    
    encrypt_btn = encrypt_button(encrypt_data)
    decrypt_btn = decrypt_button(decrypt_data)
    
    btn_row = default_container(
        content=default_row([encrypt_btn, decrypt_btn]),
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW
    )
    
    form_column = default_container(
        default_column([input_field, output_container, btn_row])
    )
    form = default_drag_area(form_column)
    
    # Page Parameters
    page.add(form)
    page.appbar = appbar
    # page.on_resize = lambda _: print(f"Window resized with dimensions: {page.width} x {page.height}")
    