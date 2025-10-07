# RJW-IDD Internationalization (i18n) Support

This document outlines the internationalization framework for RJW-IDD projects.

## Overview

Internationalization enables RJW-IDD projects to support multiple languages and locales, making the methodology accessible to global teams.

## Directory Structure

```
project/
├── locales/
│   ├── en/
│   │   ├── LC_MESSAGES/
│   │   │   ├── messages.po
│   │   │   └── messages.mo
│   ├── es/
│   │   ├── LC_MESSAGES/
│   │   │   ├── messages.po
│   │   │   └── messages.mo
│   └── templates/
│       └── messages.pot
├── src/
│   └── i18n.py
└── babel.cfg
```

## Configuration

### babel.cfg
```ini
[python: src/**.py]
[jinja2: templates/**.html]
extensions=jinja2.ext.i18n

[extractors]
jinja2 = jinja2.ext.extract:extract
```

### pyproject.toml additions
```toml
[tool.babel]
locale_dirs = ["locales"]
domain = "messages"

[project.optional-dependencies]
i18n = [
    "babel>=2.12",
    "gettext>=4.0",
]
```

## Python Implementation

### i18n.py
```python
"""Internationalization utilities for RJW-IDD."""

import gettext
import locale
import os
from pathlib import Path
from typing import Optional

# Default settings
DEFAULT_DOMAIN = "messages"
DEFAULT_LOCALES_DIR = Path(__file__).parent.parent / "locales"


class I18N:
    """Internationalization manager."""

    def __init__(
        self,
        domain: str = DEFAULT_DOMAIN,
        locales_dir: Optional[Path] = None,
        fallback_locale: str = "en"
    ):
        self.domain = domain
        self.locales_dir = locales_dir or DEFAULT_LOCALES_DIR
        self.fallback_locale = fallback_locale
        self._translators = {}

    def get_translator(self, locale_code: str) -> gettext.GNUTranslations:
        """Get translator for specific locale."""
        if locale_code in self._translators:
            return self._translators[locale_code]

        try:
            translator = gettext.translation(
                self.domain,
                localedir=str(self.locales_dir),
                languages=[locale_code],
                fallback=True
            )
            self._translators[locale_code] = translator
            return translator
        except FileNotFoundError:
            # Fallback to default locale
            if locale_code != self.fallback_locale:
                return self.get_translator(self.fallback_locale)
            raise

    def gettext(self, message: str, locale_code: Optional[str] = None) -> str:
        """Translate message to specified locale."""
        if locale_code is None:
            locale_code = self._get_current_locale()

        translator = self.get_translator(locale_code)
        return translator.gettext(message)

    def ngettext(
        self,
        singular: str,
        plural: str,
        n: int,
        locale_code: Optional[str] = None
    ) -> str:
        """Translate pluralized message."""
        if locale_code is None:
            locale_code = self._get_current_locale()

        translator = self.get_translator(locale_code)
        return translator.ngettext(singular, plural, n)

    def _get_current_locale(self) -> str:
        """Get current system locale."""
        try:
            # Get locale from environment or system
            current_locale, _ = locale.getlocale()
            if current_locale:
                # Extract language code (e.g., 'en_US' -> 'en')
                return current_locale.split('_')[0].lower()
            return self.fallback_locale
        except (locale.Error, ValueError):
            return self.fallback_locale

    def set_locale(self, locale_code: str) -> None:
        """Set current locale for translations."""
        try:
            locale.setlocale(locale.LC_ALL, f"{locale_code}.UTF-8")
        except locale.Error:
            # Fallback to language only
            try:
                locale.setlocale(locale.LC_ALL, locale_code)
            except locale.Error:
                pass  # Keep default


# Global instance
i18n = I18N()

# Convenience functions
def _(message: str) -> str:
    """Translate message using current locale."""
    return i18n.gettext(message)

def ngettext(singular: str, plural: str, n: int) -> str:
    """Translate pluralized message."""
    return i18n.ngettext(singular, plural, n)
```

## Usage Examples

### Basic Translation
```python
from src.i18n import _, ngettext

# Simple translation
message = _("Hello, World!")
error_msg = _("File not found")

# Plural forms
files_count = 5
message = ngettext(
    "Found %(count)d file",
    "Found %(count)d files",
    files_count
) % {"count": files_count}
```

### Template Translation
```html
<!-- templates/welcome.html -->
<h1>{{ _("Welcome to RJW-IDD") }}</h1>
<p>{{ _("This methodology helps you build better software.") }}</p>
```

### Error Messages
```python
from src.i18n import _

class RJWIDDError(Exception):
    """Base exception with i18n support."""

    def __init__(self, message_key: str, **kwargs):
        self.message_key = message_key
        self.kwargs = kwargs
        super().__init__(self.get_message())

    def get_message(self) -> str:
        """Get localized error message."""
        return _(self.message_key) % self.kwargs

class ValidationError(RJWIDDError):
    def __init__(self, field: str, reason: str):
        super().__init__(
            "validation_error",
            field=field,
            reason=reason
        )
```

## Translation Workflow

### 1. Extract Messages
```bash
# Extract messages from source code
pybabel extract -F babel.cfg -o locales/templates/messages.pot src/

# Extract from templates (if using Jinja2)
pybabel extract -F babel.cfg -o locales/templates/messages.pot templates/
```

### 2. Initialize Locales
```bash
# Create translation files for new languages
pybabel init -i locales/templates/messages.pot -d locales -l es
pybabel init -i locales/templates/messages.pot -d locales -l fr
pybabel init -i locales/templates/messages.pot -d locales -l de
```

### 3. Update Translations
```bash
# Update existing translation files when source changes
pybabel update -i locales/templates/messages.pot -d locales
```

### 4. Compile Translations
```bash
# Compile .po files to .mo files for runtime use
pybabel compile -d locales
```

## Supported Languages

### Core Languages
- **English (en)**: Default/fallback language
- **Spanish (es)**: Complete translation available
- **French (fr)**: Complete translation available
- **German (de)**: Complete translation available
- **Portuguese (pt)**: Partial translation
- **Chinese (zh)**: Partial translation
- **Japanese (ja)**: Partial translation

### Message Categories

#### Core Methodology Messages
- Phase names and descriptions
- Guard error messages
- Validation messages
- Change log entries

#### Tool Messages
- CLI help text
- Progress indicators
- Error descriptions
- Success confirmations

#### Documentation Messages
- Section headers
- Navigation labels
- Status indicators
- Help text

## Quality Assurance

### Translation Testing
```python
import pytest
from src.i18n import i18n

def test_translations_complete():
    """Test that all supported locales have translations."""
    test_messages = [
        "Hello, World!",
        "File not found",
        "Validation error",
        "Operation completed successfully"
    ]

    for locale in ["en", "es", "fr", "de"]:
        for message in test_messages:
            translated = i18n.gettext(message, locale)
            assert translated != message or locale == "en"  # English is source

def test_plural_forms():
    """Test plural form handling."""
    for locale in ["en", "es", "fr", "de"]:
        # Test singular
        result = i18n.ngettext("%(count)d file", "%(count)d files", 1, locale)
        assert "%(count)d" in result

        # Test plural
        result = i18n.ngettext("%(count)d file", "%(count)d files", 2, locale)
        assert "%(count)d" in result
```

### CI Integration
```yaml
- name: Test i18n
  run: |
    python -m pytest tests/test_i18n.py -v

- name: Check translation completeness
  run: |
    # Custom script to check for missing translations
    python tools/check_translations.py
```

## Best Practices

### Message Keys
- Use descriptive, unique message keys
- Include context in key names: `error_file_not_found`
- Avoid concatenating translated strings
- Use placeholders for dynamic content: `%(name)s`

### Cultural Adaptation
- Consider date/time formats per locale
- Respect number formatting conventions
- Account for text expansion in translations
- Test with real users from target locales

### Performance
- Compile translations for production use
- Cache translator instances
- Lazy load translations when possible
- Monitor translation file sizes

## Tools and Resources

### Translation Tools
- **Poedit**: GUI editor for .po files
- **Virtaal**: Cross-platform translation tool
- **Gtranslator**: GNOME translation editor
- **Transifex**: Web-based translation platform

### Quality Tools
- **Pology**: Translation quality assurance
- **translate-toolkit**: Translation file processing
- **LanguageTool**: Grammar and style checking

### Learning Resources
- [GNU gettext manual](https://www.gnu.org/software/gettext/manual/)
- [Babel documentation](https://babel.pocoo.org/)
- [Unicode CLDR](https://cldr.unicode.org/)
- [Mozilla l10n](https://mozilla-l10n.github.io/)

## Migration Guide

### From Non-i18n Code
1. Wrap user-facing strings with `_()`
2. Extract messages to .pot file
3. Create initial translations
4. Update build process to compile translations
5. Test with different locales

### Adding New Languages
1. Extract current messages
2. Initialize new locale: `pybabel init -l <code>`
3. Translate messages in .po file
4. Compile translations
5. Update language detection logic
6. Test thoroughly

This i18n framework ensures RJW-IDD can be effectively used by international teams while maintaining the methodology's precision and clarity.