# Сборка проекта LaTeX

Проект компилируется с использованием:

* XeLaTeX
* Biber

Порядок сборки:

```bash
xelatex article_main.tex
biber article_main
xelatex article_main.tex
xelatex article_main.tex
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
4. Выбрать способ сборки: `xelatex -> biber -> xelatex*2`