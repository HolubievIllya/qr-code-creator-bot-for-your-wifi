import wifi_qrcode_generator.generator


def create_qr_code(name: str, password: str, file_name: str):
    qr_code = wifi_qrcode_generator.generator.wifi_qrcode(
        ssid=name, hidden=False, authentication_type="WPA", password=password
    )
    qr_code.make_image().save(f"{file_name}.png")