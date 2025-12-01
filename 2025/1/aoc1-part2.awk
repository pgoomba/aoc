#!/usr/bin/env gawk -f

BEGIN {
    crosses = 0;
    pos = 50;
}

/^L.*/ { direction = -1; }
/^R.*/ { direction = 1; }

function mod(a, b) {
    # (╯°□°)╯︵ ┻━┻ - AWK mod returns negative numbers
    r = a % b
    if (r < 0) r += (b > 0 ? b : -b)
    return r
}

/^[RL]/ {
    if (match($0, /^[RL](.*)$/, m)) {
        steps = m[1]
        crosses += int((((direction > 0) ? pos : mod(100-pos, 100)) + steps) / 100)
        pos = mod(pos + direction*steps, 100)
    }
}

END {
    print crosses
}