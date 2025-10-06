import flet as ft

from typing import Optional


# == Presets ==
def simple_icon_button(
    icon: ft.IconDataOrControl,
    icon_color: ft.ColorValue = ft.Colors.PRIMARY,
    on_click: Optional[ft.ControlEventHandler[ft.IconButton]] = None
) -> ft.IconButton:
    return ft.IconButton(
        icon=icon, icon_color=icon_color, on_click=on_click
    )

def important_button(
    content: ft.StrOrControl,
    icon: ft.IconDataOrControl,
    on_click: Optional[ft.ControlEventHandler[ft.Button]] = None
):
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
):
    return ft.PopupMenuItem(
        content=ft.Text(value=text, color=color),
        icon=ft.Icon(icon=icon, color=color),
        on_click=on_click, checked=checked
    )


# == Pre-Assembled Buttons
def minimize_button(
    on_click: Optional[ft.ControlEventHandler[ft.IconButton]] = None
) -> ft.IconButton:
    return simple_icon_button(icon=ft.Icons.MINIMIZE, on_click=on_click)

def theme_button(
    on_click: Optional[ft.ControlEventHandler[ft.IconButton]] = None
) -> ft.AnimatedSwitcher:
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

def exit_button(
    on_click: Optional[ft.ControlEventHandler[ft.IconButton]] = None
) -> ft.IconButton:
    return simple_icon_button(icon=ft.Icons.CLOSE, on_click=on_click)

def preset_appbar(actions: list[ft.Control]) -> ft.AppBar:
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

def preset_input_field() -> ft.Container:
    return ft.Container(
        content=ft.TextField(
            autofocus=True, expand=True,
            hint_text="Input a paragraph, or anything."
        ),
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        border_radius=8, padding=16
    )

def preset_output_container(
    on_click: Optional[ft.ControlEventHandler[ft.Container]] = None
) -> ft.AnimatedSwitcher:
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
        duration=500, reverse_duration=200
    )

def encrypt_button(
    on_click: Optional[ft.ControlEventHandler[ft.Button]] = None
) -> ft.Button:
    return important_button(
        content="Encrypt", icon=ft.Icons.ENHANCED_ENCRYPTION,
        on_click=on_click
    )
    
def decrypt_button(
    on_click: Optional[ft.ControlEventHandler[ft.Button]] = None
) -> ft.Button:
    return important_button(
        content="Decrypt", icon=ft.Icons.NO_ENCRYPTION,
        on_click=on_click
    )