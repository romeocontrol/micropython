#!/bin/sh

OPT="-j3 CFLAGS_EXTRA=-DNDEBUG"

function get_port_data() {
    port_dir=""
    port_flags=""
    port_output=""
    case $1 in
        b) port_dir=bare-arm port_output=build/firmware.elf ;;
        m) port_dir=minimal; port_output=build/firmware.elf ;;
        u) port_dir=unix; port_output=micropython ;;
        n) port_dir=unix; port_flags=nanbox; port_output=micropython_nanbox ;;
        s) port_dir=stm32; port_output=$(ls -trd ports/stm32/build-* | tail -n1 | cut -d / -f 3)/firmware.elf ;;
        c) port_dir=cc3200; port_flags=BTARGET=application; port_output=build/WIPY/release/application.axf ;;
        8) port_dir=esp8266; port_output=build-GENERIC/firmware.elf ;;
        3) port_dir=esp32; port_output=build-GENERIC/application.elf ;;
        r) port_dir=nrf; port_output=build-pca10040/firmware.elf ;;
        d) port_dir=samd; port_output=build-ADAFRUIT_ITSYBITSY_M4_EXPRESS/firmware.elf ;;
    esac
}

clean=false
if [ "$1" = "-c" ]; then
    clean=true
    shift 1
fi

port_chars_cmdline="bmu"
if [ $# -gt 0 ]; then
    if [ "$1" = "all" ]; then
        port_chars_cmdline="bmunsc83rd"
    else
        port_chars_cmdline=$1
    fi
    shift 1
fi

port_chars=""
for (( i=0; i<${#port_chars_cmdline}; i++ )); do
    port_char=${port_chars_cmdline:$i:1}
    get_port_data $port_char
    if [ "$port_dir" = "" ]; then
        echo "unknown port character: $port_char"
        exit 1
    fi
    port_chars="$port_chars $port_char"
done

if $clean; then
    echo "CLEANING FIRST"
    for port_char in $port_chars; do
        get_port_data $port_char
        make -C ports/$port_dir $port_flags clean || exit 1
    done
fi

echo "BUILDING MPY-CROSS"
make -C mpy-cross $OPT || exit 1

echo "BUILDING PORTS"
for port_char in $port_chars; do
    get_port_data $port_char
    if [ $port_char = u ]; then
        make -C ports/unix $OPT axtls || exit 1
    fi
    make -C ports/$port_dir $OPT $port_flags || exit 1
done

echo "COMPUTING SIZES"
for port_char in $port_chars; do
    get_port_data $port_char
    size ports/$port_dir/$port_output
done
