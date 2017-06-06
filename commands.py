SERVER = [
    # {
    #     'request': ['#C0*00'],
    #     'responseRegex': [r'\w*#P00\*\w*']
    # }
    {
        'request': '#C0*00',
        'responseRegex': r'\w*#P00\*\w*'
    }
]

CLIENT = {
    'remoteRequest': '#C0*00',
    'responseTemplate': '{}#P00*00'
}
