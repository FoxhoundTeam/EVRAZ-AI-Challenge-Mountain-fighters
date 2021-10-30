from src.base.models import Camera, Frame, Violation, WorkShop
from datetime import timedelta
from django.core.files import File

CAMERAS = {
    'CAM 1': ['am3_1', 'am3_5', 'am3_9', 'oz'],
    'CAM 2': ['am3_3'],
    'CAM 3': ['am3_4', 'am3_7', 'oz7'],
    'CAM 4': ['am3_6'],
}

def fill_db(dttm_start, folder_path):
    ws, _ = WorkShop.objects.get_or_create(name='Рабочий цех № 1', code='ddf889-cade-222-cffaaad26099')

    with open('etc/files.txt') as f:
        files = f.read().split('\n')
    
    for cam, codes in CAMERAS.items():
        cam, _ = Camera.objects.update_or_create(
            name=cam,
            work_shop=ws,
            defaults={
                'code': ''.join(codes),
            }
        )
        i = 0
        for code in codes:
            dttm = dttm_start + timedelta(hours=i)
            i += 1
            for f_name in filter(lambda x: x.startswith(code), files):
                with open(folder_path + f_name, 'rb') as f:
                    frame = Frame.objects.create(
                        camera=cam,
                        photo=File(f, f_name),
                        dttm=dttm,
                    )
                if 'violation' in f_name:
                    Violation.objects.create(
                        frame=frame,
                    )
                dttm += timedelta(seconds=1)
