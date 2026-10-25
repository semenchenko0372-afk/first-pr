# first-pr

Учебный репозиторий для первого pull request.

## Скиллы Claude Code для видео и дизайна

В `.claude/skills/` установлены скиллы (подхватываются Claude Code автоматически в этом репозитории):

| # | Набор | Источник | Для чего |
|---|-------|----------|----------|
| 1 | HyperFrames (HeyGen) | [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) | видео из HTML/CSS/JS: `hyperframes`, `hyperframes-cli`, `media-use`, `slideshow`, `figma`… |
| 2 | Remotion | [remotion-dev/skills](https://github.com/remotion-dev/skills) | видео на React: `remotion-best-practices`, `remotion-captions`, `remotion-render`… |
| 3 | Эмиль Ковальски | [emilkowalski/skills](https://github.com/emilkowalski/skills) | анимации и полировка UI: `emil-design-eng`, `animate`, `review-animations`… (без мобильных: `write-swift`, `mobile-native`, `animate-expo`) |
| 4 | taste-skill | [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) | «вкус» во фронтенде, без шаблонного AI-дизайна |
| 5 | impeccable | [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | аудит и доводка дизайна (типографика, отступы, шрифты) |
| 6 | frontend-design (Anthropic) | [anthropics/skills](https://github.com/anthropics/skills) | официальный скилл для фронтенд-дизайна |
| 7 | UI UX Pro Max | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | стили, палитры, шрифтовые пары, дизайн-системы |

Для рендера видео нужны Node.js и ffmpeg (HyperFrames и Remotion ставят свои пакеты через `npx` при первом использовании).
