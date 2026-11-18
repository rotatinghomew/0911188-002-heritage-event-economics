import json
from .calendar import lookup
from .journal import packet
from .settlement import statement
from .tills import net_sales


def run_workbench(action, directory, key, ledger):
    selected = key or 'harbor-fair'
    if action == 'receipts':
        return packet(ledger, 'settlement', selected)
    source = json.loads((directory / 'workbench.json').read_text())
    event = lookup(source['events'], selected)
    if action == 'calendar':
        return event
    if action == 'turnover':
        return net_sales(source['sales'], source['refunds'], selected)
    return packet(ledger, 'settlement', selected, statement(source, event))
