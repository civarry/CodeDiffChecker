from difflib import Differ

file1_path = "main/utils.py"
file2_path = "index/utils.py"

# Read files from the paths
with open(file1_path, 'r', encoding='utf-8') as file1, open(file2_path, 'r', encoding='utf-8') as file2:
    file1_content = file1.readlines()
    file2_content = file2.readlines()

differ = Differ()
result = list(differ.compare(file1_content, file2_content))

# Initialize counts for summary
num_unchanged = 0
num_original_only = 0
num_updated_only = 0

# Generate the summary and count lines
for line in result:
    if line.startswith('  '):  # lines that are unchanged
        num_unchanged += 1
    elif line.startswith('- '):  # lines that are only in the original file
        num_original_only += 1
    elif line.startswith('+ '):  # lines that are only in the updated file
        num_updated_only += 1

# Create the HTML content with file names and paths
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Comparison Result</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #24292e;
        }}
        .container {{
            margin: 0 auto;
            padding: 20px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }}
        th, td {{
            border: 1px solid #dfe2e5;
            padding: 8px;
            text-align: left;
        }}
        th {{
            background-color: #f6f8fa;
            font-weight: bold;
        }}
        .green {{
            color: green;
        }}
        .red {{
            color: red;
        }}
        .summary {{
            background-color: #f1f8ff;
            border: 1px solid #c8e1ff;
            border-radius: 3px;
            padding: 10px;
            margin-bottom: 20px;
        }}
        .summary h3 {{
            margin-top: 0;
            font-size: 1.2em;
            font-weight: bold;
            color: #0366d6;
        }}
        .summary ul {{
            list-style-type: none;
            padding: 0;
        }}
        .summary li {{
            margin-bottom: 5px;
        }}
        .summary li strong {{
            display: inline-block;
            width: 150px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>File Comparison Result</h1>

        <div class="summary">
            <h3>Summary</h3>
            <ul>
                <li><strong>Unchanged lines:</strong> {num_unchanged}</li>
                <li><strong>{file1_path} lines:</strong> {num_original_only}</li>
                <li><strong>{file2_path} lines:</strong> {num_updated_only}</li>
            </ul>
        </div>

        <table>
            <thead>
                <tr>
                    <th>Unchanged</th>
                    <th>{file1_path} Only</th>
                    <th>{file2_path} Only</th>
                </tr>
            </thead>
            <tbody>
"""

# Add rows to the table
for line in result:
    if line.startswith('  '):  # lines that are unchanged
        unchanged = line.strip()
        original_only = ""
        updated_only = ""
    elif line.startswith('- '):  # lines that are only in the original file
        unchanged = ""
        original_only = line.strip()
        updated_only = ""
    elif line.startswith('+ '):  # lines that are only in the updated file
        unchanged = ""
        original_only = ""
        updated_only = line.strip()
    else:
        continue
    
    html_content += f"""
            <tr>
                <td>{unchanged}</td>
                <td><span class="red">{original_only}</span></td>
                <td><span class="green">{updated_only}</span></td>
            </tr>
    """

# Complete the HTML content
html_content += """
            </tbody>
        </table>
    </div>
</body>
</html>
"""

# Save the result as an HTML file
html_file_path = "comparison_result.html"
with open(html_file_path, 'w', encoding='utf-8') as html_file:
    html_file.write(html_content)

print(f"Comparison result saved as {html_file_path}")
