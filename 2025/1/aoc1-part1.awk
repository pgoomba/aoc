#!/usr/bin/env gawk -f

BEGIN {
    zero = 0;
    pos = 50;
    sign = 1;
}

/^L.*/ { sign = -1; }
/^R.*/ { sign = 1; }

/^[RL]/ {
    if (match($0, /^[RL](.*)$/, m)) {
        pos = (pos + sign * m[1]) % 100
        if (pos == 0) {
            zero++;
        }
    }
}

END {
    print zero
}