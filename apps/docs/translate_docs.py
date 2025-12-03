import os
import re
import time
from typing import List, Dict
import subprocess

def find_files_needing_translation() -> List[str]:
    """Find all markdown files that need translation"""
    files_to_translate = []

    # Search in target directories
    target_dirs = ['01-app', '02-pages', '03-architecture', '04-community']
    base_path = 'D:/code/mycode/next.js-canary/docs'

    for target_dir in target_dirs:
        dir_path = os.path.join(base_path, target_dir)
        if os.path.exists(dir_path):
            for root, dirs, files in os.walk(dir_path):
                for file in files:
                    if file.endswith(('.md', '.mdx')):
                        file_path = os.path.join(root, file)
                        # Check if file has English title (needs translation)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                # Look for English title in front matter
                                if re.search(r'^title:\s*[a-zA-Z]', content, re.MULTILINE):
                                    files_to_translate.append(file_path)
                        except Exception as e:
                            print(f"Error reading {file_path}: {e}")

    return files_to_translate

def translate_front_matter(content: str) -> str:
    """Translate front matter metadata"""
    # Common translations for front matter fields
    translations = {
        'title:': 'title:',
        'description:': 'description:',
        'nav_title:': 'nav_title:',
        'related:': 'related:',
        'source:': 'source:',
        'showMetadata:': 'showMetadata:',
        'hideMetadata:': 'hideMetadata:',
    }

    # Split content into lines for processing
    lines = content.split('\n')
    in_front_matter = False
    translated_lines = []

    for i, line in enumerate(lines):
        if line.strip() == '---':
            in_front_matter = not in_front_matter
            translated_lines.append(line)
            continue

        if in_front_matter:
            # Check if line starts with a translatable field
            for eng_key, chn_key in translations.items():
                if line.startswith(eng_key):
                    # Extract the value after the colon
                    if ':' in line:
                        key_part, value_part = line.split(':', 1)
                        value_part = value_part.strip()

                        # Skip if already translated (contains Chinese)
                        if re.search(r'[\u4e00-\u9fff]', value_part):
                            translated_lines.append(line)
                            break

                        # For now, just keep the original - we'll manually review these
                        translated_lines.append(line)
                        break
                    else:
                        translated_lines.append(line)
                        break
            else:
                translated_lines.append(line)
        else:
            # Not in front matter, keep original for now
            translated_lines.append(line)

    return '\n'.join(translated_lines)

def translate_content(content: str) -> str:
    """Translate main content while preserving code blocks and special syntax"""
    # For now, return original content as this would need proper translation service
    # This is a placeholder for the actual translation logic
    return content

def process_file(file_path: str) -> bool:
    """Process a single file for translation"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if already translated
        if re.search(r'^title:\s*[\u4e00-\u9fff]', content, re.MULTILINE):
            print(f"Already translated: {file_path}")
            return True

        print(f"Processing: {file_path}")

        # Translate front matter
        translated_content = translate_front_matter(content)

        # Translate main content (placeholder)
        translated_content = translate_content(translated_content)

        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(translated_content)

        return True

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Main translation function"""
    print("Finding files that need translation...")
    files_to_translate = find_files_needing_translation()

    print(f"Found {len(files_to_translate)} files to translate")

    # Process files in batches
    batch_size = 10
    total_processed = 0
    successful = 0
    failed = []

    for i in range(0, len(files_to_translate), batch_size):
        batch = files_to_translate[i:i+batch_size]
        print(f"\nProcessing batch {i//batch_size + 1}/{(len(files_to_translate)-1)//batch_size + 1}")

        for file_path in batch:
            if process_file(file_path):
                successful += 1
            else:
                failed.append(file_path)
            total_processed += 1

            # Progress indicator
            if total_processed % 5 == 0:
                print(f"Progress: {total_processed}/{len(files_to_translate)}")

    # Summary
    print(f"\n=== Translation Summary ===")
    print(f"Total files processed: {total_processed}")
    print(f"Successful: {successful}")
    print(f"Failed: {len(failed)}")

    if failed:
        print("Failed files:")
        for file_path in failed:
            print(f"  - {file_path}")

if __name__ == "__main__":
    main()