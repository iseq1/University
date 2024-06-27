#include <iostream>
using namespace std;

struct Connection {
    int number;
    int count;
};

int main() {
    setlocale(LC_ALL, "ru");
    int n; cout<<"Введите количетсво элементов"<<endl; cin>>n;
    int*mas=new int [n]; cout<<"Введите сами элементы:"<<endl;
    for(int i=0; i<n; i++) { cin>>mas[i]; } // массив пользователя
    int*counts=new int [n];
    for(int i=0; i<n; i++) { counts[i]=1; }
    int maxcount=0;
    for (int i=0; i<n; i++) {
        for (int j=i+1; j<n; j++) {
            if (mas[j]>mas[i] && counts[j] <= counts[i]) { counts[j] = counts[i] + 1; }
        }
    }
    for (int i=0; i<n; i++) {
        if (maxcount<counts[i]){
            maxcount=counts[i];
        }
    }
    cout<<"Максимальная возрастающая подпоследовательность равна:"<<maxcount<<endl;
    cout<<"Сама подпоследовательность: ";
    Connection nums[n];
    for(int i=0;i<n;i++){
        nums[i].number=mas[i];
        nums[i].count=counts[i];
    }
    int f=0;
    for (int i=0; i<n; i++) {
        if (nums[f].number<nums[i].number && nums[i].count-nums[f].count==1) {
            cout<<nums[f].number;
            f++;
        }
    }

}
