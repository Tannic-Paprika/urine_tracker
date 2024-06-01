import cv2
import numpy as np
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.conf import settings
import base64

def identify_color_blocks(image_path, lower_hsv, upper_hsv):
    image = cv2.imread(image_path)
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_hsv = np.array(lower_hsv)
    upper_hsv = np.array(upper_hsv)
    mask = cv2.inRange(image_hsv, lower_hsv, upper_hsv)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    min_contour_area = 100
    contours = [c for c in contours if cv2.contourArea(c) > min_contour_area]
    contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[1])
    output_image = cv2.cvtColor(image_hsv, cv2.COLOR_HSV2RGB)
    rgb_values = []
    for i, c in enumerate(contours[:10]):
        x, y, w, h = cv2.boundingRect(c)
        if 0.8 < w / h < 1.2:
            block = output_image[y:y+h, x:x+w]
            mean_rgb = block.mean(axis=0).mean(axis=0)
            rgb_values.append({
                'block': i+1,
                'R': int(mean_rgb[0]),
                'G': int(mean_rgb[1]),
                'B': int(mean_rgb[2])
            })
            cv2.rectangle(output_image, (x, y), (x+w, y+h), (0, 255, 0), 2)
    _, encoded_image = cv2.imencode('.png', cv2.cvtColor(output_image, cv2.COLOR_RGB2BGR))
    image_data = base64.b64encode(encoded_image).decode('utf-8')
    return rgb_values, image_data

def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        image_url = fs.url(filename)
        return redirect('process_image', image_url=image_url)
    return render(request, 'upload.html')

def process_image(request, image_url):
    if request.method == 'POST':
        lower_hsv = [
            int(request.POST.get('h_min')),
            int(request.POST.get('s_min')),
            int(request.POST.get('v_min'))
        ]
        upper_hsv = [
            int(request.POST.get('h_max')),
            int(request.POST.get('s_max')),
            int(request.POST.get('v_max'))
        ]
        image_path = settings.MEDIA_ROOT + '/' + image_url.split('/')[-1]
        rgb_values, image_data = identify_color_blocks(image_path, lower_hsv, upper_hsv)
        return JsonResponse({'rgb_values': rgb_values, 'image_data': image_data})
    
    lower_hsv = [10, 50, 50]
    upper_hsv = [30, 255, 255]
    context = {
        'image_url': image_url,
        'lower_hsv': lower_hsv,
        'upper_hsv': upper_hsv
    }
    return render(request, 'process_image.html', context)
