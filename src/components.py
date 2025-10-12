import os, tempfile, asyncio
import flet as ft

from typing import Optional
from loader import CONFIG_FILE, CONFIG_ROOT, _LOG_FILE, reset_config_file
from pathlib import Path
from notifications import simple_notification


# == Presets ==
def simple_icon_button(
    icon: ft.IconDataOrControl,
    icon_color: ft.ColorValue = ft.Colors.PRIMARY,
    on_click: Optional[ft.ControlEventHandler[ft.IconButton]] = None
) -> ft.IconButton:
    """Literally just an icon button."""
    return ft.IconButton(
        icon=icon, icon_color=icon_color, on_click=on_click
    )

def important_button(
    content: ft.StrOrControl,
    icon: ft.IconDataOrControl,
    on_click: Optional[ft.ControlEventHandler[ft.Button]] = None
) -> ft.Button:
    """Styling for important buttons."""
    return ft.Button(
        content=content, expand=True,
        color=ft.Colors.PRIMARY,
        bgcolor=ft.Colors.PRIMARY_CONTAINER,
        icon=icon, on_click=on_click
    )

def simple_popup_menu_item(
    text: str,
    color: ft.ColorValue,
    icon: ft.IconData,
    on_click: Optional[ft.ControlEventHandler[ft.PopupMenuItem]] = None,
    checked: Optional[bool] = None
) -> ft.PopupMenuItem:
    """A popup menu item that handles self-toggling if needed."""
    def default_on_click(e: ft.ControlEventHandler[ft.PopupMenuItem]):
        """`e` only has `name="click"` and `data: bool`"""
        popup_menu_item.checked = e.data
        popup_menu_item.update()
    if checked is not None and on_click is None:
        on_click=default_on_click
    popup_menu_item = ft.PopupMenuItem(
        content=ft.Text(value=text, color=color),
        icon=ft.Icon(icon=icon, color=color),
        on_click=on_click, checked=checked
    )
    return popup_menu_item


# == Pre-Assembled Components ==
# Buttons
def minimize_button(page: ft.Page) -> ft.IconButton:
    """Handles the window minimizing function."""
    def on_click(_):
        page.window.minimized = True
    return simple_icon_button(
        icon=ft.Icons.MINIMIZE, on_click=on_click
    )

def theme_button(
    on_click: Optional[ft.ControlEventHandler[ft.IconButton]] = None
) -> ft.AnimatedSwitcher:
    """An animated app theme switcher button."""
    return ft.AnimatedSwitcher(
        content=ft.IconButton(
            icon=ft.Icons.LIGHT_MODE, icon_color=ft.Colors.PRIMARY,
            on_click=on_click
        ),
        transition=ft.AnimatedSwitcherTransition.SCALE,
        switch_in_curve=ft.AnimationCurve.BOUNCE_OUT,
        switch_out_curve=ft.AnimationCurve.BOUNCE_IN,
        duration=500, reverse_duration=200
    )

def exit_button(page: ft.Page) -> ft.IconButton:
    """Handles the app exit function."""
    return simple_icon_button(
        icon=ft.Icons.CLOSE,
        on_click=lambda _: asyncio.create_task(
            coro=page.window.close(),
            name="Exit Button -> Closing Window"
        )
    )

def encrypt_button(
    on_click: Optional[ft.ControlEventHandler[ft.Button]] = None
) -> ft.Button:
    """Use with the encrypt function."""
    return important_button(
        content="Encrypt", icon=ft.Icons.ENHANCED_ENCRYPTION,
        on_click=on_click
    )
    
def decrypt_button(
    on_click: Optional[ft.ControlEventHandler[ft.Button]] = None
) -> ft.Button:
    """Use with the decrypt function."""
    return important_button(
        content="Decrypt", icon=ft.Icons.NO_ENCRYPTION,
        on_click=on_click
    )

def preset_popup_menu_button(
    page: ft.Page, *,
    new_menu_item: list[ft.PopupMenuItem]
) -> ft.PopupMenuButton:
    """An extensive popup menu button, that serves as an extra options menu."""
    async def on_open(e: ft.ControlEvent):
        await asyncio.sleep(0.5)
        popup_menu_btn: ft.PopupMenuButton = e.control
        popup_menu_btn.badge = None
        await asyncio.sleep(0.5)
        popup_menu_btn.update()
    
    def reset_config(_):
        try:
            reset_config_file()
            simple_notification("Successfully cleared output file.", page)
        except Exception as e:
            simple_notification(f"Failed to clear output file: {e}", page)
    
    return ft.PopupMenuButton(
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
            simple_popup_menu_item(
                text="Clear Output Contents", icon=ft.Icons.CLEAR_ALL,
                on_click=reset_config,
                color=ft.Colors.PRIMARY
            ),
            *new_menu_item,
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
        ], icon_color=ft.Colors.PRIMARY, badge=ft.Badge(small_size=10),
        on_open=on_open
    )

# App Bar
def preset_appbar(actions: list[ft.Control]) -> ft.AppBar:
    """A simple predefined appbar."""
    return ft.AppBar(
        title=ft.WindowDragArea(
            content=ft.Text("Encryption", color=ft.Colors.PRIMARY),
            maximizable=False
        ),
        actions=actions,
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        actions_padding=4, title_spacing=4,
        shape=ft.RoundedRectangleBorder(radius=5),
        leading_width=8, leading=ft.Container()
    )

# Input Fields
def preset_input_field() -> ft.Container:
    """A simple wrapped input field."""
    return ft.Container(
        content=ft.TextField(
            autofocus=True, expand=True,
            hint_text="Input a paragraph, or anything."
        ),
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        border_radius=8, padding=16
    )

# Containers
def preset_output_container(
    on_click: Optional[ft.ControlEventHandler[ft.Container]] = None
) -> ft.AnimatedSwitcher:
    """An animated output container (for post data encryption/decryption)."""
    output_column = ft.Column(
        controls=[ft.Text("Output goes here")], expand=True,
        scroll=ft.ScrollMode.AUTO
    )
    return ft.AnimatedSwitcher(
        content=ft.Container(
            content=output_column,
            expand=True, bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
            alignment=ft.Alignment.CENTER, padding=16,
            border_radius=8, on_click=on_click
        ),
        transition=ft.AnimatedSwitcherTransition.SCALE,
        switch_in_curve=ft.AnimationCurve.BOUNCE_OUT,
        switch_out_curve=ft.AnimationCurve.BOUNCE_IN,
        duration=500, reverse_duration=200, expand=True
    )
