import flet as ft
from vigener import decrypt_message, encrypt_message

def main(page: ft.Page):
    page.title = 'Шифр Виженера'
    page.window_width = 500
    page.window_height = 500
    page.window_resizable = False
    label = ft.Text(
        'Шифр Виженера',
        text_align='CENTER', width=500,
        size=25,
    )

    def clear(e):
        e.control.error_text = ''
        page.update()

    def check_lang():
        ru_alpha = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"



    def decrypt(e):
        if len(message_field.value) > 200 and key_field.value == '':
            key, decrypted = decrypt_message(message_field.value)
            key_field.value = key
            message_field.value = decrypted
        elif len(message_field.value) >= 1 and key_field.value != '':
            key, decrypted = decrypt_message(message_field.value, key_field.value)
            key_field.value = key
            message_field.value = decrypted
        else:
            message_field.error_text = "Сообщение должно быть длиннее для расшифровки"
        page.update()

    def encrypt(e):
        if len(key_field.value) > 1 and len(message_field.value) > 1:
            encrypted = encrypt_message(message_field.value, key_field.value)
            message_field.value = encrypted
        elif len(key_field.value) <= 1:
            key_field.error_text = 'Ключ должен быть больше 1 символа'
        page.update()

    key_label = ft.Text('Ключ', text_align='CENTER', width=90)
    key_field = ft.TextField(width=350, on_change=clear)

    message_label = ft.Text('Сообщение', text_align='CENTER', width=90, )
    message_field = ft.TextField(height=250, width=350, multiline=True, min_lines=10, on_change=clear)

    page.add(
        label,
        ft.Row([
            key_label,
            key_field
        ]),
        ft.Row([
            message_label, message_field,
        ], width=500),
    )
    page.add(
        ft.Row([
            ft.ElevatedButton('Зашифровать', on_click=encrypt),
            ft.ElevatedButton('Дешифровать', on_click=decrypt)
        ], alignment=ft.MainAxisAlignment.CENTER),
    )


ft.app(main)
