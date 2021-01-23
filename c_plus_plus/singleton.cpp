#include <iostream>
#include <memory>
#include <mutex>

using namespace std;

class Singleton{
    private:
        int n = 0;
        Singleton(){
            cout << "constructor called!" << endl;
        }
        Singleton(Singleton&)=delete;
        Singleton& operator=(const Singleton&)=delete;
        static Singleton* m_instance_ptr;
        static std::mutex m_mutex;
    public:
        ~Singleton(){
            n = 0;
            cout << "destructor called!" << endl;
        }
        static Singleton* get_instance();
        void use() {
            cout << "in use: " << n << endl;
            n += 1;
        }
};

Singleton* Singleton::get_instance(){
    if(m_instance_ptr == nullptr)
    {
        std::lock_guard<std::mutex> lk(m_mutex);
        if(m_instance_ptr == nullptr){
            m_instance_ptr = new Singleton;
        }
    }
    return m_instance_ptr;
}
Singleton* Singleton::m_instance_ptr = nullptr;
std::mutex Singleton::m_mutex;
int main(void){
    Singleton *instance = Singleton::get_instance();
    instance->use();
    delete instance;
    Singleton *instance_2 = Singleton::get_instance();
    instance_2->use();
    return 0;
}

