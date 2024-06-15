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
    
    # Split and filter out empty or whitespace-only lines
    file1_lines = [line for line in file1_content.splitlines(keepends=True) if line.strip()]
    file2_lines = [line for line in file2_content.splitlines(keepends=True) if line.strip()]
    
    differ = Differ()
    result = list(differ.compare(file1_lines, file2_lines))
    
    num_unchanged = 0
    num_file1_unique = 0
    num_file2_unique = 0
    
    for line in result:
        if line.startswith('  '):  # Check for unchanged lines
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
    
    <div id="comparisonResult">
        <input type="text" id="searchInput" class="form-control mt-3 mb-3" placeholder="Search diff to see affected lines...">
    <table class="table table-bordered">
            <thead class="thead-dark">
                <tr>
                    <th scope="col" id="unchangedHeader">Unchanged</th>
                    <th scope="col" id="file1Header">File 1</th>
                    <th scope="col" id="file2Header">File 2</th>
                </tr>
            </thead>
            <tbody>
    """
    
    for index, line in enumerate(result):
        unchanged = ""
        file1_line = ""
        file2_line = ""
        if line.startswith('  '):  # Check unchanged lines
            unchanged = line.strip()
        elif line.startswith('- '):
            file1_line = "diff1: " + line.strip()
        elif line.startswith('+ '):
            file2_line = "diff2: " + line.strip()
        
        unchanged = html.escape(unchanged)
        file1_line = html.escape(file1_line)
        file2_line = html.escape(file2_line)
        
        html_content += f"""
        <tr id="row_{index}">
            <td>{unchanged}</td>
            <td class="text-danger">{file1_line}</td>
            <td class="text-success">{file2_line}</td>
        </tr>
        """
    
    html_content += """
            </tbody>
        </table>
    </div>
    
    <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
    <script>
        $(document).ready(function () {
            $('#searchInput').keyup(function () {
                var searchText = $(this).val().toLowerCase();
        
                $('tbody tr').each(function () {
                    var unchangedText = $(this).find('td:nth-child(1)').text().toLowerCase();
                    var file1Text = $(this).find('td:nth-child(2)').text().toLowerCase();
                    var file2Text = $(this).find('td:nth-child(3)').text().toLowerCase();
        
                    if (unchangedText.indexOf(searchText) === -1 &&
                        file1Text.indexOf(searchText) === -1 &&
                        file2Text.indexOf(searchText) === -1) {
                        $(this).hide();
                    } else {
                        $(this).show();
                    }
                });
            });
        });
    </script>
    """
    
    return html_content

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
