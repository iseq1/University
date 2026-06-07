# Сборка проекта LaTeX

Проект компилируется с использованием:

* XeLaTeX

Порядок сборки:

```bash
xelatex beamer_main.tex
xelatex beamer_main.tex
```

В VSCode используется расширение LaTeX Workshop + MikTex.
### Настройки сборки находятся в:

```text
.vscode/settings.json
```

### Запуск сборки:
1. Открыть проект в Visual Studio Code
2. Прожать: `ctrl` + `shift` + `P`
3. Выбрать: `Latex Workshop: Build with recipe`
4. Выбрать способ сборки: `xelatex only`