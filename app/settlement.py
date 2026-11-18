from .calendar import billable
from .tills import net_sales


def statement(source, event):
    if not billable(event):
        raise ValueError('未实际举办的活动不能结算')
    sales = net_sales(source['sales'], source['refunds'], event['id'])
    return {'venue': event['venue'], 'sales': sales,
            'fee_cents': sum(sales.values()) * source['terms']['venue_percent'] // 100}
