from zipfile import ZipFile, ZIP_DEFLATED
class FileService:
    @staticmethod
    def save_to_file(file_path, data):
        """
        Save data in file
        :param file_path:
        :param data:
        :return:
        """
        try:
            with open(file_path, 'w') as file:
                file.writelines(data)
                file.close()
        except FileNotFoundError as e:
            print(f"Ошибка: {e}")
            return None

    @staticmethod
    def archive_file(file_path, zip_path):
        """
        Archive file
        :param file_path:
        :param zip_path:
        :return:
        """
        with ZipFile(zip_path, 'w', compression=ZIP_DEFLATED, compresslevel=2) as archive:
            archive.write(file_path)

    @staticmethod
    def get_archive_info(zip_path):
        """
        Get archive info
        :param zip_path:
        :return:
        """
        try:
            with ZipFile(zip_path, 'r') as archive:
                for item in archive.infolist():
                    if item.is_dir():
                        print(f"Папка: {item.filename}")
                    else:
                        print(f"Файл: {item.filename}")
                    print(f"Размер: {item.file_size}")
                    print(f"Дата создания: {item.date_time}")
        except FileNotFoundError as e:
            print(f"Ошибка: {e}")
            return None
        except IOError as e:
            print(f"Ошибка: {e}")
            return None
