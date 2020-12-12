from IPython.display import HTML, display
def notebook_table(*headers):
    table = ['<tr>', *[f'<th style="text-align:left">{h}</th>' for h in headers], '</tr>']
    notebook_table.display = lambda: display(HTML(''.join(['<table>', *table, '</table>'])))
    item = 0
    def print_in_table(*values):
        nonlocal table, item
        for val in values:
            if item % len(headers) == 0: table += "<tr>"
            table += [f'<td style="text-align:left">{val}</td>']
            item += 1
            if item % len(headers) == 0: table += "</tr>"
    return print_in_table
