/*
7. Дан текст, состоящий из слов. Создать функцию, которая
напечатает слова в несколько строк шириной W, вставляя лишние
пробелы между словами. Начало слова – первый символ в строке,
конец слова – последний.
*/

#include <iostream>

void Build_In_Width(char *str, int w);  //Образуем текст по заданной ширине
int* Word_Length(char *str, int numWords); //Длина определенного слова в строке
int Word_Count(char *str); //Количество слов в строке
int* Insert_Space(int *wordsLen, int numWords, int w); // Вставка необходимых пробелов и табуляция строки
void Split_Line(char *str);  //Отделяем строку с фразой от строки с пустыми символами

// Science is organized knowledge and wisdom is organized life

using namespace std;
int main() {
    char *str = new char[500];
    cin.getline(str, 500);
    Split_Line(str); //Отделяем строку с фразой от строки с пустыми символами
    int w; cin >> w;
    cout << w << endl;
    Build_In_Width(str, w); //Образуем текст по заданной ширине
}

void Split_Line(char *str){ //Отделяем строку с фразой от строки с пустыми символами
    int len;
    for(int i = 0; ; i++){
        if(str[i] == '\0'){
            len = i;
            break;
        }
    }
    char *newStr = new char[len];
    for(int i = 0 ; i < len; i++){
        newStr[i] = str[i];
    }
}

void Build_In_Width(char *str, int w){ //Образуем текст по заданной ширине
    int numWords = Word_Count(str);
    int *wordsLen = Word_Length(str, numWords);
    //количество лишних пробелов после j-го слова
    int *spaces = Insert_Space(wordsLen, numWords, w);

    int j = 0;
    for(int i = 0; ; i++){
        cout << str[i];
        if(str[i] == ' '){
            if(spaces[j] != -1) {
                for (int k = 0; k < spaces[j]; k++) {
                    cout << ' ';
                }
            }
            else{
                cout << '\n';
            }
            j++;
        }
        else if(str[i] == '\0') {
            cout << '\n';
            break;
        }
    }
}

int* Insert_Space(int *wordsLen, int numWords, int w){ // Вставка необходимых пробелов и табуляция строки
    int *spaces = new int[numWords];

    int lineLen = wordsLen[0];//первое слово
    int firstWord = 0;
    for(int i = 0; i < numWords; i++){
        //то, что уже есть в строке + пробел + след слово
        if(i != numWords-1 && lineLen + 1 + wordsLen[i + 1] <= w){
            lineLen += 1 + wordsLen[i + 1];
        }
        else{
            int spaceLeft = w - lineLen;//осталось добавить пробелов
            for(int j = firstWord; j < i; j++){
                spaces[j] = spaceLeft/(i - j);
                spaceLeft -= spaces[j];
            }
            spaces[i] = -1;//обозначение переноса строки
            firstWord = i + 1;
            lineLen = wordsLen[i + 1];
        }
    }
    return spaces;
}

int Word_Count(char *str){ //Количество слов в строке
    int numWords = 0;
    for(int i = 0; str[i] != '\0'; i++){
        if(str[i] != ' ' && str[i] != '\0' && (str[i + 1] == ' ' || str[i + 1] == '\0' )){
            numWords++;
        }
    }
    return numWords;
}

int* Word_Length(char *str, int numWords){ //Длина определенного слова в строке
    int *wordsLen = new int[numWords];
    for(int i = 0; i < numWords; i++) wordsLen[i] = 0;
    //считаем длины слов
    int j = 0;
    for(int i = 0; ; i++){
        if(str[i] != ' ' && str[i] != '\0')
            wordsLen[j]++;
        else{
            j++;
        }

        if(str[i] == '\0')
            break;
    }
    return wordsLen;
}