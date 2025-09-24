import qrcode
from qrcode.constants import ERROR_CORRECT_M
from io import BytesIO
import base64
from django.http import HttpResponse
from django.shortcuts import render

# Store the last generated QR in memory for download
generated_qr = None


def home(request):
    global generated_qr
    qr_data_uri = None
    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        if text:
            qr = qrcode.QRCode(
                version=None,
                error_correction=ERROR_CORRECT_M,
                box_size=10,
                border=4,
            )
            qr.add_data(text)
            qr.make(fit=True)
            img = qr.make_image(fill_color='black', back_color='white')

            buffer = BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)
            img_bytes = buffer.getvalue()
            generated_qr = img_bytes  # store for download
            img_b64 = base64.b64encode(img_bytes).decode('utf-8')
            qr_data_uri = 'data:image/png;base64,' + img_b64

    return render(request, 'generator/home.html', {'qr_data_uri': qr_data_uri})


def download_qr(request):
    global generated_qr
    if generated_qr:
        response = HttpResponse(generated_qr, content_type='image/png')
        response['Content-Disposition'] = 'attachment; filename="qrcode.png"'
        return response
    return HttpResponse("No QR code generated yet.")