#include <iostream>
#include <string>

using namespace std;

class Mediator;

class Person
{
    public:
        virtual void setMediator(Mediator* mediator){};
        virtual void sendMessage(string msg)  = 0;
        virtual void getMessage(){};
    protected:
        Mediator *m_mediator;
};

class Mediator
{
    public:
        virtual void setHost(Person* p) = 0;
        virtual void setClient(Person* p) = 0;
        virtual void sendMsg(Person* p, string msg)
        {
        }
};

class HouseMediator::public Mediator
{
    public:
        void setHost(Person* p)
        {
            m_host = p;
        }
        void setClient(Person* p)
        {
            m_client = p;
        }
        void sendMsg(Person* p, string msg)
        {
            if(p == m_host)
            {
                m_client->getMessage();
            }
            else
            {
                m_host->getMessage();
            }
        }
    private:
        Person* m_host;
        Person* m_client;
};

class HostPerson: public Person
{
    public:
        void setMediator(Mediator* mediator)
        {
            m_mediator = mediator;
        }
        void sendMessage(string msg)
        {
            m_mediator->sendMsg(this, msg);
        }
        void getMessage(string msg)
        {
            cout << "房东收到消息！"  << endl;
        }
};

class ClientPerson:public Person
{
    public:
        void setMediator(Mediator* mediator)
        {
            m_mediator = mediator;
        }
        void sendMessage(string msg)
        {
            m_mediator->sendMsg(this, msg);
        }
        void getMessage(string msg)
        {
            cout << "客户收大消息！" << endl;
        }
};

int main()
{
    HouseMediator *mediator = new HouseMediator();
    HostPerson *host = new HostPerson();
    host->setMediator(mediator);
    ClientPerson *client = new ClientPerson();
    client->setMediator(mediator);
    mediator->setClient(client);
    mediator->setHost(host);
    client->sendMessage("我要租房子！");
    host->sendMessage("有房子要出租！");

    return 0;
}
