#include <iostream>
using namespace std;

/*

struct Advertising {
    int adsShown;
    double clickThroughRatePercentage;
    double averageEarningsPerClick;
};

void output(Advertising ad){ cout<<endl;
    cout << "Number of ads shown: " << ad.adsShown << endl;
    cout << "Click through rate: " << ad.clickThroughRatePercentage << endl;
    cout << "Average earnings per click: $" << ad.averageEarningsPerClick << endl;
    cout << "Total Earnings: $" <<(ad.adsShown * ad.clickThroughRatePercentage / 100 * ad.averageEarningsPerClick) << endl;
}


int main() {
    setlocale(LC_ALL, "ru");
    Advertising add;

    cout << "How many ads were shown today? ";
    cin >> add.adsShown;
    cout << "What percentage of users clicked on the ads? ";
    cin >> add.clickThroughRatePercentage;
    cout << "What was the average earnings per click? ";
    cin >> add.averageEarningsPerClick;

    output(add);

    return 0;
}

 */


  /*

struct Drob
{
    int chislitel;
    int znamenatel;
};

void multiply(Drob d1, Drob d2)
{
    // Не забываем об операторе static_cast, иначе компилятор выполнит целочисленное деление!
    cout << static_cast<float>(d1.chislitel* d2.chislitel) / (d1.znamenatel* d2.znamenatel);
}

int main()
{
    // Определяем первую переменную-дробь
    Drob d1;
    cout << "Input the first chislitel: ";
    cin >> d1.chislitel;
    cout << "Input the first znamenatel: ";
    cin >> d1.znamenatel;

    // Определяем вторую переменную-дробь
    Drob d2;
    cout << "Input the second chislitel: ";
    cin >> d2.chislitel;
    cout << "Input the second znamenatel: ";
    cin >> d2.znamenatel;

    multiply(d1, d2);

    return 0;
}

   */



  /*

struct Train{
    char path[50];
    int number;
    int hour;
    int min;
};

int main(){
    setlocale(LC_ALL, "ru");
    cout<<"Введите количество поездов на станции!"<<endl; const int n = 2;
    Train trains[n];
    for(int i=0; i<n; i++) {
        cout<<"Введите пункт назначения поезда №"<<i+1<<endl;
        cin>>trains[i].path;
        cout<<"Введите номер поезда №"<<i+1<<endl;
        cin>>trains[i].number;
        cout<<"Введите время (час, минуты) отправления поезда №"<<i+1<<endl;
        cin>>trains[i].hour>>trains[i].min;
    }

    for(int i=0;i<n;i++){
        for(int j=i+1; j<n;j++){
            if(strcmp(trains[i].path, trains[j].path)>0){
                Train tmp = trains[i];
                trains[i] = trains[j];
                trains[j] = tmp;
            }
        }
    }
    cout<<"Все возможные рейсы поездов на текущий период!"<<endl;
    for (int i=0;i<n;++i){
        cout << " Пункт назначения: " << trains[ i ].path << " Номер: " << trains[ i ].number << " Время отправления: " << trains[ i ].hour << ":" << trains[ i ].min  << endl << endl;
    }

    int time_h;
    int time_min;
    int k = 0;
    cout << "Введите ваше время (часы затем минуты)" << endl;
    cin >> time_h >> time_min;
    cout << " Ваше время:" << time_h <<":" << time_min << endl << endl;
    for(int i = 0; i < n; i++)
    {
        if((time_h < trains[i].hour) || (time_h == trains[i].hour && time_min < trains[i].min))
        {
            cout << " следующие поезда отправятся после вашего времени: " << trains[i].number  <<" с временем "<< trains[i].hour << ":"<< trains[i].min << endl;
            k++;
        }
    }
    if(k == 0)
        cout << " Нет подходящих поездов" << endl;


    return 0;
}


*/


  /*

struct Stud{
    char name[15];
    int group;
    double ses[5];
};

int main(){
    setlocale(LC_ALL, "ru");
    const int n=5;
    Stud students[n];
    cout<<"Введите Имя, группу, оценки по основным дисциплинам студента через пробел!";
    for(int i=0;i<n;i++){
        cin>>students[i].name>>students[i].group;
        for(int j=0; j<5;j++) {
            cin>>students[i].ses[j];
        }
    }
    for(int i=0;i<n;i++){
        for(int j=i+1; j<n;j++){
            if(students[i].group > students[j].group){
                Stud tmp = students[i];
                students[i] = students[j];
                students[j] = tmp;
            }
        }
    }
    double srzn=0, k=0;
    for(int i=0;i<n;i++){
        for(int j=0;j<5;j++){
            srzn+=students[i].ses[j];
        }
        if ((srzn/5)>=4) {
            cout<<students[i].name<<" "<<students[i].group<<" "<<srzn/5<<endl;
            k++;
        }
        srzn=0;
    }
    if (k==0){
        cout<<"Не нашлось подходящих студентов!";
    }
    return 0;
}


    */


  /*

struct Bday{
    int day;
    int month;
    int year;
};


struct Znak{
    char name[100];
    char zodiac[100];
    struct Bday;
};

int main(){ setlocale(LC_ALL, "ru");
    const int n=5;
    Znak book[n];
    Bday bday[n];
    cout<<"Введите Имя, Знак Зодиака и дату рождения (число, месяц, год) через пробел для каждого участника!"<<endl;
    for(int i=0;i<n;i++){
        cin>>book[i].name>>book[i].zodiac>>bday[i].day>>bday[i].month>>bday[i].year;
    }
    cout<<"Введите знак зодиака человека, которого вы хотите увидеть!"<<endl; char znak[50]; cin>>znak;
    int k=0;
    for(int i=0;i<n;i++){
        if (strcmp(znak, book[i].zodiac)==0) {
            cout<<book[i].name<<" "<<bday[i].day<<"."<<bday[i].month<<"."<<bday[i].year<<endl;
            k++;
        }
    }
    if (k==0) {
        cout<<"Подходящих людей не нашлось! ";
    }

    return 0;
}


    */
    /*

struct Worker{
    char name[25];
    int age;
    int experience;
    int pension;
};

int main() {
    const int n=5;
    Worker workers[n];
    cout<<"Input name, age, work experience through a space!"<<endl;
    int pension_age=62;
    for(int i=0;i<n;i++){
        cin>>workers[i].name>>workers[i].age>>workers[i].experience;
        workers[i].pension = pension_age - workers[i].age ;
    }
    for(int i=0;i<n;i++){
        if (workers[i].pension<=15) {
            cout<<workers[i].name<<" "<<workers[i].pension<<" years before retirement!"<<endl;
        }
    }

    return 0;
}


    */


struct Aeroflot{
    char destination[50];
    int number;
    char type[50];
};

int main(){
    const int n=7;
    Aeroflot airplanes[n];
    cout<<"Input destination, number, typo of airplanes through a space!"<<endl;
    for(int i=0;i<n;i++){
        cin>>airplanes[i].destination>>airplanes[i].number>>airplanes[i].type;
    }
    for(int i=0;i<n;i++){
        for(int j=i+1;j<n;j++){
            if (strcmp(airplanes[i].destination, airplanes[j].destination)>0) {
                Aeroflot temp=airplanes[i];
                airplanes[i]=airplanes[j];
                airplanes[j]=temp;
            }
        }
    }
    cout<<"Input type of airplane that u need!"<<endl; char type_air[50]; cin>>type_air;
    for(int i=0;i<n;i++){
        if(strcmp(airplanes[i].type, type_air)==0){
            cout<<airplanes[i].destination<<" "<<airplanes[i].number<<endl;
        }
    }
}