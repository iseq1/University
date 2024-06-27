#include <iostream>
using namespace std;

bool inequality(char a[], char b[]){
    int i = 0;
    while(true){
        char a0 = a[i], b0 = b[i];
        if(a0 >= 65 && a0 <= 90)
            a0 += 32;
        if(b0 >= 65 && b0 <= 90)
            b0 += 32;
        if(a0 > b0){
            return true;
        }
        else if(a0 < b0)
            return false;
        else if(a0 == b0 && a0 == '\0')
            break;
        i++;
    }
    return false;
}

int main() {
    char txt[]="Science is organized knowledge and wisdom is organized life";
    int word_count=0, max_len_word=0, current_len=0;

    for (int i=0; txt[i]!='\0'; i++) {
        if(txt[i] != ' ' && txt[i] != '\0' && (txt[i+1] == ' ' || txt[i+1] == '\0')) {word_count++;}  //число слов

        if(txt[i] != ' ' && txt[i] != '\0')
            current_len++;
        else {
            if(max_len_word < current_len) {max_len_word = current_len;}   //слово максимальной длинны
            current_len = 0;
        }
    }

    char **words = new char*[word_count];
    int k = 0; //счетчик по изначальной строке
    for(int i = 0; i < word_count; i++){
        words[i] = new char[max_len_word+1];
        for(int j = 0; j < max_len_word+1; j++){
            if(txt[k] != ' ' && txt[k] != '\0'){
                words[i][j] = txt[k];
                k++;
            }
            else{
                words[i][j] = '\0';
                k++;
                while(txt[k] == ' ') k++;
                break;
            }
        }
    }

    //сортировка массива строк
    for(int i = 1; i < word_count; i++){
        for(int j = 0; j < word_count - i; j++){
            if(inequality(words[j], words[j + 1])){
                swap(words[j], words[j + 1]);
            }
        }
    }

    //вывод строк
    for(int i = 0; i < word_count; i++){
        cout << words[i] << endl;
    }


}