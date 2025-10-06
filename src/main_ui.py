import asyncio
import flet as ft


async def main_ui(page: ft.Page):
    # == Initial Setup ==
    await page.window.center()
    
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
    
    # == Controls ==
    # App Bar
    exit_btn = ft.IconButton(
        icon=ft.Icons.CLOSE, icon_color=ft.Colors.PRIMARY,
        on_click=lambda _: asyncio.create_task(
            coro=page.window.close(),
            name="Exit Button -> Closing Window"
        )
    )
    minimize_btn = ft.IconButton(
        icon=ft.Icons.MINIMIZE, icon_color=ft.Colors.PRIMARY,
        on_click=minimize_window
    )
    theme_btn = ft.AnimatedSwitcher(
        content=ft.IconButton(
            icon=ft.Icons.LIGHT_MODE, icon_color=ft.Colors.PRIMARY,
            on_click=theme_swap
        ),
        transition=ft.AnimatedSwitcherTransition.SCALE,
        switch_in_curve=ft.AnimationCurve.BOUNCE_OUT,
        switch_out_curve=ft.AnimationCurve.BOUNCE_IN,
        duration=500, reverse_duration=200
    )
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
    appbar = ft.AppBar(
        title=ft.WindowDragArea(
            content=ft.Text("Encryption", color=ft.Colors.PRIMARY),
            maximizable=False
        ),
        actions=[
            theme_btn, popup_menu_btn,
            ft.Container(padding=8),
            minimize_btn, exit_btn
        ],
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        actions_padding=4, title_spacing=4,
        shape=ft.RoundedRectangleBorder(radius=5),
        leading_width=8, leading=ft.Container()
    )
    
    # Main Form
    input_field = ft.Container(
        content=ft.TextField(
            autofocus=True, expand=True,
            hint_text="Input a paragraph, or anything."
        ),
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        border_radius=8, expand=True, padding=16
    )
    output_container = ft.Container(
        content=ft.Text("Output goes here"),
        expand=True, bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
        alignment=ft.Alignment.CENTER, padding=16,
        border_radius=8
    )
    input_field_column = ft.Column(
        controls=[input_field, output_container]
    )
    
    encrypt_btn = ft.Button(
        "Encrypt", expand=True, color=ft.Colors.PRIMARY,
        bgcolor=ft.Colors.PRIMARY_CONTAINER,
        icon=ft.Icons.ENHANCED_ENCRYPTION
    )
    decrypt_btn = ft.Button(
        "Decrypt", expand=True, color=ft.Colors.PRIMARY,
        bgcolor=ft.Colors.PRIMARY_CONTAINER,
        icon=ft.Icons.NO_ENCRYPTION
    )
    
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
            controls=[input_field_column, btn_row],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            run_alignment=ft.MainAxisAlignment.CENTER,
            tight=True, spacing=8, run_spacing=8
        ), bgcolor=ft.Colors.SURFACE_CONTAINER_LOWEST,
        alignment=ft.Alignment.CENTER, padding=16, border_radius=8
    )
    form = ft.WindowDragArea(content=form_column, expand=True, maximizable=False)
    
    # Page Parameters
    page.add(form)
    page.appbar = appbar
    # page.on_resize = lambda _: print(f"Window resized with dimensions: {page.width} x {page.height}")
    