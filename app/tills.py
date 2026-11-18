def net_sales(sales, refunds, event):
    result = {sale['id']: sale['cents'] for sale in sales if sale['event'] == event}
    for refund in refunds:
        if refund['sale'] in result:
            result[refund['sale']] -= refund['cents']
            if result[refund['sale']] < 0:
                raise ValueError('累计退款超过原单金额')
    return result
