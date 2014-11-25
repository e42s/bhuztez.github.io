#include <boost/asio.hpp>
namespace asio = boost::asio;
using asio::ip::tcp;
#include <boost/bind.hpp>
#include <boost/shared_ptr.hpp>
#include <boost/enable_shared_from_this.hpp>


class session 
	: public boost::enable_shared_from_this<session>
{
public:
	session(asio::io_service& io)
		: socket_(io)
	{ }

	tcp::socket& socket()
	{ return socket_; }

	void start()
	{
		asio::async_write(socket_, asio::buffer(output_buffer_, 12), boost::bind(&session::handle_write, shared_from_this(), _1, _2));
	}

	void handle_write(const boost::system::error_code& ec, std::size_t bytes_transfered)
	{
		if(!ec) 
		{
			asio::async_read(socket_, asio::buffer(input_buffer_, 12), boost::bind(&session::handle_read, shared_from_this(), _1, _2));
		} else {
			std::cerr << "write error:" << ec.message() << std:: endl;
		}
	}

	void handle_read(const boost::system::error_code& ec, std::size_t bytes_transfered)
	{
		if(ec)
		{
			std::cerr << "read error:" << ec.message() << std::endl;
		}
	}

private:
	tcp::socket socket_;
	char output_buffer_[12];
	char input_buffer_[12];
};


void handle_connect(boost::shared_ptr<session> session_ptr, const boost::system::error_code& ec)
{
	if(ec) 
	{
		std::cerr << "connect error:" << ec.message() << std::endl;
	} else {
		session_ptr->start();
	}
}


int main(int argc, char* argv[])
{
	asio::io_service io;
	tcp::resolver resolver(io);
	tcp::resolver::iterator endpoint = resolver.resolve(tcp::resolver::query("localhost", argv[1]));
	boost::shared_ptr<session> session_ptr;
	for(int i = 0; i < 4000; i++)
	{
		session_ptr.reset(new session(io));
		asio::async_connect(session_ptr->socket(), endpoint, boost::bind(handle_connect, session_ptr, _1));
	}
	io.run();
}
