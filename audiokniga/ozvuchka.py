import asyncio
import pathlib
import sys

import edge_tts

VOICE = "ru-RU-SvetlanaNeural"
RATE = "-5%"     # скорость чтения: "-10%" медленнее, "+0%" обычная
CHUNK = 20000    # примерно символов в одной части (около 20 минут звука)


def read_text(path):
    raw = path.read_bytes()
    try:
        return raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        return raw.decode("cp1251")


def split_parts(text):
    parts, cur = [], ""
    for para in text.split("\n"):
        if len(cur) + len(para) > CHUNK and cur.strip():
            parts.append(cur)
            cur = ""
        cur += para + "\n"
    if cur.strip():
        parts.append(cur)
    return parts


async def main(src):
    parts = split_parts(read_text(src))
    out = src.with_suffix("")
    out.mkdir(exist_ok=True)
    print(f"Книга разбита на {len(parts)} частей. Результат будет в папке: {out}")
    for i, part in enumerate(parts, 1):
        f = out / f"{i:03}.mp3"
        if f.exists():
            continue  # уже готово: при перезапуске продолжаем с места остановки
        print(f"Озвучиваю часть {i} из {len(parts)}...")
        tmp = f.with_suffix(".part")
        for attempt in range(3):
            try:
                await edge_tts.Communicate(part, VOICE, rate=RATE).save(str(tmp))
                break
            except Exception as e:
                print(f"  Ошибка: {e}. Пробую ещё раз...")
                await asyncio.sleep(5)
        else:
            print("Не получилось. Проверьте интернет и запустите ещё раз — готовые части сохранятся.")
            return
        tmp.replace(f)
    print("Готово! Аудиокнига в папке:", out)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python ozvuchka.py kniga.txt")
        sys.exit(1)
    asyncio.run(main(pathlib.Path(sys.argv[1])))
