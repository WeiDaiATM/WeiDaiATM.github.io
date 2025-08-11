#!/usr/bin/env python3
import re
import os
import sys

def convert_jemdoc_to_html(jemdoc_content, title=""):
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
<div class="menu-category">Menu</div>
<div class="menu-item"><a href="index.html">Home</a></div>
<div class="menu-item"><a href="research.html">Research</a></div>
<div class="menu-item"><a href="publications.html">Publications</a></div>
<div class="menu-item"><a href="teaching.html">Teaching</a></div>
<div class="menu-item"><a href="contact.html">Contact</a></div>
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
    
    # Handle image blocks (profile photo)
    content = re.sub(r'~~~\s*\{[^}]*\}\{img_left\}\{([^}]+)\}[^~]*~~~([^~]*)~~~', 
                    r'<table class="imgtable"><tr><td><img src="\1" alt="photo" width="131px" height="160px" /></td><td align="left">\2</td></tr></table>', 
                    content, flags=re.DOTALL)
    
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
    
    return html_template.format(title=page_title, content=content)

def main():
    jemdoc_files = ['index.jemdoc', 'research.jemdoc', 'publications.jemdoc', 'teaching.jemdoc', 'contact.jemdoc']
    
    for jemdoc_file in jemdoc_files:
        if os.path.exists(jemdoc_file):
            with open(jemdoc_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            html_content = convert_jemdoc_to_html(content)
            html_file = jemdoc_file.replace('.jemdoc', '.html')
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"Converted {jemdoc_file} to {html_file}")

if __name__ == "__main__":
    main()