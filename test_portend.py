import socket

import pytest

import portend


def socket_infos():
	"""
	Generate addr infos for connections to localhost
	"""
	host = ''
	port = portend.find_available_local_port()
	family = getattr(socket, 'AF_UNSPEC', socket.AF_INET)
	return socket.getaddrinfo(host, port, family, socket.SOCK_STREAM)


def id_for_info(info):
	af, = info[:1]
	return str(af)

def build_addr_infos():
	params = list(socket_infos())
	ids = list(map(id_for_info, params))
	return locals()


@pytest.fixture(**build_addr_infos())
def listening_addr(request):
	af, socktype, proto, canonname, sa = request.param
	sock = socket.socket(af, socktype, proto)
	sock.bind(sa)
	sock.listen(5)
	try:
		yield sa
	finally:
		sock.close()


@pytest.fixture(**build_addr_infos())
def nonlistening_addr(request):
	af, socktype, proto, canonname, sa = request.param
	return sa


class TestCheckPort:
	def test_check_port_listening(self, listening_addr):
		with pytest.raises(IOError):
			portend._check_port(*listening_addr[:2])

	def test_check_port_nonlistening(self, nonlistening_addr):
		portend._check_port(*nonlistening_addr[:2])
