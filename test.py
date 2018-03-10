


host_list_dit = {
    'lifeson':
        {
            'basic_info': {'product': ' PowerEdge 2970'},
            'disk_list':
                {'disk': '100.2', 'diskused': '5.6', 'diskfree': '97.1'},
            'ram_list':
                {'ram': '31', 'ramused': '2', 'ramfree': '27'},
            'cpu_list':
                {'cpuname': 'Quad-Core AMD Opteron(tm) Processor 2374 HE', 'physicalcpu': '2', 'cpucores': '4',
                 'virtualcpu': '8'},
            'diskusedwidth': 5,
            'diskfreewidth': 96,
            'ramusedwidth': 6,
            'ramfreewidth': 87
        },

    'vanhalen':
        {
            'basic_info':
                {'product': ' PowerEdge R515'},
            'disk_list':
                {'disk': '1057.9', 'diskused': '425.9', 'diskfree': '660.9'},
            'ram_list':
                {'ram': '62', 'ramused': '61', 'ramfree': '1'},
            'cpu_list': {'cpuname': 'AMD Opteron(tm) Processor 4280                 ', 'physicalcpu': '2',
                         'cpucores': '4', 'virtualcpu': '16'},
            'diskusedwidth': 40,
            'diskfreewidth': 62,
            'ramusedwidth': 98,
            'ramfreewidth': 1
        },

    'clapton':
        {
            'basic_info': {'product': ' PowerEdge R515'},
            'disk_list': {'disk': '1175.3', 'diskused': '473.3', 'diskfree': '781.7'},
            'ram_list': {'ram': '56', 'ramused': '14', 'ramfree': '0'},
            'cpu_list': {'cpuname': 'AMD Opteron(tm) Processor 4280', 'physicalcpu': '2', 'cpucores': '4',
                         'virtualcpu': '16'},
            'diskusedwidth': 40,
            'diskfreewidth': 56,
            'ramusedwidth': 22,
            'ramfreewidth': 0
        },
    'a':
        {
            'basic_info': {'product': ' PowerEdge R515'},
            'disk_list': {'disk': '1175.3', 'diskused': '473.3', 'diskfree': '781.7'},
            'ram_list': {'ram': '2', 'ramused': '14', 'ramfree': '0'},
            'cpu_list': {'cpuname': 'AMD Opteron(tm) Processor 4280', 'physicalcpu': '2', 'cpucores': '4',
                         'virtualcpu': '16'},
            'diskusedwidth': 40,
            'diskfreewidth': 56,
            'ramusedwidth': 22,
            'ramfreewidth': 0
        },
    'b':
        {
            'basic_info': {'product': ' PowerEdge R515'},
            'disk_list': {'disk': '1175.3', 'diskused': '473.3', 'diskfree': '781.7'},
            'ram_list': {'ram': '99', 'ramused': '14', 'ramfree': '0'},
            'cpu_list': {'cpuname': 'AMD Opteron(tm) Processor 4280', 'physicalcpu': '2', 'cpucores': '4',
                         'virtualcpu': '16'},
            'diskusedwidth': 40,
            'diskfreewidth': 56,
            'ramusedwidth': 22,
            'ramfreewidth': 0
        }

}

host_list_ram = sorted([(int(v['ram_list']['ram'])) for k, v in host_list_dit.items()])

print(host_list_ram)

new_host_list = []
cont = 0

for ram in host_list_ram:
    for k, v in host_list_dit.items():
        if int(v['ram_list']['ram']) == ram:
            new_host_list.insert(cont, (k, v))
            cont += 1
            continue

for i in new_host_list:
    print(i)

print(111111111111111)

from collections import OrderedDict

b = OrderedDict(sorted(host_list_dit.items(), key=lambda t: t[1]['ram_list']['ram']))
print(b)
