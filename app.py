from flask import Flask, render_template, request
from difflib import Differ
import html

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compare', methods=['POST'])
def compare():
    file1 = request.files['file1']
    file2 = request.files['file2']
    
    file1_content = file1.read().decode('utf-8')
    file2_content = file2.read().decode('utf-8')
    
    differ = Differ()
    result = list(differ.compare(file1_content.splitlines(keepends=True), file2_content.splitlines(keepends=True)))
    
    num_unchanged = 0
    num_file1_unique = 0
    num_file2_unique = 0
    
    for line in result:
        if line.startswith('  ') and not line.isspace():  # Check for unchanged lines excluding blanks
            num_unchanged += 1
        elif line.startswith('- '):
            num_file1_unique += 1
        elif line.startswith('+ '):
            num_file2_unique += 1
    
    html_content = f"""
    <div class="alert alert-info" role="alert">
        <strong>Comparison Summary:</strong>
        <ul>
            <li><strong>Unchanged lines:</strong> {num_unchanged}</li>
            <li><strong>File 1 unique lines:</strong> {num_file1_unique}</li>
            <li><strong>File 2 unique lines:</strong> {num_file2_unique}</li>
        </ul>
    </div>
    
    <table class="table table-bordered">
        <thead class="thead-dark">
            <tr>
                <th scope="col">Unchanged</th>
                <th scope="col">File 1</th>
                <th scope="col">File 2</th>
            </tr>
        </thead>
        <tbody>
    """
    
    for line in result:
        unchanged = ""
        file1_line = ""
        file2_line = ""
        if line.startswith('  ') and not line.isspace():  # Check unchanged lines excluding blanks
            unchanged = line.strip()
        elif line.startswith('- '):
            file1_line = line.strip()
        elif line.startswith('+ '):
            file2_line = line.strip()
        
        unchanged = html.escape(unchanged)
        file1_line = html.escape(file1_line)
        file2_line = html.escape(file2_line)
        
        html_content += f"""
        <tr>
            <td>{unchanged}</td>
            <td class="text-danger">{file1_line}</td>
            <td class="text-success">{file2_line}</td>
        </tr>
        """
    
    html_content += """
        </tbody>
    </table>
    """
    
    return html_content

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
