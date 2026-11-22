# Merkezi loglama mekanizması (log.md yerine sistem logları)
# src/core/logger.py

import logging
from pathlib import Path


def get_logger(name: str = "HybridPlanner", log_file: str = "logs/pipeline.log") -> logging.Logger:
    """
    Tez deneyleri ve hata analizi için hem konsola hem de dosyaya
    yapılandırılmış log yazan merkezi logger döndürür.
    """
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Konsol çıktısı
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Dosya çıktısı
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger