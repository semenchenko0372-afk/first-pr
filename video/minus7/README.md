# «Этаж −7» — пробный вертикальный хоррор-ролик

58 секунд, 1080×1920, 30 fps. Готовый файл: `renders/minus7.mp4`.

**Сюжет.** 23:47, ты последний в офисе. Лифт проезжает первый этаж и уезжает на несуществующий
минус седьмой. В конце тёмного коридора — монитор с записью камеры лифта: время то же, 23:47,
и за твоей спиной в кадре кто-то стоит. Финал-крючок: «Ты обернёшься? Продолжение следует».

## Сцены

| Время | Сцена | Файл |
|---|---|---|
| 0–5.6 | Ночной небоскрёб под дождём, наезд на единственное светящееся окно | `compositions/exterior.html` |
| 5.6–9.2 | Панель лифта, рука нажимает «1» | `compositions/panel.html` |
| 9.2–18.9 | Табло: 5…1, затем 0, −1… | `compositions/floors.html` |
| 18.9–26 | Мигает свет, «−7», лицо в красном свете | `compositions/flicker.html` |
| 26–33.8 | Двери, фонарик, коридор с царапинами «23:47» | `compositions/corridor.html` |
| 33.8–45.6 | Монитор, запись CAM 04, фигура за спиной | `compositions/cctv.html` |
| 45.6–53.75 | Крупный план, бледное лицо за плечом, шёпот | `compositions/behind.html` |
| 53.75–58.5 | «Ты обернёшься?» | `compositions/endcard.html` |

Субтитры — `compositions/captions.html`, плёночное зерно и виньетка — `compositions/fx.html`.

## Как пересобрать

```bash
cd video/minus7
python3 tools/char.py build     # вставить героя в сцены с маркером %%CHAR:..%% (уже вставлен)
bash tools/mix.sh               # пересобрать звуковую дорожку assets/soundtrack.wav
npx hyperframes check           # проверка
npx hyperframes preview         # просмотр в браузере
npx hyperframes render -o renders/minus7.mp4 --quality delivery
```

Тайминг реплик — `voice-timing.txt`. Чтобы заменить голос (например, на свою запись),
положите файлы `assets/voice/p01.mp3 … p21.mp3` и выполните `bash tools/voice.sh && bash tools/mix.sh`.

Лицензии на музыку и звуки — `CREDITS.md`.
