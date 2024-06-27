/*
7. ��� �����, ��������� �� ����. ������� �������, �������
���������� ����� � ��������� ����� ������� W, �������� ������
������� ����� �������. ������ ����� � ������ ������ � ������,
����� ����� � ���������.
*/

#include <iostream>

void Build_In_Width(char *str, int w);  //�������� ����� �� �������� ������
int* Word_Length(char *str, int numWords); //����� ������������� ����� � ������
int Word_Count(char *str); //���������� ���� � ������
int* Insert_Space(int *wordsLen, int numWords, int w); // ������� ����������� �������� � ��������� ������
void Split_Line(char *str);  //�������� ������ � ������ �� ������ � ������� ���������

// Science is organized knowledge and wisdom is organized life

using namespace std;
int main() {
    char *str = new char[500];
    cin.getline(str, 500);
    Split_Line(str); //�������� ������ � ������ �� ������ � ������� ���������
    int w; cin >> w;
    cout << w << endl;
    Build_In_Width(str, w); //�������� ����� �� �������� ������
}

void Split_Line(char *str){ //�������� ������ � ������ �� ������ � ������� ���������
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

void Build_In_Width(char *str, int w){ //�������� ����� �� �������� ������
    int numWords = Word_Count(str);
    int *wordsLen = Word_Length(str, numWords);
    //���������� ������ �������� ����� j-�� �����
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

int* Insert_Space(int *wordsLen, int numWords, int w){ // ������� ����������� �������� � ��������� ������
    int *spaces = new int[numWords];

    int lineLen = wordsLen[0];//������ �����
    int firstWord = 0;
    for(int i = 0; i < numWords; i++){
        //��, ��� ��� ���� � ������ + ������ + ���� �����
        if(i != numWords-1 && lineLen + 1 + wordsLen[i + 1] <= w){
            lineLen += 1 + wordsLen[i + 1];
        }
        else{
            int spaceLeft = w - lineLen;//�������� �������� ��������
            for(int j = firstWord; j < i; j++){
                spaces[j] = spaceLeft/(i - j);
                spaceLeft -= spaces[j];
            }
            spaces[i] = -1;//����������� �������� ������
            firstWord = i + 1;
            lineLen = wordsLen[i + 1];
        }
    }
    return spaces;
}

int Word_Count(char *str){ //���������� ���� � ������
    int numWords = 0;
    for(int i = 0; str[i] != '\0'; i++){
        if(str[i] != ' ' && str[i] != '\0' && (str[i + 1] == ' ' || str[i + 1] == '\0' )){
            numWords++;
        }
    }
    return numWords;
}

int* Word_Length(char *str, int numWords){ //����� ������������� ����� � ������
    int *wordsLen = new int[numWords];
    for(int i = 0; i < numWords; i++) wordsLen[i] = 0;
    //������� ����� ����
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