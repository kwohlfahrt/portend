portend
=======

por·tend
pôrˈtend/
verb

    be a sign or warning that (something, especially something momentous or calamitous) is likely to happen.

Usage
-----

Use portend to monitor TCP ports for bound or unbound states.

For example, to wait for a port to be occupied, timing out after 3 seconds:

    portend.occupied('www.google.com', 80, timeout=3)

Or to wait for a port to be free, timing out after 5 seconds:

    portend.free('::1', 80, timeout=5)
