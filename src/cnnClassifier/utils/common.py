import os
from box.exceptions import BoxValueError
import yaml
from cnnClassifier import logger
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any
import base64


# các hàm until sau được sử dụng để đảm bảo rằng các hàm có chú thích kiểu (type annotations) đúng
# và sẽ ném ra lỗi nếu không đúng kiểu nó giúp đảm bảo tính nhất quán 
# và an toàn khi làm việc với các kiểu dữ liệu trong Python


# mục đích: Đọc một file YAML và trả về nội dung của nó dưới dạng một đối tượng ConfigBox.
# Cách hoạt động: Mở file YAML, đọc nội dung và chuyển đổi nó thành một đối tượng ConfigBox.
@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """reads yaml file and returns
    Args:
        path_to_yaml (str): path like input
    Raises:
        ValueError: if yaml file is empty
        e: empty file
    Returns:
        ConfigBox: ConfigBox type
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e
    
    
# Mục đích: Tạo ra nhiều thư mục cùng một lúc.
# Cách hoạt động: Nhận vào một danh sách các đường dẫn, 
# lặp qua từng đường dẫn và dùng os.makedirs(..., exist_ok=True) để tạo thư mục. 
# Lệnh này an toàn vì nó sẽ không báo lỗi nếu thư mục đã tồn tại.
@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """create list of directories
    Args:
        path_to_directories (list): list of path of directories
        ignore_log (bool, optional): ignore if multiple dirs is to be created. Defaults to False.
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"created directory at: {path}")


# Mục đích: Lưu một dictionary của Python vào một file JSON.
# Cách hoạt động: Mở một file, sau đó dùng json.dump() để ghi dictionary vào file đó 
# với định dạng thụt lề 4 dấu cách cho dễ đọc (indent=4).
@ensure_annotations
def save_json(path: Path, data: dict):
    """save json data
    Args:
        path (Path): path to json file
        data (dict): data to be saved in json file
    """
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

    logger.info(f"json file saved at: {path}")


# Mục đích: Đọc một file JSON và trả về một đối tượng tiện dụng.
# Cách hoạt động: Mở và đọc file JSON bằng json.load(), sau đó 
# chuyển dictionary đọc được thành đối tượng ConfigBox để có thể truy cập bằng dấu chấm 
# (ví dụ: config.key thay vì config['key']).
@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """load json files data
    Args:
        path (Path): path to json file
    Returns:
        ConfigBox: data as class attributes instead of dict
    """
    with open(path) as f:
        content = json.load(f)

    logger.info(f"json file loaded succesfully from: {path}")
    return ConfigBox(content)


# Mục đích: Lưu bất kỳ đối tượng Python nào (như model đã huấn luyện, scaler...) vào một file nhị phân (binary).
# Cách hoạt động: Sử dụng thư viện joblib để "dump" (đổ) đối tượng vào một file. 
# joblib thường hiệu quả hơn pickle cho các đối tượng lớn chứa mảng NumPy.
@ensure_annotations
def save_bin(data: Any, path: Path):
    """save binary file
    Args:
        data (Any): data to be saved as binary
        path (Path): path to binary file
    """
    joblib.dump(value=data, filename=path)
    logger.info(f"binary file saved at: {path}")


# Mục đích: Đọc một đối tượng Python từ một file nhị phân đã được lưu bằng joblib.
# Cách hoạt động: Dùng joblib.load() để tải đối tượng từ file.
@ensure_annotations
def load_bin(path: Path) -> Any:
    """load binary data
    Args:
        path (Path): path to binary file
    Returns:
        Any: object stored in the file
    """
    data = joblib.load(path)
    logger.info(f"binary file loaded from: {path}")
    return data


# Mục đích: Lấy kích thước của một file và trả về dưới dạng một chuỗi văn bản dễ đọc (đơn vị KB).
# Cách hoạt động: Dùng os.path.getsize() để lấy kích thước file (tính bằng byte), 
# chia cho 1024 để đổi sang KB, làm tròn và định dạng lại thành chuỗi.
@ensure_annotations
def get_size(path: Path) -> str:
    """get size in KB
    Args:
        path (Path): path of the file
    Returns:
        str: size in KB
    """
    size_in_kb = round(os.path.getsize(path)/1024)
    return f"~ {size_in_kb} KB"


# Mục đích: Giải mã một chuỗi Base64 thành một file ảnh.
# Cách hoạt động: Nhận một chuỗi Base64 (thường được gửi từ một web form), 
# dùng base64.b64decode() để chuyển nó lại thành dữ liệu nhị phân của ảnh, 
# sau đó ghi dữ liệu này ra một file. Dùng cho việc nhận ảnh từ phía người dùng (frontend).
def decodeImage(imgstring, fileName):
    imgdata = base64.b64decode(imgstring)
    with open(fileName, 'wb') as f:
        f.write(imgdata)
        f.close()

# Mục đích: Mã hóa một file ảnh thành một chuỗi Base64.
# Cách hoạt động: Đọc một file ảnh ở chế độ nhị phân ("rb"), 
# sau đó dùng base64.b64encode() để chuyển dữ liệu ảnh thành 
# một chuỗi văn bản an toàn để truyền đi qua mạng (ví dụ: trong một file JSON).
def encodeImageIntoBase64(croppedImagePath):
    with open(croppedImagePath, "rb") as f:
        return base64.b64encode(f.read())