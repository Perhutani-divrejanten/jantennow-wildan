import os
import re
from pathlib import Path

print("🚀 Starting comprehensive JantenNow rebranding...")

# Define replacements
replacements = {
    # Logo replacements
    '<img src="img/warta jabar.png" alt="Warta Jabar">': '<span class="brand-logo">JantenNow</span>',
    '<img src="img/warta jabar.png">': '<span class="brand-logo">JantenNow</span>',
    
    # Footer and branding replacements
    'Warta Janten': 'JantenNow',
    'Warta Jabar': 'JantenNow',
    'warta jabar': 'JantenNow',
    'warta janten': 'JantenNow',
    
    # Email and contact replacements
    'redaksi@wartajanten.id': 'redaksi@jantennow.id',
    'privacy@wartajanten.id': 'privacy@jantennow.id',
    'info@wartajanten.id': 'info@jantennow.id',
    'kontak@wartajanten.id': 'kontak@jantennow.id',
}

# Title pattern replacements (more complex)
title_replacements = [
    (r'Portal Berita .* - Warta Janten', 'Portal Berita Jawa Barat & Banten - JantenNow'),
    (r'Portal Berita .* - Warta Jabar', 'Portal Berita Jawa Barat & Banten - JantenNow'),
    (r'(.+?) - Warta Janten', r'\1 - JantenNow'),
    (r'(.+?) - Warta Jabar', r'\1 - JantenNow'),
]

def process_file(file_path):
    """Process a single file with all replacements"""
    try:
        # Try UTF-8 first, then fall back to latin-1
        encoding = 'utf-8'
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
        except UnicodeDecodeError:
            encoding = 'latin-1'
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
        
        original_content = content
        
        # Apply simple replacements
        for old, new in replacements.items():
            content = content.replace(old, new)
        
        # Apply regex replacements for titles
        for pattern, replacement in title_replacements:
            content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
        
        # Only write if content changed
        if content != original_content:
            with open(file_path, 'w', encoding=encoding) as f:
                f.write(content)
            return True, encoding
        return False, encoding
    except Exception as e:
        return None, str(e)

# Process HTML files
html_files = list(Path('.').glob('*.html')) + list(Path('.').glob('*/*.html'))
updated_count = 0
error_count = 0

for file_path in sorted(html_files):
    result, info = process_file(file_path)
    if result is True:
        print(f"✅ Updated: {file_path}")
        updated_count += 1
    elif result is False:
        print(f"⊘ No changes: {file_path}")
    else:
        print(f"❌ Error in {file_path}: {info}")
        error_count += 1

print(f"\n📊 Summary:")
print(f"✅ Updated files: {updated_count}")
print(f"⊘ Unchanged: {len(html_files) - updated_count - error_count}")
print(f"❌ Errors: {error_count}")
