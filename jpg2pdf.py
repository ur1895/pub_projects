import os
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import portrait


def get_image_info(image_path):
    image = Image.open(image_path)
    width, height = image.size

    info = {
        "width": width,
        "height": height,
        "image": image,
    }

    # Выводим информацию о входном изображении
    print(f"\nИнформация о входном изображении ({os.path.basename(image_path)}):")
    print(f"Размер: {width} x {height} пикселей")
    print(f"Ориентация: {'альбомная' if width >= height else 'книжная'}")

    return info


def convert_to_pdf(image_info, output_pdf_path):
    image = image_info['image']
    width, height = image_info['width'], image_info['height']
    orientation = 'альбомная' if width >= height else 'книжная'

    # Создаем PDF-файл с размером страницы, равным размеру изображения
    page_size = (width, height) if orientation == "альбомная" else (height, width)

    # Избегаем конфликта имен, изменяя имя переменной
    pdf_output_path = output_pdf_path

    pdf_canvas = canvas.Canvas(pdf_output_path, pagesize=page_size)

    # Вставляем изображение в PDF с сохранением пропорций и более высоким разрешением
    pdf_canvas.drawInlineImage(image, 0, 0, width=width, height=height, preserveAspectRatio=True)

    # Сохраняем PDF-файл
    pdf_canvas.save()

    print(f"Обработка завершена. PDF сохранен в {pdf_output_path}")


def is_image_file(file_path):
    valid_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"}
    return any(file_path.lower().endswith(ext) for ext in valid_extensions)


if __name__ == "__main__":
    # Указываем путь к папке с изображениями
    input_folder_path = r"C:\JPG2PDF"

    # Получаем список всех файлов в папке
    all_files = os.listdir(input_folder_path)

    # Фильтруем только графические файлы
    image_files = [f for f in all_files if is_image_file(os.path.join(input_folder_path, f))]

    # Если есть графические файлы, обрабатываем их
    if image_files:
        for image_file in image_files:
            image_file_path = os.path.join(input_folder_path, image_file)

            # Анализируем изображение и получаем информацию
            input_image_info = get_image_info(image_file_path)

            # Указываем путь для сохранения PDF на основе пути к изображению
            output_pdf_path = f"{os.path.splitext(image_file_path)[0]}.pdf"

            # Преобразуем изображение в PDF
            convert_to_pdf(input_image_info, output_pdf_path)
    else:
        print("В выбранной папке нет графических файлов.")
