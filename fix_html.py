import os
import re
from pathlib import Path

html_files = list(Path('.').glob('*.html')) + list(Path('.').glob('**/*.html'))

for file in html_files:
    try:
        # Try UTF-8 first, then fall back to latin-1 for files like news.html
        encoding = 'utf-8'
        try:
            with open(file, 'r', encoding=encoding) as f:
                content = f.read()
        except UnicodeDecodeError:
            encoding = 'latin-1'
            with open(file, 'r', encoding=encoding) as f:
                content = f.read()
        
        # Fix double angle brackets in logo
        content = content.replace('<<span class="brand-logo">JantenNow</span>>', '<span class="brand-logo">JantenNow</span>')
        
        # Fix and remove duplicate CSS links (handle all variants)
        content = re.sub(
            r'<link href="css/style\.css" rel="stylesheet">[\r\n\s]*<link href="css/jantennow-enhancements\.css" rel="stylesheet">[\r\n\s]*<link href="css/jantennow-enhancements\.css" rel="stylesheet">', 
            '<link href="css/style.css" rel="stylesheet">\n        <link href="css/jantennow-enhancements.css" rel="stylesheet">', 
            content,
            flags=re.MULTILINE
        )
        
        # Remove backtick-r-backtick-n artifacts
        content = content.replace('`r`n', '\n')
        
        with open(file, 'w', encoding=encoding) as f:
            f.write(content)
        print(f'Fixed: {file} (encoding: {encoding})')
    except Exception as e:
        print(f'Error in {file}: {e}')

print('Done!')

