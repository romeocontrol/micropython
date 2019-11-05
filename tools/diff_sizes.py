#!/usr/bin/env python
# to compute the difference in sizes from the output of build_ports.sh

import sys, re

def parse_input(filename):
    data = dict()
    lines = []
    found_sizes = False
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line.strip() == 'COMPUTING SIZES':
                found_sizes = True
            elif found_sizes:
                lines.append(line)
    is_size_line = False
    for line in lines:
        if is_size_line:
            fields = line.split()
            data[fields[-1]] = [int(f) for f in fields[:-2]]
            is_size_line = False
        else:
            is_size_line = line.startswith('text\t ')
    return data

if len(sys.argv) != 3:
    print('usage: %s <out1> <out2>' % sys.argv[0])
    raise SystemExit(1)

data1 = parse_input(sys.argv[1])
data2 = parse_input(sys.argv[2])

pretty_name = {
    'ports/bare-arm/build/firmware.elf':'bare-arm',
    'ports/minimal/build/firmware.elf':'minimal x86',
    'ports/unix/micropython':'unix x64',
    'ports/unix/micropython_nanbox':'unix nanbox',
    'ports/stm32/build-PYBV10/firmware.elf':'stm32',
    'ports/cc3200/build/WIPY/release/application.axf':'cc3200',
    'ports/esp8266/build-GENERIC/firmware.elf':'esp8266',
    'ports/esp32/build-GENERIC/application.elf':'esp32',
    'ports/nrf/build-pca10040/firmware.elf':'nrf',
    'ports/samd/build-ADAFRUIT_ITSYBITSY_M4_EXPRESS/firmware.elf':'samd',
}

for key, value1 in data1.items():
    value2 = data2[key]
    name = pretty_name[key]
    data = [v2 - v1 for v1, v2 in zip(value1, value2)]
    warn = ''
    board = re.search(r'/build-([A-Za-z0-9_]+)/', key)
    if board:
        board = board.group(1)
    else:
        board = ''
    if name == 'cc3200':
        delta = data[0]
        percent = 100 * delta / value1[0]
        if data[1] != 0:
            warn += ' %+u(data)' % data[1]
    else:
        delta = data[3]
        percent = 100 * delta / value1[3]
        if data[1] != 0:
            warn += ' %+u(data)' % data[1]
        if data[2] != 0:
            warn += ' %+u(bss)' % data[2]
    if warn:
        warn = '[incl%s]' % warn
    print('%11s: %+5u %+.3f%% %s%s' % (name, delta, percent, board, warn))
