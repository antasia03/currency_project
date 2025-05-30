import requests
from django.shortcuts import render

def currency_rates(request):
    """
    Обрабатывает запросы к странице с курсами валют,
    поиском по коду валюты и конвертером валют.
    """
    url = 'https://api.nbrb.by/exrates/rates?periodicity=0'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException:
        data = []

    needed = ['USD', 'EUR', 'RUB']
    filtered = [item for item in data if item['Cur_Abbreviation'] in needed]

    query = request.GET.get('code', '').upper()
    search_result = None

    if query:
        search_result = next(
            (item for item in data if item['Cur_Abbreviation'] == query),
            None
        )

    amount = request.GET.get('amount')
    from_currency = request.GET.get('from_currency')
    to_currency = request.GET.get('to_currency')
    conversion_result = None

    if amount and from_currency and to_currency:
        try:
            amount = float(amount)
            from_rate = next(
                (item for item in data if item['Cur_Abbreviation'] == from_currency),
                None
            )
            to_rate = next(
                (item for item in data if item['Cur_Abbreviation'] == to_currency),
                None
            )
            if from_rate and to_rate:
                amount_in_byn = amount * from_rate['Cur_OfficialRate'] / from_rate['Cur_Scale']
                result = amount_in_byn * to_rate['Cur_Scale'] / to_rate['Cur_OfficialRate']
                conversion_result = f"{amount} {from_currency} = {round(result, 4)} {to_currency}"
        except Exception:
            conversion_result = "Ошибка при конвертации."

    context = {
        'rates': filtered,
        'all_rates': data,
        'search_result': search_result,
        'query': query,
        'conversion_result': conversion_result
    }
    return render(request, 'currency_rates.html', context)
