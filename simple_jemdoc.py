#!/usr/bin/env python3
import re
import os
import sys

def parse_menu_file():
    """Parse MENU file and return menu structure"""
    menu_items = []
    if os.path.exists('MENU'):
        with open('MENU', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        current_category = None
        for line in lines:
            line = line.rstrip()
            if not line:
                continue
            
            # Check if line contains a URL (menu item)
            if '[' in line and ']' in line:
                # Extract text and URL
                url_match = re.search(r'\[([^\]]+)\]', line)
                if url_match:
                    url = url_match.group(1)
                    text = re.sub(r'\s*\[[^\]]+\]', '', line).strip()
                    if current_category:
                        menu_items.append({
                            'type': 'item',
                            'category': current_category,
                            'url': url,
                            'text': text
                        })
            else:  # Category line
                current_category = line.strip()
                menu_items.append({
                    'type': 'category',
                    'name': current_category
                })
    
    return menu_items

def generate_menu_html(current_file, is_chinese=False):
    """Generate menu HTML based on MENU file"""
    menu_items = parse_menu_file()
    menu_html = []
    
    for item in menu_items:
        if item['type'] == 'category':
            # Show appropriate menu category based on language
            if item['name'] == 'Language':
                menu_html.append('<div class="menu-category">语言</div>' if is_chinese else '<div class="menu-category">Language</div>')
            elif is_chinese and item['name'] == '菜单':
                menu_html.append('<div class="menu-category">菜单</div>')
            elif not is_chinese and item['name'] == 'Menu':
                menu_html.append('<div class="menu-category">Menu</div>')
        else:
            # Show menu items based on language and category
            if item['category'] == 'Language':
                # For Language section, show the opposite language
                if is_chinese and item['text'] == 'English':
                    menu_html.append(f'<div class="menu-item"><a href="{item["url"]}">{item["text"]}</a></div>')
                elif not is_chinese and item['text'] == '中文':
                    menu_html.append(f'<div class="menu-item"><a href="{item["url"]}">{item["text"]}</a></div>')
            elif is_chinese and item['category'] == '菜单':
                # Show Chinese menu items for Chinese pages
                menu_html.append(f'<div class="menu-item"><a href="{item["url"]}">{item["text"]}</a></div>')
            elif not is_chinese and item['category'] == 'Menu':
                # Show English menu items for English pages
                menu_html.append(f'<div class="menu-item"><a href="{item["url"]}">{item["text"]}</a></div>')
    
    return '\n'.join(menu_html)

def convert_jemdoc_to_html(jemdoc_content, title="", current_file=""):
    is_chinese = '_cn.' in current_file
    menu_html = generate_menu_html(current_file, is_chinese)
    
    html_template = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
<head>
<meta name="generator" content="jemdoc, see http://jemdoc.jaboc.net/" />
<meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
<link rel="stylesheet" href="jemdoc.css" type="text/css" />
<title>{title}</title>
</head>
<body>
<table summary="Table for page layout." id="tlayout">
<tr valign="top">
<td id="layout-menu">
<div id="layout-menu-container">
{menu}
</div>
</td>
<td id="layout-content">
<div id="toptitle">
<h1>{title}</h1>
</div>
{content}
</td>
</tr>
</table>
</body>
</html>"""
    
    content = jemdoc_content
    
    # Extract title
    title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
    if title_match:
        page_title = title_match.group(1)
        content = re.sub(r'^# (.+)$', '', content, flags=re.MULTILINE)
    else:
        page_title = title
    
    # Convert sections
    content = re.sub(r'^== (.+)$', r'<h2>\1</h2>', content, flags=re.MULTILINE)
    content = re.sub(r'^=== (.+)$', r'<h3>\1</h3>', content, flags=re.MULTILINE)
    
    # Handle bold text
    content = re.sub(r'\*([^*\n]+)\*', r'<b>\1</b>', content)
    
    # Handle italic text  
    content = re.sub(r'/([^/\n]+)/', r'<i>\1</i>', content)
    
    # Handle links
    content = re.sub(r'\[([^\]]+) ([^\]]+)\]', r'<a href="\1">\2</a>', content)
    
    # Handle email obfuscation
    content = re.sub(r'([a-zA-Z0-9._%+-]+) \\?\[@\\?\] ([a-zA-Z0-9.-]+)', r'\1@\2', content)
    
    # Handle line breaks
    content = re.sub(r' \\n', '<br/>', content)
    
    # Handle image blocks with ~~~ syntax (after text processing)
    content = re.sub(r'~~~\s*\n\{\}\{img_left\}\{([^}]+)\}\{[^}]*\}\{(\d+)\}\{(\d+)\}\s*\n(.*?)\n~~~', 
                    r'<table class="imgtable"><tr><td><img src="\1" alt="photo" width="\2px" height="\3px" /></td><td align="left">\4</td></tr></table>', 
                    content, flags=re.DOTALL)
    
    # Process lines
    lines = content.split('\n')
    result_lines = []
    in_ordered_list = False
    in_unordered_list = False
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        if not line:
            if in_ordered_list:
                result_lines.append('</ol>')
                in_ordered_list = False
            if in_unordered_list:
                result_lines.append('</ul>')
                in_unordered_list = False
            result_lines.append('')
            i += 1
            continue
            
        # Handle ordered lists
        if re.match(r'^\d+\. ', line):
            if not in_ordered_list:
                if in_unordered_list:
                    result_lines.append('</ul>')
                    in_unordered_list = False
                result_lines.append('<ol>')
                in_ordered_list = True
            result_lines.append('<li>' + re.sub(r'^\d+\. ', '', line) + '</li>')
        # Handle unordered lists
        elif re.match(r'^- ', line):
            if not in_unordered_list:
                if in_ordered_list:
                    result_lines.append('</ol>')
                    in_ordered_list = False
                result_lines.append('<ul>')
                in_unordered_list = True
            result_lines.append('<li>' + line[2:] + '</li>')
        # Handle nested unordered lists (-- items)
        elif re.match(r'^  -- ', line):
            if in_unordered_list:
                # Add as nested list item with proper indentation
                result_lines.append('<ul><li>' + line[5:] + '</li></ul>')
            else:
                result_lines.append('<p>' + line + '</p>')
        # Handle headers (already converted above)
        elif line.startswith('<h'):
            if in_ordered_list:
                result_lines.append('</ol>')
                in_ordered_list = False
            if in_unordered_list:
                result_lines.append('</ul>')
                in_unordered_list = False
            result_lines.append(line)
        # Handle image table
        elif line.startswith('<table class="imgtable"'):
            if in_ordered_list:
                result_lines.append('</ol>')
                in_ordered_list = False
            if in_unordered_list:
                result_lines.append('</ul>')
                in_unordered_list = False
            result_lines.append(line)
        # Regular paragraphs
        else:
            if in_ordered_list:
                result_lines.append('</ol>')
                in_ordered_list = False
            if in_unordered_list:
                result_lines.append('</ul>')
                in_unordered_list = False
            if line:
                result_lines.append('<p>' + line + '</p>')
        
        i += 1
    
    # Close any remaining lists
    if in_ordered_list:
        result_lines.append('</ol>')
    if in_unordered_list:
        result_lines.append('</ul>')
    
    content = '\n'.join(result_lines)
    
    return html_template.format(title=page_title, content=content, menu=menu_html)

def main():
    # 处理命令行参数
    if len(sys.argv) > 1:
        jemdoc_file = sys.argv[1]
        
        # 检查是否指定了输出文件名
        output_file = None
        if len(sys.argv) > 3 and sys.argv[2] == '-o':
            output_file = sys.argv[3]
        
        if os.path.exists(jemdoc_file):
            with open(jemdoc_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            html_file = output_file if output_file else jemdoc_file.replace('.jemdoc', '.html')
            html_content = convert_jemdoc_to_html(content, current_file=html_file)
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"Converted {jemdoc_file} to {html_file}")
    else:
        # 默认处理这些文件
        jemdoc_files = ['index.jemdoc', 'research.jemdoc', 'publications.jemdoc', 'teaching.jemdoc', 'people.jemdoc', 
                        'joinus.jemdoc', 'contact.jemdoc', 'index_cn.jemdoc', 'research_cn.jemdoc', 'publications_cn.jemdoc', 
                        'teaching_cn.jemdoc', 'people_cn.jemdoc', 'joinus_cn.jemdoc', 'contact_cn.jemdoc']
        
        for jemdoc_file in jemdoc_files:
            if os.path.exists(jemdoc_file):
                with open(jemdoc_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                html_file = jemdoc_file.replace('.jemdoc', '.html')
                html_content = convert_jemdoc_to_html(content, current_file=html_file)
                
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                print(f"Converted {jemdoc_file} to {html_file}")

if __name__ == "__main__":
    main()