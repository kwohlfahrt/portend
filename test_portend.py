import socket

import pytest

import portend


def socket_infos():
	"""
	Generate addr infos for connections to localhost
	"""
	host = ''
	port = portend.find_available_local_port()
	infos = socket.getaddrinfo(host, port, socket.AF_UNSPEC, socket.SOCK_STREAM)
	for info in infos:
		yield host, port, info


@pytest.fixture(params=list(socket_infos()))
def listening_addr(request):
	host, port, info = request.param
	af, socktype, proto, canonname, sa = info
	sock = socket.socket(af, socktype, proto)
	sock.bind(sa)
	sock.listen(5)
	try:
		yield sa
	finally:
		sock.close()


class TestCheckPort:
	def test_check_port_listening(self, listening_addr):
		with pytest.raises(IOError):
			portend._check_port(*listening_addr[:2])
