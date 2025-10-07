# RJW-IDD IDE and Editor Configurations

This directory contains configuration files and settings optimized for various IDEs and editors to work effectively with RJW-IDD projects.

## Supported Editors

### Visual Studio Code / Cursor / Windsurf
- **Directory**: `.vscode/`, `.cursor/`, `.windsurf/`
- **Features**: Full Python support, linting, formatting, testing, Git integration
- **Extensions**: Python, Black, Ruff, MyPy, GitHub Copilot, Jupyter, Docker

### Other Editors

#### Cline
Cline is a command-line editor. Use these settings:

```bash
# Add to your shell profile (~/.bashrc, ~/.zshrc, etc.)
export EDITOR="cline"
export RJW_IDD_PROJECT_ROOT="$(pwd)"

# Python environment setup
export PYTHONPATH="$RJW_IDD_PROJECT_ROOT:$PYTHONPATH"
export PATH="$RJW_IDD_PROJECT_ROOT/.venv/bin:$PATH"

# Aliases for common tasks
alias rjw-test="python -m pytest tests/"
alias rjw-lint="ruff check . && black --check . && mypy ."
alias rjw-format="black . && ruff check --fix ."
```

#### Roo
Roo is a modern code editor. Create `~/.config/roo/settings.json`:

```json
{
  "python": {
    "interpreter": "./.venv/bin/python",
    "linting": {
      "enabled": true,
      "tools": ["ruff", "mypy"]
    },
    "formatting": {
      "provider": "black",
      "lineLength": 100
    }
  },
  "editor": {
    "formatOnSave": true,
    "rulers": [100],
    "tabSize": 4,
    "insertSpaces": true,
    "trimTrailingWhitespace": true,
    "insertFinalNewline": true
  },
  "files": {
    "exclude": [
      "**/__pycache__",
      "**/.pytest_cache",
      "**/*.pyc",
      "**/.venv"
    ]
  },
  "extensions": {
    "recommendations": [
      "python",
      "ruff",
      "black",
      "mypy",
      "git",
      "docker"
    ]
  }
}
```

#### Kilo
Kilo is a terminal-based editor. Add to your `~/.config/kilo/init.lua`:

```lua
-- RJW-IDD Kilo configuration
local kilo = require('kilo')

-- Python settings
kilo.set('python.interpreter', './.venv/bin/python')
kilo.set('python.linting', true)
kilo.set('python.formatter', 'black')
kilo.set('python.line_length', 100)

-- Editor settings
kilo.set('editor.format_on_save', true)
kilo.set('editor.rulers', {100})
kilo.set('editor.tab_size', 4)
kilo.set('editor.insert_spaces', true)
kilo.set('editor.trim_trailing_whitespace', true)
kilo.set('editor.insert_final_newline', true)

-- File associations
kilo.set('files.associations', {
  ['*.py'] = 'python',
  ['*.md'] = 'markdown',
  ['*.yml'] = 'yaml',
  ['*.yaml'] = 'yaml',
  ['*.json'] = 'json'
})

-- Keybindings for RJW-IDD workflow
kilo.map('n', '<leader>t', ':!python -m pytest tests/<CR>')
kilo.map('n', '<leader>l', ':!ruff check . && black --check . && mypy .<CR>')
kilo.map('n', '<leader>f', ':!black . && ruff check --fix .<CR>')
kilo.map('n', '<leader>g', ':!git status<CR>')
```

#### Gemini Code Assist
Gemini Code Assist integrates with various editors. Configure via:

**VS Code Extension Settings:**
```json
{
  "geminiCodeAssist.enable": true,
  "geminiCodeAssist.python": {
    "enabled": true,
    "linting": true,
    "formatting": true,
    "testing": true
  },
  "geminiCodeAssist.context": {
    "include": [
      "specs/",
      "docs/",
      "research/",
      "artifacts/"
    ],
    "exclude": [
      ".venv/",
      "__pycache__/",
      ".pytest_cache/"
    ]
  }
}
```

**Standalone CLI Configuration:**
Create `~/.config/gemini-code-assist/config.yaml`:
```yaml
project:
  type: "rjw-idd"
  root: "."
  language: "python"

python:
  interpreter: "./.venv/bin/python"
  virtualenv: ".venv"
  requirements: "requirements-dev.txt"

linting:
  enabled: true
  tools: ["ruff", "mypy", "black"]

testing:
  framework: "pytest"
  config: "pyproject.toml"
  coverage: true

context:
  include:
    - "specs/"
    - "docs/"
    - "research/"
    - "artifacts/"
  exclude:
    - ".venv/"
    - "__pycache__/"
    - ".pytest_cache/"
    - "*.pyc"

ai:
  model: "gemini-pro"
  context_window: 8192
  temperature: 0.1
  max_tokens: 2048
```

#### Claude Code
Claude Code is Anthropic's CLI tool. Configure with:

Create `~/.config/claude-code/config.json`:
```json
{
  "project": {
    "type": "rjw-idd",
    "language": "python",
    "root": "."
  },
  "python": {
    "interpreter": "./.venv/bin/python",
    "virtualenv": ".venv",
    "requirements": "requirements-dev.txt"
  },
  "linting": {
    "enabled": true,
    "tools": ["ruff", "mypy", "black"],
    "fix_on_save": true
  },
  "testing": {
    "framework": "pytest",
    "config": "pyproject.toml",
    "coverage": true,
    "auto_run": false
  },
  "context": {
    "include": [
      "specs/",
      "docs/",
      "research/",
      "artifacts/",
      "tools/",
      "scripts/"
    ],
    "exclude": [
      ".venv/",
      "__pycache__/",
      ".pytest_cache/",
      "*.pyc",
      "*.log"
    ]
  },
  "ai": {
    "model": "claude-3-5-sonnet-20241022",
    "max_tokens": 4096,
    "temperature": 0.1
  },
  "workflow": {
    "test_first": true,
    "evidence_driven": true,
    "spec_driven": true,
    "guard_enforced": true
  }
}
```

#### Gemini CLI
Google's Gemini CLI tool. Configure with:

Create `~/.config/gemini-cli/rjw-idd.yaml`:
```yaml
project:
  name: "RJW-IDD Starter Kit"
  type: "methodology"
  language: "python"
  version: "1.0.0"

environment:
  python_version: "3.11"
  virtualenv: ".venv"
  requirements: "requirements-dev.txt"

tools:
  linter: "ruff"
  formatter: "black"
  type_checker: "mypy"
  test_runner: "pytest"

context:
  include:
    - "specs/"
    - "docs/"
    - "research/"
    - "artifacts/"
    - "tools/"
    - "scripts/"
  exclude:
    - ".venv/"
    - "__pycache__/"
    - ".pytest_cache/"
    - "*.pyc"
    - "*.log"
    - ".git/"

ai:
  model: "gemini-1.5-pro"
  temperature: 0.1
  max_output_tokens: 2048
  safety_settings:
    - category: "HARM_CATEGORY_HARASSMENT"
      threshold: "BLOCK_MEDIUM_AND_ABOVE"
    - category: "HARM_CATEGORY_HATE_SPEECH"
      threshold: "BLOCK_MEDIUM_AND_ABOVE"
    - category: "HARM_CATEGORY_SEXUALLY_EXPLICIT"
      threshold: "BLOCK_MEDIUM_AND_ABOVE"
    - category: "HARM_CATEGORY_DANGEROUS_CONTENT"
      threshold: "BLOCK_MEDIUM_AND_ABOVE"

workflow:
  phases:
    - "research_driven_development"
    - "spec_driven_development"
    - "implementation"
    - "operations"
  guards:
    - "red_green_guard"
    - "change_log_guard"
    - "governance_alignment_guard"
    - "living_docs_guard"
```

#### Codex
OpenAI's Codex-based tools. Configure with:

Create `~/.config/codex/rjw-idd.json`:
```json
{
  "project": {
    "name": "RJW-IDD Starter Kit",
    "type": "methodology",
    "language": "python"
  },
  "openai": {
    "model": "gpt-4-turbo-preview",
    "temperature": 0.1,
    "max_tokens": 4096,
    "api_key_env": "OPENAI_API_KEY"
  },
  "python": {
    "interpreter": "./.venv/bin/python",
    "virtualenv": ".venv",
    "requirements": "requirements-dev.txt"
  },
  "development": {
    "linting": {
      "enabled": true,
      "tools": ["ruff", "mypy"]
    },
    "formatting": {
      "enabled": true,
      "tool": "black",
      "line_length": 100
    },
    "testing": {
      "enabled": true,
      "framework": "pytest",
      "coverage": true
    }
  },
  "context": {
    "include": [
      "specs/",
      "docs/",
      "research/",
      "artifacts/",
      "tools/",
      "scripts/"
    ],
    "exclude": [
      ".venv/",
      "__pycache__/",
      ".pytest_cache/",
      "*.pyc",
      "*.log"
    ]
  },
  "workflow": {
    "methodology": "rjw-idd",
    "phases": [
      "RDD",
      "SDD",
      "Implementation",
      "Operations"
    ],
    "guards": [
      "red_green",
      "change_log",
      "governance_alignment",
      "living_docs"
    ]
  }
}
```

## Additional Editors

### Vim/Neovim
Add to `~/.vimrc` or `~/.config/nvim/init.vim`:

```vim
" RJW-IDD Python development settings
set nocompatible
set encoding=utf-8
set tabstop=4
set shiftwidth=4
set expandtab
set autoindent
set ruler
set colorcolumn=100
set textwidth=100
set formatoptions+=t
set wrap
set linebreak

" Python-specific settings
autocmd FileType python setlocal
    \ tabstop=4
    \ shiftwidth=4
    \ expandtab
    \ autoindent
    \ fileformat=unix

" File type associations
autocmd BufRead,BufNewFile *.py set filetype=python
autocmd BufRead,BufNewFile *.md set filetype=markdown
autocmd BufRead,BufNewFile *.yml,*.yaml set filetype=yaml
autocmd BufRead,BufNewFile *.json set filetype=json

" Key mappings for RJW-IDD workflow
nnoremap <leader>t :!cd %:p:h && python -m pytest tests/<CR>
nnoremap <leader>l :!cd %:p:h && ruff check % && black --check %<CR>
nnoremap <leader>f :!cd %:p:h && black %<CR>
nnoremap <leader>g :!cd %:p:h && git status<CR>

" Plugins (using vim-plug)
call plug#begin('~/.vim/plugged')
Plug 'vim-python/python-syntax'
Plug 'nvie/vim-flake8'
Plug 'psf/black'
Plug 'dense-analysis/ale'
call plug#end()
```

### Emacs
Add to `~/.emacs.d/init.el`:

```elisp
;; RJW-IDD Python development settings
(require 'package)
(add-to-list 'package-archives '("melpa" . "https://melpa.org/packages/") t)
(package-initialize)

;; Basic settings
(setq-default tab-width 4)
(setq-default indent-tabs-mode nil)
(setq-default fill-column 100)
(global-display-fill-column-indicator-mode 1)
(add-hook 'before-save-hook 'delete-trailing-whitespace)
(setq require-final-newline t)

;; Python development
(use-package python
  :ensure t
  :mode ("\\.py\\'" . python-mode)
  :interpreter ("python" . python-mode)
  :config
  (setq python-indent-offset 4)
  (add-hook 'python-mode-hook
            (lambda ()
              (setq fill-column 100)
              (display-fill-column-indicator-mode))))

;; Black formatting
(use-package python-black
  :ensure t
  :after python
  :hook (python-mode . python-black-on-save-mode))

;; Ruff linting
(use-package flycheck
  :ensure t
  :init (global-flycheck-mode))

;; Key bindings for RJW-IDD workflow
(global-set-key (kbd "C-c t") (lambda () (interactive) (shell-command "python -m pytest tests/")))
(global-set-key (kbd "C-c l") (lambda () (interactive) (shell-command "ruff check . && black --check . && mypy .")))
(global-set-key (kbd "C-c f") (lambda () (interactive) (shell-command "black . && ruff check --fix .")))
(global-set-key (kbd "C-c g") (lambda () (interactive) (shell-command "git status")))
```

### Sublime Text
Create `~/Library/Application Support/Sublime Text/Packages/User/RJW-IDD.sublime-project`:

```json
{
  "folders": [
    {
      "path": "."
    }
  ],
  "settings": {
    "tab_size": 4,
    "translate_tabs_to_spaces": true,
    "trim_trailing_white_space_on_save": true,
    "ensure_newline_at_eof_on_save": true,
    "rulers": [100],
    "word_wrap": true,
    "wrap_width": 100
  },
  "build_systems": [
    {
      "name": "RJW-IDD Test",
      "cmd": ["python", "-m", "pytest", "tests/"],
      "working_dir": "${project_path}"
    },
    {
      "name": "RJW-IDD Lint",
      "cmd": ["ruff", "check", ".", "&&", "black", "--check", ".", "&&", "mypy", "."],
      "working_dir": "${project_path}"
    },
    {
      "name": "RJW-IDD Format",
      "cmd": ["black", ".", "&&", "ruff", "check", "--fix", "."],
      "working_dir": "${project_path}"
    }
  ]
}
```

### JetBrains IDEs (PyCharm, IntelliJ)
Create `.idea/rjw-idd.iml` and configure:

**Project Structure:**
- Set Python interpreter to `.venv/bin/python`
- Mark `src/` as sources root
- Mark `tests/` as test sources root

**Code Style:**
- Right margin: 100 columns
- Use spaces, 4 spaces per indent
- Black formatter integration

**External Tools:**
- Add tools for pytest, ruff, black, mypy
- Key bindings for common commands

### Atom
Create `.atom/config.cson`:

```coffeescript
"*":
  core:
    telemetryConsent: "no"
  editor:
    tabLength: 4
    softTabs: true
    softWrap: true
    preferredLineLength: 100
    showInvisibles: true
    normalizeIndentOnPaste: true

".python.source":
  editor:
    tabLength: 4
    softTabs: true

"autocomplete-python":
  includeCompletionsForImportStatements: true
  includeCompletionsForImportStatements: true

"python-black":
  lineLength: 100
  formatOnSave: true

"linter-ui-default":
  showPanel: true
```

## Setup Instructions

### For New Contributors
1. Choose your preferred editor from the list above
2. Copy the appropriate configuration to your editor's settings
3. Install recommended extensions/plugins
4. Run `scripts/setup/bootstrap_project.sh` to set up the environment
5. Start coding with full RJW-IDD workflow support

### Environment Variables
Set these in your shell profile for all editors:

```bash
export RJW_IDD_PROJECT_ROOT="/path/to/rjw-idd-starter-kit"
export PYTHONPATH="$RJW_IDD_PROJECT_ROOT:$PYTHONPATH"
export PATH="$RJW_IDD_PROJECT_ROOT/.venv/bin:$PATH"
```

### Validation
Run this command to verify your editor setup:

```bash
python -m pytest tests/ --tb=short
ruff check .
black --check .
mypy .
```

All commands should pass without errors for a properly configured environment.